from pydantic import ValidationError

from trailcam_pipeline.models import (
    Observation,
    RawDetection,
    ValidationErrorReport,
    ValidationResult,
)


def validate_detections(
    detections: list[RawDetection], min_confidence: float
) -> ValidationResult:
    accepted_detections: list[RawDetection] = []

    accepted_detections = _filter_by_confidence(detections, min_confidence)
    observations, errors = _transform_into_observations(accepted_detections)
    filter_count = len(detections) - len(accepted_detections)

    return ValidationResult(
        observations=observations,
        errors=errors,
        filter_count=filter_count,
    )


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
