from datetime import timedelta
from pathlib import Path

from typer import Typer

from trailcam_pipeline.analysis.abundance import calculate_relative_abundance_index
from trailcam_pipeline.analysis.activity import create_activity_histograms
from trailcam_pipeline.analysis.count import create_daily_species_counts
from trailcam_pipeline.export import (
    export_daily_species_counts_csv,
    export_events_csv,
    export_relative_abundance_csv,
)
from trailcam_pipeline.ingest import CsvFormatError, load_detections_from_csv
from trailcam_pipeline.models import Config
from trailcam_pipeline.plot import export_activity_density_plots
from trailcam_pipeline.transform import group_into_events
from trailcam_pipeline.validate import validate_detections

cli = Typer()


@cli.command()
def run(
    input_csv_path: Path,
    out_dir_path: Path,
    min_confidence: float = 0.8,
    event_window_minutes: int = 5,
):
    activity_dir = out_dir_path / "activity"
    print("----- Config -----")
    print(f"Input CSV file: {input_csv_path}")
    if not input_csv_path.is_file():
        raise ValueError(f"{input_csv_path} does not exist")
    print(f"Output directory: {out_dir_path}")
    if not out_dir_path.is_dir():
        out_dir_path.mkdir(parents=True, exist_ok=False)
        print(f"Created directory: {out_dir_path}")
    if not activity_dir.is_dir():
        activity_dir.mkdir(parents=True, exist_ok=False)
    print(f"Minimum confidence threshold: {min_confidence}")
    if min_confidence < 0 or min_confidence > 1:
        raise ValueError("min_confidence must be between 0 and 1.")
    print(f"Event window: {event_window_minutes} minutes")
    if event_window_minutes < 0:
        raise ValueError("event_window_minutes must be equal to or greater than 0.")

    event_timedelta = timedelta(minutes=event_window_minutes)

    config = Config(
        input_csv_path=input_csv_path,
        min_confidence=min_confidence,
        event_window=event_timedelta,
    )

    try:
        print("")
        print("----- Ingestion -----")
        ingest_result = load_detections_from_csv(config.input_csv_path)
        print(f"Read {ingest_result.count.read} lines from CSV")
        print(f"Dropped {ingest_result.count.dropped} lines")
        print(f"Wrote {ingest_result.count.written} detection records")

        print("")
        print("----- Processing -----")
        validation_result = validate_detections(
            ingest_result.detections, config.min_confidence
        )
        print(
            f"Validated {len(validation_result.observations)} observations from {ingest_result.count.written} detections"
        )
        events = group_into_events(validation_result.observations, config.event_window)
        print(
            f"Grouped {len(validation_result.observations)} observations into {len(events)} events"
        )

        print("")
        print("----- Analysis -----")
        daily_counts = create_daily_species_counts(events)
        print(f"Computed daily species count for {len(daily_counts)} dates")
        abundance = calculate_relative_abundance_index(events)
        print(f"Computed relative abundanced for {len(abundance)} species")
        densities = create_activity_histograms(events)
        print(f"Computed activity windows for {len(densities)} species")
    except CsvFormatError as e:
        print("Could not process input .csv file:")
        print(e)
        return

    print("")
    print("----- Output -----")
    events_csv = export_events_csv(events, out_dir_path)
    print(f"Exported processed events data to {events_csv}")
    counts_csv = export_daily_species_counts_csv(daily_counts, out_dir_path)
    print(f"Exported daily species counts to {counts_csv}")
    abundance_csv = export_relative_abundance_csv(abundance, out_dir_path)
    print(f"Exported relative abundance statistics to {abundance_csv}")
    plot_paths = export_activity_density_plots(densities, activity_dir)
    print(f"Exported {len(plot_paths)} species activity plot(s) to {activity_dir}")


if __name__ == "__main__":
    cli()
