from typing import Annotated

import typer

import slack_time_localization_bot.config as config


def main(
    slack_app_token: Annotated[str, typer.Argument(envvar="SLACK_APP_TOKEN")],
    slack_bot_token: Annotated[str, typer.Argument(envvar="SLACK_BOT_TOKEN")],
):
    """Detect temporal expressions in Slack messages ("tomorrow at 5 pm") and translate them for readers in other
    timezones."""
    config.SLACK_APP_TOKEN = slack_app_token
    config.SLACK_BOT_TOKEN = slack_bot_token
    # app needs to be imported after SLACK_APP_TOKEN is set or else this app will crash
    import slack_time_localization_bot.app as app

    app.run()


def run():
    typer.run(main)
