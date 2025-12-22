import csv
from pathlib import Path

from trailcam_pipeline.models import RawDetection


def load_detections_from_csv(input_csv_path: Path) -> list[RawDetection]:
    detections: list[RawDetection] = []

    with open(input_csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            norm_row = normalize_row(row)
            detection = RawDetection.model_validate(norm_row)
            detections.append(detection)

    return detections


def normalize_row(row: dict[str, str]) -> dict[str, str | None]:
    return {k: (v if v != "" else None) for k, v in row.items()}
