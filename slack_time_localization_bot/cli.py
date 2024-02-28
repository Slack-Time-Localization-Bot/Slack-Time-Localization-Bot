import logging
from typing import Annotated

import typer

from slack_time_localization_bot import app


def main(
    slack_app_token: Annotated[str, typer.Argument(envvar="SLACK_APP_TOKEN")],
    slack_bot_token: Annotated[str, typer.Argument(envvar="SLACK_BOT_TOKEN")],
    user_cache_size: Annotated[int, typer.Option(envvar="USER_CACHE_SIZE")] = 500,
    user_cache_ttl: Annotated[int, typer.Option(envvar="USER_CACHE_TTL")] = 600,
    prefer_24h_interpretation: Annotated[
        bool, typer.Option(envvar="PREFER_24h_INTERPRETATION")
    ] = True,
    debug: Annotated[bool, typer.Option(envvar="DEBUG")] = False,
):
    """Detect temporal expressions in Slack messages ("tomorrow at 5 pm") and translate them for readers in other
    timezones."""

    log_level = logging.DEBUG if debug else logging.INFO

    app.run(
        slack_app_token=slack_app_token,
        slack_bot_token=slack_bot_token,
        user_cache_size=user_cache_size,
        user_cache_ttl=user_cache_ttl,
        prefer_24h_interpretation=prefer_24h_interpretation,
        log_level=log_level,
    )


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
