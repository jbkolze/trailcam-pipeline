from pydantic import ValidationError

from trailcam_pipeline.models import Observation, RawDetection


def validate_detections(
    detections: list[RawDetection], min_confidence: float
) -> list[Observation]:
    filtered_detections: list[RawDetection] = []

    filtered_detections = _filter_by_confidence(detections, min_confidence)
    observations = _transform_into_observations(filtered_detections)

    return observations


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


def _transform_into_observations(detections: list[RawDetection]) -> list[Observation]:
    observations: list[Observation] = []

    for detection in detections:
        if not detection.count:
            detection.count = 1
        try:
            obs = Observation(**detection.model_dump())
            observations.append(obs)
        except ValidationError as e:
            print(f"Error occurred validating detection for {detection.filename}")
            print(e)

    return observations
