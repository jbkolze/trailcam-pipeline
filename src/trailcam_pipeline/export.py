import csv
from pathlib import Path

from trailcam_pipeline.models import EventSummary


def export_summaries(summaries: list[EventSummary], out_dir: Path) -> None:
    export_to_csv(summaries, out_dir)


def export_to_csv(summaries: list[EventSummary], out_dir: Path) -> None:
    csv_path = out_dir / "events_summary.csv"
    field_names = EventSummary.model_fields.keys()

    with open(csv_path, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()

        for summary in summaries:
            writer.writerow(summary.model_dump())

    print(f"Data has been written to {csv_path}")
