from datetime import date

from trailcam_pipeline.models import (
    DailySpeciesCount,
    DailySpeciesCountRow,
    Event,
    EventRow,
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
