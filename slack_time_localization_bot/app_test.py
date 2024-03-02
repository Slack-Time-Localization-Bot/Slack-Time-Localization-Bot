import logging
from unittest.mock import call

import pytest

import slack_time_localization_bot
from slack_time_localization_bot.app import SlackTimeLocalizationBot


def create_test_bot(
    mocker,
    app_token="some-token",
    mock_user=None,
    mock_channel_members=None,
    mock_permalink=None,
):
    """Create a SlackTimeLocalizationBot instance with almost all dependencies mocked."""
    app_mock = mocker.MagicMock()
    app_mock.client = mocker.MagicMock()
    app_mock.event = mocker.MagicMock()
    app_mock.action = mocker.MagicMock()
    client_mock = mocker.MagicMock()
    app_mock.client = client_mock
    mock_user_info_result = mocker.MagicMock()
    mock_user_info_result.data = mock_user
    client_mock.users_info = mocker.MagicMock(return_value=mock_user_info_result)
    client_mock.chat_postEphemeral = mocker.MagicMock()
    mock_conversations_members_result = mocker.MagicMock()
    mock_conversations_members_result.data = mock_channel_members
    client_mock.conversations_members = mocker.MagicMock(
        return_value=mock_conversations_members_result
    )
    client_mock.chat_getPermalink = mocker.MagicMock(
        return_value={"permalink": mock_permalink}
    )

    bot = SlackTimeLocalizationBot(app_mock, app_token)
    return bot


def test_slack_bot_start(mocker):
    socket_mode_handler_instance_mock = mocker.MagicMock()
    socket_mode_handler_instance_mock.start = mocker.MagicMock()
    socket_mode_handler_class_mock = mocker.MagicMock(
        return_value=socket_mode_handler_instance_mock
    )

    bot = create_test_bot(mocker)
    bot.start(socket_mode_handler_class_mock)

    assert bot.app.event.call_count == 1
    assert bot.app.action.call_count == 1
    assert socket_mode_handler_class_mock.call_count == 1
    assert socket_mode_handler_instance_mock.start.call_count == 1


def test_slack_bot_message_without_temporal_expressions(mocker):
    mock_user = {
        "user": {
            "tz": "Europe/Amsterdam",
            "is_bot": False,
        }
    }
    bot = create_test_bot(mocker, mock_user=mock_user)

    message = {
        "channel": "some-channel",
        "user": "some-user",
        "text": "some-text-without-temporal_expressions",
        "ts": "some-ts",
    }
    bot.process_message(bot.app.client, message)

    bot.app.client.users_info.assert_called_once_with(user=message["user"])


TEST_MESSAGES = [
    (
        "Let's meet at 10:30 GMT.",
        "> at 10:30 GMT\n_10:30 (GMT)_ ➔ _11:30 (Europe/Amsterdam)_ or _10:30 (UTC)_",
    ),
    (
        "Let's meet at 10:30 UTC.",
        "> at 10:30 UTC\n_10:30 (UTC)_ ➔ _11:30 (Europe/Amsterdam)_",
    ),
    (
        "Let's meet at 10:30 CET.",
        "> at 10:30 CET\n_10:30 (CET)_ ➔ _10:30 (Europe/Amsterdam)_ or _09:30 (UTC)_",
    ),
    (
        "starting between at 5:00 and 7:00 CET",
        "> between at 5:00 and 7:00 CET\n_05:00 - 07:00 (CET)_ ➔ _05:00 - 07:00 (Europe/Amsterdam)_ "
        "or _04:00 - 06:00 (UTC)_",
    ),
]


@pytest.mark.parametrize("input_text,expected_message", TEST_MESSAGES)
def test_slack_bot_message_with_temporal_expressions(
    mocker, input_text, expected_message
):
    mock_user = {
        "user": {
            "id": "some-id",
            "name": "some-user",
            "tz": "Europe/Amsterdam",
            "is_bot": False,
        }
    }
    mock_channel_members = {"members": ["some-user", "some-other-user"]}

    bot = create_test_bot(
        mocker, mock_user=mock_user, mock_channel_members=mock_channel_members
    )

    message = {
        "channel": "some-channel",
        "user": "some-user",
        "text": input_text,
        "ts": "some-ts",
    }
    bot.process_message(bot.app.client, message)

    bot.app.client.users_info.assert_has_calls(
        [call(user=message["user"]), call(user="some-other-user")]
    )
    expected_blocks = [
        {
            "type": "section",
            "text": {
                "text": expected_message,
                "type": "mrkdwn",
            },
            "accessory": {
                "type": "button",
                "action_id": "dismiss",
                "accessibility_label": "Dismiss this message",
                "text": {
                    "type": "plain_text",
                    "text": "X",
                },
            },
        }
    ]
    bot.app.client.chat_postEphemeral.assert_has_calls(
        [
            call(
                channel="some-channel",
                user="some-id",
                blocks=expected_blocks,
                thread_ts=None,
            ),
        ]
    )


