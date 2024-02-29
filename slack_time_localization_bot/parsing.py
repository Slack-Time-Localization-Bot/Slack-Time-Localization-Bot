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
    .with_minimum_relative_distance(0.3)
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


def select_time_values_based_on_24h_preference(
    candidates: List[datetime.datetime],
):
    """Pick the datetime which is most likely correct for a text written in 24h format.

    For example: If the text is "Let's meet at 6:00" the duckling will come up with 6 in the morning and 18:00 in the
    evening. Duckling might list 18:00 in the evening as first result, which would be used by the bot.
    If the administrator knows that their Slack workspace users always use the 24h format then 6 in the morning would
    be the correct interpretation.
    This function implements the 24h format preference by taking the first element and trying to find another element
    which is exactly 12h in the past (the day of the month is disregarded). If such an element exists it is returned.
    Else we just take the first element.
    """
    if len(candidates) == 1:
        return candidates[0]
    preferred_candidate = candidates[0]
    for candidate in candidates[1:]:
        if preferred_candidate.hour - candidate.hour == 12:
            # take other candidate if it is 12h in the future
            # for example 5:00 wins against 17:00
            return candidate
    return preferred_candidate


def text_to_temporal_expressions(
    text: str,
    reference_time: datetime.datetime,
    prefer_24h_interpretation: bool = True,
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
            candidates = [
                isoparse(x["value"])
                for x in result["value"]["values"]
                if x["grain"] != "day"
            ]
            if candidates:
                chosen_datetime = (
                    select_time_values_based_on_24h_preference(candidates)
                    if prefer_24h_interpretation
                    else candidates[0]
                )
                return_value.append(
                    TemporalExpression(
                        text=result["body"],
                        datetime=chosen_datetime,
                        timezone=detect_timezone(result["body"])
                        or reference_time.tzinfo,
                    )
                )
        elif result["value"]["type"] == "interval":
            interval_timezone = detect_timezone(result["body"])
            if interval_timezone and interval_timezone != reference_time.tzinfo:
                return_value += text_to_temporal_expressions(
                    result["body"],
                    reference_time.astimezone(interval_timezone),
                    prefer_24h_interpretation,
                )
            else:
                if "from" in result["value"]:
                    from_candidates = [
                        isoparse(x["from"]["value"])
                        for x in result["value"]["values"]
                        if x["from"]["grain"] != "day"
                    ]
                    if from_candidates:
                        chosen_from_datetime = (
                            select_time_values_based_on_24h_preference(from_candidates)
                            if prefer_24h_interpretation
                            else from_candidates[0]
                        )
                        return_value.append(
                            TemporalExpression(
                                text=result["body"],
                                datetime=chosen_from_datetime,
                                timezone=detect_timezone(result["body"])
                                or reference_time.tzinfo,
                            )
                        )
                if "to" in result["value"]:
                    to_candidates = [
                        isoparse(x["to"]["value"])
                        for x in result["value"]["values"]
                        if x["to"]["grain"] != "day"
                    ]
                    if to_candidates:
                        chosen_to_datetime = (
                            select_time_values_based_on_24h_preference(to_candidates)
                            if prefer_24h_interpretation
                            else to_candidates[0]
                        )
                        # correct interval end datetime
                        if "from" in result["value"]:
                            # for unknown reasons the time does not need to be corrected in half-intervals
                            if result["value"]["to"]["grain"] == "minute":
                                chosen_to_datetime = (
                                    chosen_to_datetime - datetime.timedelta(minutes=1)
                                )
                            elif result["value"]["to"]["grain"] == "hour":
                                chosen_to_datetime = (
                                    chosen_to_datetime - datetime.timedelta(hours=1)
                                )
                        return_value.append(
                            TemporalExpression(
                                text=result["body"],
                                datetime=chosen_to_datetime,
                                timezone=detect_timezone(result["body"])
                                or reference_time.tzinfo,
                            )
                        )
    return return_value
