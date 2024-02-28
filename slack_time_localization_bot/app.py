import datetime
import logging
import operator
from typing import Dict, List
from zoneinfo import ZoneInfo

from cachetools import TTLCache, cachedmethod
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from slack_time_localization_bot.parsing import (
    text_to_temporal_expressions,
    TemporalExpression,
)
from slack_time_localization_bot.utils import sanitize_message_text


class SlackTimeLocalizationBot:
    def __init__(
        self,
        app: App,
        slack_app_token: str,
        user_cache_size: int = 500,
        user_cache_ttl: int = 600,
        prefer_24h_interpretation: bool = True,
        time_format: str = "%H:%M",
    ):
        self.app = app
        self.slack_app_token = slack_app_token
        self.logger = logging.getLogger(__name__)
        self.app.message()(  # register process_message as handler for every incoming message
            self.process_message
        )
        self.user_cache = TTLCache(maxsize=user_cache_size, ttl=user_cache_ttl)
        self.time_format = time_format
        self.prefer_24h_interpretation = prefer_24h_interpretation

    def start(self, socket_mode_handler_cls: type[SocketModeHandler]):
        socket_mode_handler_cls(self.app, self.slack_app_token).start()

    @cachedmethod(operator.attrgetter("user_cache"))
    def get_user(self, user_id: str) -> Dict:
        return self.app.client.users_info(user=user_id).data["user"]

    @staticmethod
    def text_to_temporal_expressions_for_timezone(
        text: str, timezone: ZoneInfo, prefer_24h_interpretation: bool
    ) -> List[TemporalExpression]:
        reference_time = datetime.datetime.now(tz=timezone)
        return text_to_temporal_expressions(
            text, reference_time, prefer_24h_interpretation
        )

    def time_comparison_to_text(
        self,
        temporal_expression: TemporalExpression,
        user_timezone: datetime.tzinfo,
    ) -> str:
        return (
            f"> {temporal_expression.text}\n"
            f"_{temporal_expression.datetime.astimezone(temporal_expression.timezone).strftime(self.time_format)} "
            f"({temporal_expression.timezone})_ ➔ "
            f"_{temporal_expression.datetime.astimezone(user_timezone).strftime(self.time_format)} ({user_timezone})_ "
            f"or _{temporal_expression.datetime.astimezone(ZoneInfo('UTC')).strftime(self.time_format)} (UTC)_"
        )

    def process_message(self, client: WebClient, message):
        channel_id = message["channel"]
        thread_id = message.get("thread_ts", None)
        poster_id = message["user"]
        text = sanitize_message_text(message["text"])

        poster = self.get_user(poster_id)
        if not poster:
            return
        poster_timezone = ZoneInfo(poster["tz"])
        temporal_expressions = self.text_to_temporal_expressions_for_timezone(
            text, poster_timezone, self.prefer_24h_interpretation
        )

        if temporal_expressions:
            channel_members = client.conversations_members(channel=channel_id).data[
                "members"
            ]

            for channel_member in channel_members:
                member_user = self.get_user(channel_member)
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
                                lambda x: self.time_comparison_to_text(
                                    x, member_timezone
                                ),
                                temporal_expressions_with_different_tz,
                            )
                        )
                        ephemeral_message = "\n".join(ephemeral_message_lines)
                        self.logger.debug(
                            f'Sending ephemeral message to {member_user["name"]}: {ephemeral_message}'
                        )
                        client.chat_postEphemeral(
                            channel=channel_id,
                            user=member_id,
                            text=ephemeral_message,
                            thread_ts=thread_id,
                        )


def run(
    slack_bot_token: str,
    slack_app_token: str,
    user_cache_size: int = 500,
    user_cache_ttl: int = 600,
    prefer_24h_interpretation: bool = True,
    log_level: int | str = logging.INFO,
):
    logging.basicConfig(level=log_level)
    app = App(token=slack_bot_token)
    bot = SlackTimeLocalizationBot(
        app=app,
        slack_app_token=slack_app_token,
        user_cache_size=user_cache_size,
        user_cache_ttl=user_cache_ttl,
        prefer_24h_interpretation=prefer_24h_interpretation,
    )
    bot.start(SocketModeHandler)
