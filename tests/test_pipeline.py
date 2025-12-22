from datetime import timedelta
from pathlib import Path

from trailcam_pipeline.models import Config
from trailcam_pipeline.pipeline import run_pipeline


def test_pipeline():
    out_dir_path = Path("tests", "output")
    if not out_dir_path.is_dir():
        out_dir_path.mkdir(parents=True, exist_ok=False)

    config = Config(
        input_csv_path=Path("tests", "data", "test.csv"),
        out_dir_path=out_dir_path,
        min_confidence=0.8,
        event_window_timedelta=timedelta(minutes=5),
    )
    run_pipeline(config)
