# Slack Time Localization Bot

Detect temporal expressions in Slack messages (_tomorrow at 5 pm_) and translate them for readers in other timezones.

## Quickstart

[Create a Slack app](https://api.slack.com/start/quickstart) with the following manifest:

```yaml
display_information:
  name: Time Localization
  description: Detect temporal expressions in Slack messages ("tomorrow at 5 pm") and translate them for readers in other timezones.
  background_color: "#240b24"
features:
  app_home:
    home_tab_enabled: false
    messages_tab_enabled: true
    messages_tab_read_only_enabled: false
  bot_user:
    display_name: Time Localization
    always_online: true
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - channels:history
      - chat:write
      - groups:history
      - groups:write
      - im:history
      - im:write
      - mpim:history
      - mpim:write
      - users:read
      - channels:read
      - groups:read
      - mpim:read
      - im:read
settings:
  event_subscriptions:
    bot_events:
      - app_home_opened
      - app_mention
      - channel_history_changed
      - group_history_changed
      - im_history_changed
      - message.channels
      - message.groups
      - message.im
      - message.mpim
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```

Create and get the bot token (under "OAuth & Permissions") and app token (under "Basic Information") for your Slack app.

```shell
pip install slack-time-localization-bot
```

> ℹ️ Currently only Linx x86_64 is supported

Finally you can run it with

```shell
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_APP_TOKEN=xapp-...
slack-time-localization-bot
```

You can now invite the bot to a conversation is slack and the bot will translate temporal expressions for every message.

## Running Tests

Install poetry and run

```shell
poetry install
poetry run pytest ./slack_time_localization_bot
```