import datetime
import logging
import zoneinfo
from dataclasses import dataclass
from typing import List, Optional
from zoneinfo import ZoneInfo

import regex as re
from dateutil.parser import isoparse
from duckling import (
    load_time_zones,
    parse_ref_time,
    parse_lang,
    default_locale_lang,
    Context,
    parse_dimensions,
    parse,
)
from lingua import LanguageDetectorBuilder

detector = (
    LanguageDetectorBuilder.from_all_spoken_languages()
    .with_preloaded_language_models()
    .build()
)
time_zones = load_time_zones("/usr/share/zoneinfo")

# initializations that should be done once on module load
logger = logging.getLogger(__name__)
timezone_regex = re.compile(r" (\L<tz>)", tz=zoneinfo.available_timezones())


@dataclass
class TemporalExpression:
    text: str
    datetime: datetime.datetime
    timezone: datetime.tzinfo


def detect_language(text: str) -> Optional[str]:
    if len(text) >= 5:
        language = detector.detect_language_of(text)
        if language:
            return language.iso_code_639_1.name
    return "EN"


def detect_timezone(text: str) -> Optional[datetime.tzinfo]:
    match = timezone_regex.search(text)
    if match:
        return ZoneInfo(match.group(1))
    return None


def text_to_temporal_expressions(
    text: str, reference_time: datetime.datetime
) -> List[TemporalExpression]:
    lang = detect_language(text)
    lang_for_duckling = parse_lang(lang)
    default_locale = default_locale_lang(lang_for_duckling)
    ref_time = parse_ref_time(
        time_zones, reference_time.tzinfo.key, int(reference_time.timestamp())
    )
    context = Context(ref_time, default_locale)
    output_dims = parse_dimensions(["time"])
    duckling_result = parse(text, context, output_dims, False)

    return_value = []
    for result in duckling_result:
        if result["value"]["type"] == "value":
            # result is a single point in time
            return_value.append(
                TemporalExpression(
                    text=result["body"],
                    datetime=isoparse(result["value"]["value"]),
                    timezone=detect_timezone(result["body"]) or reference_time.tzinfo,
                )
            )
        elif (
            result["value"]["type"] == "interval"
            and "from" in result["value"]
            and "to" in result["value"]
        ):
            interval_timezone = detect_timezone(result["body"])
            if interval_timezone and interval_timezone != reference_time.tzinfo:
                return_value += text_to_temporal_expressions(
                    result["body"], reference_time.astimezone(interval_timezone)
                )
            else:
                return_value.append(
                    TemporalExpression(
                        text=result["body"],
                        datetime=isoparse(result["value"]["from"]["value"]),
                        timezone=detect_timezone(result["body"])
                        or reference_time.tzinfo,
                    )
                )
                to_datetime = isoparse(result["value"]["to"]["value"])
                # correct interval end datetime
                if result["value"]["to"]["grain"] == "minute":
                    to_datetime = to_datetime - datetime.timedelta(minutes=1)
                elif result["value"]["to"]["grain"] == "hour":
                    to_datetime = to_datetime - datetime.timedelta(hours=1)
                return_value.append(
                    TemporalExpression(
                        text=result["body"],
                        datetime=to_datetime,
                        timezone=detect_timezone(result["body"])
                        or reference_time.tzinfo,
                    )
                )
    return return_value
