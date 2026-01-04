import csv
from datetime import date
from pathlib import Path

from trailcam_pipeline.models import (
    DailySpeciesCount,
    DailySpeciesCountRow,
    Event,
    EventRow,
    RelativeAbundanceIndexRow,
)
from trailcam_pipeline.projection import (
    daily_species_counts_to_rows,
    events_to_event_rows,
    relative_abundance_to_rows,
)


def export_events_csv(events: list[Event], out_dir: Path) -> Path:
    event_rows = events_to_event_rows(events)
    csv_path = out_dir / "events_summary.csv"
    field_names = EventRow.model_fields.keys()

    with open(csv_path, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()

        for event_row in event_rows:
            writer.writerow(event_row.model_dump())

    return csv_path


def export_daily_species_counts_csv(
    daily_counts: dict[date, DailySpeciesCount], out_dir: Path
) -> Path:
    daily_count_rows = daily_species_counts_to_rows(daily_counts)
    csv_path = out_dir / "daily_counts.csv"
    field_names = DailySpeciesCountRow.model_fields.keys()

    with open(csv_path, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()

        for daily_count_row in daily_count_rows:
            writer.writerow(daily_count_row.model_dump())

    return csv_path


def export_relative_abundance_csv(abundance: dict[str, float], out_dir: Path) -> Path:
    abundance_rows = relative_abundance_to_rows(abundance)
    csv_path = out_dir / "relative_abundance.csv"
    field_names = RelativeAbundanceIndexRow.model_fields.keys()

    with open(csv_path, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()

        for abundance_row in abundance_rows:
            writer.writerow(abundance_row.model_dump())

    return csv_path
