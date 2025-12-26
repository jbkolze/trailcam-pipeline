import csv
from pathlib import Path

from trailcam_pipeline.models import Event, EventRow
from trailcam_pipeline.projection import events_to_event_rows


def export_events_csv(events: list[Event], out_dir: Path) -> None:
    event_rows = events_to_event_rows(events)
    csv_path = out_dir / "events_summary.csv"
    field_names = EventRow.model_fields.keys()

    with open(csv_path, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()

        for event_row in event_rows:
            writer.writerow(event_row.model_dump())

    print(f"Data has been written to {csv_path}")
