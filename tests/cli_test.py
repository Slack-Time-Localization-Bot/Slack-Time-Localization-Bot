import logging

from slack_time_localization_bot import app
from slack_time_localization_bot import cli


def test_cli(monkeypatch, mocker):
    mock_run = mocker.MagicMock()
    monkeypatch.setattr(app, "run", mock_run)
    cli_kwargs = {
        "slack_app_token": "some_app_token",
        "slack_bot_token": "some_bot_token",
        "user_cache_size": 100,
        "user_cache_ttl": 300,
        "prefer_24h_interpretation": False,
        "debug": True,
    }

    cli.main(**cli_kwargs)

    mock_run.assert_called_once_with(
        slack_app_token=cli_kwargs["slack_app_token"],
        slack_bot_token=cli_kwargs["slack_bot_token"],
        user_cache_size=cli_kwargs["user_cache_size"],
        user_cache_ttl=cli_kwargs["user_cache_ttl"],
        prefer_24h_interpretation=cli_kwargs["prefer_24h_interpretation"],
        log_level=logging.DEBUG,
    )
