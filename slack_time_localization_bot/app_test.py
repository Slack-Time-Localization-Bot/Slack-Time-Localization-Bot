from unittest.mock import call

from slack_time_localization_bot.app import SlackTimeLocalizationBot


def test_slack_bot_start(mocker):
    app_mock = mocker.MagicMock()
    app_mock.client = mocker.MagicMock()
    app_mock.message = mocker.MagicMock()
    socket_mode_handler_instance_mock = mocker.MagicMock()
    socket_mode_handler_instance_mock.start = mocker.MagicMock()
    socket_mode_handler_class_mock = mocker.MagicMock(
        return_value=socket_mode_handler_instance_mock
    )

    bot = SlackTimeLocalizationBot(app_mock, "some-token")
    bot.start(socket_mode_handler_class_mock)

    assert app_mock.message.call_count == 1
    assert socket_mode_handler_class_mock.call_count == 1
    assert socket_mode_handler_instance_mock.start.call_count == 1


def test_slack_bot_message_without_temporal_expressions(mocker):
    app_mock = mocker.MagicMock()
    client_mock = mocker.MagicMock()
    app_mock.client = client_mock
    mock_user = {
        "user": {
            "tz": "Europe/Amsterdam",
            "is_bot": False,
        }
    }
    mock_user_info_result = mocker.MagicMock()
    mock_user_info_result.data = mock_user
    client_mock.users_info = mocker.MagicMock(return_value=mock_user_info_result)
    bot = SlackTimeLocalizationBot(app_mock, "some-token")

    message = {
        "channel": "some-channel",
        "user": "some-user",
        "text": "some-text-without-temporal_expressions",
    }
    bot.process_message(client_mock, message)

    client_mock.users_info.assert_called_once_with(user=message["user"])


def test_slack_bot_message_with_temporal_expressions(mocker):
    app_mock = mocker.MagicMock()
    client_mock = mocker.MagicMock()
    app_mock.client = client_mock
    mock_user = {
        "user": {
            "id": "some-id",
            "name": "some-user",
            "tz": "Europe/Amsterdam",
            "is_bot": False,
        }
    }
    mock_channel_members = {"members": ["some-user", "some-other-user"]}
    mock_user_info_result = mocker.MagicMock()
    mock_user_info_result.data = mock_user
    client_mock.users_info = mocker.MagicMock(return_value=mock_user_info_result)
    mock_conversations_members_result = mocker.MagicMock()
    mock_conversations_members_result.data = mock_channel_members
    client_mock.conversations_members = mocker.MagicMock(
        return_value=mock_conversations_members_result
    )
    bot = SlackTimeLocalizationBot(app_mock, "some-token")

    message = {
        "channel": "some-channel",
        "user": "some-user",
        "text": "Let's meet at 10:30 GMT.",
    }
    bot.process_message(client_mock, message)

    client_mock.users_info.assert_has_calls(
        [call(user=message["user"]), call(user="some-other-user")]
    )
