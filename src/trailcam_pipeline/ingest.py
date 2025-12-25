import csv
from pathlib import Path

from trailcam_pipeline.models import RawDetection


def load_detections_from_csv(input_csv_path: Path) -> list[RawDetection]:
    detections: list[RawDetection] = []

    required_columns = {"filename", "timestamp", "camera_id", "species"}

    with open(input_csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            raise CsvFormatError(f"Input .csv missing required columns: {missing}")
        for row in reader:
            norm_row = _normalize_row(row)
            detection = RawDetection.model_validate(norm_row)
            detections.append(detection)

    return detections


def _normalize_row(row: dict[str, str]) -> dict[str, str | None]:
    return {k: (v if v != "" else None) for k, v in row.items()}


class CsvFormatError(Exception):
    pass
