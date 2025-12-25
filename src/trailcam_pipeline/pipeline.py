from trailcam_pipeline.ingest import load_detections_from_csv
from trailcam_pipeline.models import (
    Config,
    PipelineResult,
)
from trailcam_pipeline.summarize import summarize_events
from trailcam_pipeline.transform import group_into_events
from trailcam_pipeline.validate import validate_detections


def run_pipeline(config: Config) -> PipelineResult:
    raw_detections = load_detections_from_csv(config.input_csv_path)
    validation_result = validate_detections(raw_detections, config.min_confidence)
    events = group_into_events(validation_result.observations, config.event_window)
    event_summaries = summarize_events(events)

    return PipelineResult(
        observations=validation_result.observations,
        events=events,
        event_summaries=event_summaries,
        validation_errors=validation_result.errors,
        confidence_filter_count=validation_result.filter_count,
    )
