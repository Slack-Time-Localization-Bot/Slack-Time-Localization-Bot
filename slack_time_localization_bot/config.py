import logging
import os

TIME_FORMAT = "%H:%M"
LOG_LEVEL = logging.INFO
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
USER_CACHE_SIZE = 500
USER_CACHE_TTL = 600
