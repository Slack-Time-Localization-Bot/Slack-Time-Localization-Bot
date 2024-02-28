# Slack Time Localization Bot

[![codecov](https://codecov.io/gh/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/graph/badge.svg?token=RHMXGIH8Z9)](https://codecov.io/gh/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot)

Detect temporal expressions in Slack messages (_tomorrow at 5 pm_) and translate them for readers in other timezones.

# Who is this for?

Many organizations have people around the globe communicating via Slack. 
That usually means a lot of different timezones.
So when people try to coordinate their activities a lot of time conversions have to happen when reading messages.
If you read `"How about tomorrow at 5 pm?"` you might need to do the following:

1. Check the author's timezone.
2. Check your own timezone (you usually know that already).
3. Convert `"tomorrow at 5 pm"` into your timezone.

This is cumbersome and prone to errors. Especially when dealing with summer/winter time.
This bot aims to help people with that.

The bot can easily be self-hosted and does not need to be reachable from the internet due to Slack's [socket mode](https://api.slack.com/apis/connections/socket).

## How It Works

Currently, the implementation is centered around Meta's [Duckling library](https://github.com/facebook/duckling). 
It can detect temporal expressions in [various languages](https://github.com/facebook/duckling/tree/main/Duckling/Dimensions) and extract a timestamp from it.
Since Duckling needs to know the language of the text in advance the library [lingua-py](https://github.com/pemistahl/lingua-py) is used to detect the language.
Big kudos to the authors of these libraries. Without them this bot could not have been developed in a feasible amount of time.

The Slack bot reads every message it has access to and uses Duckling to extract timestamps. 
For every possible reader of the message the bot then compares the timezone of the message author and the reader and translates the timestamp to the reader's timezone.
Finally, the bot will post an ephemeral message below the message with the detected temporal expressions and the timestamps translated to the local timezone.
That ephemeral message might look different for readers if they are not in the same timezone.

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
export USER_CACHE_SIZE=500 # number of user profiles to cache in memory
export USER_CACHE_TTL=600 # number of seconds a user profile will be cached in memory
export PREFER_24h_INTERPRETATION=true # set to true if 5:00 usually means 5 in the morning and not late afternoon
export DEBUG=false # set to true to enable verbose logging including message contents
slack-time-localization-bot
```

You can now invite the bot to a conversation is slack and the bot will translate temporal expressions for every message.

## Running Tests

Install poetry and run

```shell
poetry install
poetry run pytest ./slack_time_localization_bot
```
