import datetime
import logging
from typing import Dict, List
from zoneinfo import ZoneInfo

from cachetools import cached, TTLCache
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from slack_time_localization_bot.config import (
    TIME_FORMAT,
    SLACK_APP_TOKEN,
    SLACK_BOT_TOKEN,
)
from slack_time_localization_bot.parsing import (
    text_to_temporal_expressions,
    TemporalExpression,
)
from slack_time_localization_bot.utils import sanitize_message_text

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = App(token=SLACK_BOT_TOKEN)


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_active_users() -> Dict:
    client: WebClient = app.client
    members = client.users_list().data["members"]
    return {
        member["id"]: member
        for member in members
        if not member["is_bot"] and not member["deleted"]
    }


def text_to_temporal_expressions_for_timezone(
    text: str, timezone: ZoneInfo
) -> List[TemporalExpression]:
    reference_time = datetime.datetime.now(tz=timezone)
    return text_to_temporal_expressions(text, reference_time)


def time_comparison_to_text(
    temporal_expression: TemporalExpression,
    user_timezone: datetime.tzinfo,
) -> str:
    return (
        f"> {temporal_expression.text}\n"
        f"_{temporal_expression.datetime.astimezone(temporal_expression.timezone).strftime(TIME_FORMAT)} "
        f"({temporal_expression.timezone})_ ➔ "
        f"_{temporal_expression.datetime.astimezone(user_timezone).strftime(TIME_FORMAT)} ({user_timezone})_ "
        f"or _{temporal_expression.datetime.astimezone(ZoneInfo('UTC')).strftime(TIME_FORMAT)} (UTC)_"
    )


@app.message()
def process_message(client: WebClient, message):
    channel_id = message["channel"]
    poster_id = message["user"]
    text = sanitize_message_text(message["text"])

    all_users = get_active_users()
    if poster_id not in all_users:
        return
    poster = all_users[poster_id]
    poster_timezone = ZoneInfo(poster["tz"])
    temporal_expressions = text_to_temporal_expressions_for_timezone(
        text, poster_timezone
    )

    if temporal_expressions:
        channel_members = client.conversations_members(channel=channel_id).data[
            "members"
        ]

        for channel_member in channel_members:
            if channel_member in all_users:
                member_user = all_users[channel_member]
                member_id = member_user["id"]
                member_timezone = ZoneInfo(member_user["tz"])
                temporal_expressions_with_different_tz = list(
                    filter(
                        lambda x: x.timezone != member_timezone,
                        temporal_expressions,
                    )
                )
                if temporal_expressions_with_different_tz:
                    ephemeral_message_lines = list(
                        map(
                            lambda x: time_comparison_to_text(x, member_timezone),
                            temporal_expressions_with_different_tz,
                        )
                    )
                    ephemeral_message = "\n".join(ephemeral_message_lines)
                    logger.debug(
                        f'Sending ephemeral message to {member_user["name"]}: {ephemeral_message}'
                    )
                    client.chat_postEphemeral(
                        channel=channel_id,
                        user=member_id,
                        text=ephemeral_message,
                    )


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
