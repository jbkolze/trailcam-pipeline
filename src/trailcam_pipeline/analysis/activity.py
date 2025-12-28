from datetime import datetime

from trailcam_pipeline.models import (
    ActivityDensity,
    ActivityHistogram,
    Event,
    SmoothActivityHistogram,
)
from trailcam_pipeline.utils import (
    get_datetimes_midpoint,
    normalize_list,
    smooth_circular_list,
)

DAY_MINUTES = 1440


def create_activity_histograms(events: list[Event], bin_minutes: int = 15):
    if not (DAY_MINUTES % bin_minutes == 0):
        raise ValueError("ActivityHistogram bin_minutes must equally divide into 1440")
    bin_count = DAY_MINUTES // bin_minutes
    all_species = sorted({event.species for event in events})
    histograms: dict[str, ActivityHistogram] = {}

    for species in all_species:
        histograms[species] = ActivityHistogram(species=species, bins=[0] * bin_count)

    for event in events:
        timestamp = get_datetimes_midpoint(event.start_time, event.end_time)
        minute = minute_of_day(timestamp)
        bin = minute // bin_minutes
        histograms[event.species].bins[bin] += 1

    smoothed_histograms: dict[str, SmoothActivityHistogram] = {}
    for species, histogram in histograms.items():
        smooth_hist = SmoothActivityHistogram(
            species=species, bins=smooth_circular_list(histogram.bins)
        )
        smoothed_histograms[species] = smooth_hist

    normal_histograms: dict[str, ActivityDensity] = {}
    for species, histogram in smoothed_histograms.items():
        normal_hist = ActivityDensity(
            species=species, bins=normalize_list(histogram.bins)
        )
        normal_histograms[species] = normal_hist

    return normal_histograms


def minute_of_day(dt: datetime) -> int:
    return dt.hour * 60 + dt.minute
