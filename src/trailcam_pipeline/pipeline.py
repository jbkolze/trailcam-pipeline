from trailcam_pipeline.ingest import load_detections_from_csv
from trailcam_pipeline.models import (
    Config,
    PipelineResult,
)
from trailcam_pipeline.transform import group_into_events
from trailcam_pipeline.validate import validate_detections


def run_pipeline(config: Config) -> PipelineResult:
    ingest_result = load_detections_from_csv(config.input_csv_path)
    validation_result = validate_detections(
        ingest_result.detections, config.min_confidence
    )
    events = group_into_events(validation_result.observations, config.event_window)

    return PipelineResult(
        ingest_count=ingest_result.count,
        observations=validation_result.observations,
        events=events,
        validation_errors=validation_result.errors,
        confidence_filter_count=validation_result.filter_count,
    )
