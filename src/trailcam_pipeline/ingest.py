import csv
from pathlib import Path

from dateutil.parser import parse

from trailcam_pipeline.models import IngestCsvResult, RawDetection


def load_detections_from_csv(input_csv_path: Path) -> IngestCsvResult:
    results = IngestCsvResult()

    required_columns = {"filename", "timestamp", "camera_id", "species"}

    with open(input_csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            raise CsvFormatError(f"Input .csv missing required columns: {missing}")
        for row in reader:
            results.count.read += 1
            try:
                norm_row = _normalize_row(row)
                detection = RawDetection.model_validate(norm_row)
                results.detections.append(detection)
                results.count.written += 1
            except CsvFormatError:
                results.count.dropped += 1

    return results


def _normalize_row(row: dict[str, str]) -> dict[str, str | None]:
    normalized: dict[str, str | None] = {}
    for k, v in row.items():
        if v == "":
            normalized[k] = None
            continue

        # Adjust for non-zero-padded timestamps
        if k == "timestamp":
            try:
                dt = parse(v)
                normalized[k] = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                raise CsvFormatError(f"Invalid timestamp '{v}': {e}") from e
        else:
            normalized[k] = v

    return normalized


class CsvFormatError(Exception):
    pass
