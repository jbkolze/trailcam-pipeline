from pydantic import ValidationError

from trailcam_pipeline.models import Observation, RawDetection, ValidationErrorReport


def validate_detections(
    detections: list[RawDetection], min_confidence: float
) -> tuple[list[Observation], list[ValidationErrorReport]]:
    filtered_detections: list[RawDetection] = []

    filtered_detections = _filter_by_confidence(detections, min_confidence)
    observations, errors = _transform_into_observations(filtered_detections)

    return observations, errors


def _filter_by_confidence(
    detections: list[RawDetection], min_confidence: float
) -> list[RawDetection]:
    valid_detections: list[RawDetection] = []

    for detection in detections:
        if not detection.confidence:
            detection.confidence = 1.0
        if detection.confidence >= min_confidence:
            valid_detections.append(detection)

    return valid_detections


def _transform_into_observations(
    detections: list[RawDetection],
) -> tuple[list[Observation], list[ValidationErrorReport]]:
    observations: list[Observation] = []
    errors: list[ValidationErrorReport] = []

    for detection in detections:
        if not detection.count:
            detection.count = 1
        try:
            obs = Observation(**detection.model_dump())
            observations.append(obs)
        except ValidationError as e:
            print(f"Error occurred validating detection for {detection.filename}")
            print(e)
            errors.append(
                ValidationErrorReport(
                    detection=detection,
                    error_messages=[err["msg"] for err in e.errors()],
                )
            )

    return (observations, errors)