TEST_EDIT_MESSAGES = [
    (
        "Let's meet at 10:30 GMT.",
        "> at 10:30 GMT\n_10:30 (GMT)_ ➔ _11:30 (Europe/Amsterdam)_ or _10:30 (UTC)_",
    ),
]


@pytest.mark.parametrize("input_text,expected_message", TEST_EDIT_MESSAGES)
def test_slack_bot_message_edit_with_temporal_expressions(
    mocker, input_text, expected_message
):
    mock_user = {
        "user": {
            "id": "some-id",
            "name": "some-user",
            "tz": "Europe/Amsterdam",
            "is_bot": False,
        }
    }
    mock_channel_members = {"members": ["some-user", "some-other-user"]}
    expected_message = f"_<https://mockpermalink|Message> edited:_\n" + expected_message

    bot = create_test_bot(
        mocker,
        mock_user=mock_user,
        mock_channel_members=mock_channel_members,
        mock_permalink="https://mockpermalink",
    )

    message = {
        "channel": "some-channel",
        "subtype": "message_changed",
        "ts": "some-other-ts",
        "message": {
            "user": "some-user",
            "text": input_text,
            "ts": "some-ts",
        },
    }
    bot.process_message(bot.app.client, message)

    bot.app.client.users_info.assert_has_calls(
        [call(user=message["message"]["user"]), call(user="some-other-user")]
    )
    expected_blocks = [
        {
            "type": "section",
            "text": {
                "text": expected_message,
                "type": "mrkdwn",
            },
            "accessory": {
                "type": "button",
                "action_id": "dismiss",
                "accessibility_label": "Dismiss this message",
                "text": {
                    "type": "plain_text",
                    "text": "X",
                },
            },
        }
    ]
    bot.app.client.chat_getPermalink.assert_has_calls(
        [call(channel="some-channel", message_ts="some-ts")]
    )
    bot.app.client.chat_postEphemeral.assert_has_calls(
        [
            call(
                channel="some-channel",
                user="some-id",
                blocks=expected_blocks,
                thread_ts=None,
            ),
        ]
    )


def test_slack_bot_dismiss(mocker):
    mock_ack = mocker.MagicMock()
    mock_respond = mocker.MagicMock()
    bot = create_test_bot(mocker)

    bot.process_dismiss(mock_ack, mock_respond)

    mock_ack.assert_called_once()
    mock_respond.assert_called_once_with(delete_original=True)


def test_run(monkeypatch, mocker):
    mock_bot_instance = mocker.MagicMock()
    mock_bot_instance.start = mocker.MagicMock()
    mock_bot_cls = mocker.MagicMock(return_value=mock_bot_instance)
    monkeypatch.setattr(
        slack_time_localization_bot.app, "SlackTimeLocalizationBot", mock_bot_cls
    )
    slack_app_mock_instance = mocker.MagicMock()
    slack_app_mock_cls = mocker.MagicMock(return_value=slack_app_mock_instance)
    monkeypatch.setattr(slack_time_localization_bot.app, "App", slack_app_mock_cls)

    slack_time_localization_bot.app.run(
        slack_bot_token="some-token",
        slack_app_token="some-token",
        user_cache_size=100,
        user_cache_ttl=300,
        prefer_24h_interpretation=False,
        log_level=logging.DEBUG,
    )

    slack_app_mock_cls.assert_called_once_with(
        token="some-token",
    )
    mock_bot_cls.assert_called_once_with(
        app=slack_app_mock_instance,
        slack_app_token="some-token",
        user_cache_size=100,
        user_cache_ttl=300,
        prefer_24h_interpretation=False,
    )
    mock_bot_instance.start.assert_called_once()
