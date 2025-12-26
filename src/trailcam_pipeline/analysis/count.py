from datetime import date

from trailcam_pipeline.models import DailySpeciesCount, Event
from trailcam_pipeline.utils import get_date_list


def create_daily_species_counts(events: list[Event]):
    daily_counts = initialize_daily_counts(events)

    for event in events:
        this_date = event.start_time.date()
        daily_counts[this_date].individual_count[event.species] += max(
            obs.count for obs in event.observations
        )
        daily_counts[this_date].event_count[event.species] += 1

    return daily_counts


def initialize_daily_counts(events: list[Event]) -> dict[date, DailySpeciesCount]:
    daily_counts: dict[date, DailySpeciesCount] = {}
    start_date = min(event.start_time for event in events).date()
    end_date = max(event.end_time for event in events).date()
    dates = get_date_list(start_date, end_date)
    all_species = sorted({event.species for event in events})

    for this_date in dates:
        count = DailySpeciesCount(
            date=this_date,
            individual_count={species: 0 for species in all_species},
            event_count={species: 0 for species in all_species},
        )
        daily_counts[this_date] = count

    return daily_counts
