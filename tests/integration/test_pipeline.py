from datetime import timedelta
from pathlib import Path

from trailcam_pipeline.models import Config
from trailcam_pipeline.pipeline import run_pipeline


def test_pipeline():
    config = Config(
        input_csv_path=Path("tests", "data", "test.csv"),
        min_confidence=0.8,
        event_window=timedelta(minutes=5),
    )
    run_pipeline(config)
