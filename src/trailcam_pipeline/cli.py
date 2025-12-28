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
from trailcam_pipeline.ingest import CsvFormatError
from trailcam_pipeline.models import Config
from trailcam_pipeline.pipeline import run_pipeline
from trailcam_pipeline.plot import export_activity_density_plots

cli = Typer()


@cli.command()
def run(
    input_csv_path: Path,
    out_dir_path: Path,
    min_confidence: float = 0.8,
    event_window_minutes: int = 5,
):
    activity_dir = out_dir_path / "activity"
    print("----- Input -----")
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
        print("----- Processing -----")
        result = run_pipeline(config)
        print("Data pipeline completed successfully")
        daily_counts = create_daily_species_counts(result.events)
        print("Daily species count analysis completed successfully")
        abundance = calculate_relative_abundance_index(result.events)
        print("Relative abundance analysis completed successfully")
        densities = create_activity_histograms(result.events)
        print("Species activity windows computed successfully")
    except CsvFormatError as e:
        print("Could not process input .csv file:")
        print(e)
        return

    print("")
    print("----- Output -----")
    export_events_csv(result.events, out_dir_path)
    export_daily_species_counts_csv(daily_counts, out_dir_path)
    export_relative_abundance_csv(abundance, out_dir_path)
    export_activity_density_plots(densities, activity_dir)


if __name__ == "__main__":
    cli()
