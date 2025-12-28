from datetime import date

import pandas as pd

from trailcam_pipeline.models import (
    ActivityDensity,
    DailySpeciesCount,
    DailySpeciesCountRow,
    Event,
    EventRow,
    RelativeAbundanceIndexRow,
)


def events_to_event_rows(events: list[Event]):
    event_rows: list[EventRow] = []

    for event in events:
        duration = event.end_time - event.start_time
        individual_count = max(obs.count for obs in event.observations)
        event_row = EventRow(
            event_id=event.event_id,
            start_time=event.start_time,
            end_time=event.end_time,
            camera_id=event.camera_id,
            species=event.species,
            duration=duration,
            individual_count=individual_count,
        )
        event_rows.append(event_row)

    return event_rows


def daily_species_counts_to_rows(daily_counts: dict[date, DailySpeciesCount]):
    rows: list[DailySpeciesCountRow] = []

    for count in daily_counts.values():
        for species in count.individual_count.keys():
            rows.append(
                DailySpeciesCountRow(
                    date=count.date,
                    species=species,
                    individual_count=count.individual_count[species],
                    event_count=count.event_count[species],
                )
            )

    return rows


def relative_abundance_to_rows(abundance: dict[str, float]):
    rows: list[RelativeAbundanceIndexRow] = []

    for species, index in abundance.items():
        rows.append(RelativeAbundanceIndexRow(species=species, abundance_index=index))

    return rows


def activity_density_to_df(density: ActivityDensity):
    bins = density.bins
    bin_minutes = 1440 // len(bins)
    n_bins = len(bins)

    times = [(i * bin_minutes) / 60.0 for i in range(n_bins)]

    return pd.DataFrame(
        {"hour": times, "density": density.bins, "species": density.species}
    )
