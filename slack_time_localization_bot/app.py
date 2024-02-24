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
    LOG_LEVEL, USER_CACHE_SIZE, USER_CACHE_TTL,
)
from slack_time_localization_bot.parsing import (
    text_to_temporal_expressions,
    TemporalExpression,
)
from slack_time_localization_bot.utils import sanitize_message_text

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)
app = App(token=SLACK_BOT_TOKEN)


@cached(cache=TTLCache(maxsize=USER_CACHE_SIZE, ttl=USER_CACHE_TTL))
def get_user(user_id: str) -> Dict:
    client: WebClient = app.client
    return client.users_info(user=user_id).data["user"]


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

    poster = get_user(poster_id)
    if not poster:
        return
    poster_timezone = ZoneInfo(poster["tz"])
    temporal_expressions = text_to_temporal_expressions_for_timezone(
        text, poster_timezone
    )

    if temporal_expressions:
        channel_members = client.conversations_members(channel=channel_id).data[
            "members"
        ]

        for channel_member in channel_members:
            member_user = get_user(channel_member)
            if member_user and not member_user["is_bot"]:
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


def run():
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    run()
