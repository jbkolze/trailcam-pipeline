from pathlib import Path

from typer import Typer

cli = Typer()


@cli.command()
def run(
    input_csv_path: Path,
    out_dir_path: Path,
    min_confidence: float = 0.8,
    event_window_minutes: int = 5,
):
    print(f"Input CSV file: {input_csv_path}")
    if not input_csv_path.is_file():
        raise ValueError(f"{input_csv_path} does not exist")
    print(f"Output directory: {out_dir_path}")
    if not out_dir_path.is_dir():
        out_dir_path.mkdir(parents=True, exist_ok=False)
        print(f"Created directory: {out_dir_path}")
    print(f"Minimum confidence threshold: {min_confidence}")
    if min_confidence < 0 or min_confidence > 1:
        raise ValueError("min_confidence must be between 0 and 1.")
    print(f"Event window: {event_window_minutes} minutes")
    if event_window_minutes < 0:
        raise ValueError("event_window_minutes must be equal to or greater than 0.")


if __name__ == "__main__":
    cli()
