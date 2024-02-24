import logging
from typing import Annotated

import typer

import slack_time_localization_bot.config as config


def main(
    slack_app_token: Annotated[str, typer.Argument(envvar="SLACK_APP_TOKEN")],
    slack_bot_token: Annotated[str, typer.Argument(envvar="SLACK_BOT_TOKEN")],
    user_cache_size: Annotated[bool, typer.Option(envvar="USER_CACHE_SIZE")] = 500,
    user_cache_ttl: Annotated[bool, typer.Option(envvar="USER_CACHE_TTL")] = 600,
    debug: Annotated[bool, typer.Option(envvar="DEBUG")] = False,
):
    """Detect temporal expressions in Slack messages ("tomorrow at 5 pm") and translate them for readers in other
    timezones."""

    if debug:
        config.LOG_LEVEL = logging.DEBUG
    config.SLACK_APP_TOKEN = slack_app_token
    config.SLACK_BOT_TOKEN = slack_bot_token
    config.USER_CACHE_SIZE = user_cache_size
    config.USER_CACHE_TTL = user_cache_ttl
    # app needs to be imported after SLACK_APP_TOKEN is set or else this app will crash
    import slack_time_localization_bot.app as app

    app.run()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
