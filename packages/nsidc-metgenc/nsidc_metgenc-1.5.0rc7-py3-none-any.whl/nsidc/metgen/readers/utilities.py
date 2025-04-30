import re
from datetime import timezone

from dateutil.parser import parse
from funcy import keep

from nsidc.metgen import constants


def temporal_from_premet(premet_path: str) -> list:
    if premet_path == "":
        raise Exception(
            "premet_dir is specified but no premet file exists for granule."
        )

    begin_date_keys = ["RangeBeginningDate", "Begin_date"]
    begin_time_keys = ["RangeBeginningTime", "Begin_time"]
    end_date_keys = [
        "RangeEndingDate",
        "End_date",
    ]
    end_time_keys = ["RangeEndingTime", "End_time"]

    pdict = premet_values(premet_path)
    begin = list(
        keep(
            [
                find_key_aliases(begin_date_keys, pdict),
                find_key_aliases(begin_time_keys, pdict),
            ]
        )
    )
    end = list(
        keep(
            [
                find_key_aliases(end_date_keys, pdict),
                find_key_aliases(end_time_keys, pdict),
            ]
        )
    )

    return [
        ensure_iso_datetime(td) for td in list(keep([" ".join(begin), " ".join(end)]))
    ]


def find_key_aliases(aliases: list, datetime_parts: dict) -> str:
    val = None

    for key in aliases:
        if key in datetime_parts:
            val = datetime_parts[key]
            break

    return val


def premet_values(premet_path: str) -> dict:
    pdict = {}
    with open(premet_path) as premet_file:
        for line in premet_file:
            key, val = re.sub(r"\s+", "", line).split("=")
            pdict[key] = val

    return pdict


def ensure_iso_datetime(datetime_str):
    """
    Parse ISO-standard datetime strings without a timezone identifier.
    """
    iso_obj = parse(datetime_str)
    return format_timezone(iso_obj)


def format_timezone(iso_obj):
    return (
        iso_obj.replace(tzinfo=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def points_from_spatial(spatial_path: str) -> list:
    """
    Read (lon, lat) points from a .spatial or .spo file.
    """
    if spatial_path == "":
        raise Exception(
            "spatial_dir is specified but no .spatial or .spo file exists for granule."
        )

    if re.search(constants.SPO_SUFFIX, spatial_path):
        # return spo contents, reversed to comply with Cumulus requirement for
        # counter-clockwise point order.
        return [p for p in reversed(raw_points(spatial_path))]

    # TODO: Add extra "sock" handling for points in a .spatial file
    # These files can be huge so might need another approach to handling the content
    # For now, simply return the points from the file with no changes.
    return raw_points(spatial_path)


def raw_points(spatial_path: str) -> list:
    with open(spatial_path) as file:
        return [
            {"Longitude": float(lon), "Latitude": float(lat)}
            for line in file
            for lon, lat in [line.split()]
        ]
