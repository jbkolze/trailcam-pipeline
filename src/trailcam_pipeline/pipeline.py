from trailcam_pipeline.export import export_summaries
from trailcam_pipeline.ingest import load_detections_from_csv
from trailcam_pipeline.models import Config
from trailcam_pipeline.summarize import summarize_events
from trailcam_pipeline.transform import group_into_events
from trailcam_pipeline.validate import validate_detections


def run_pipeline(config: Config):
    raw_detections = load_detections_from_csv(config.input_csv_path)
    observations = validate_detections(raw_detections, config.min_confidence)
    events = group_into_events(observations, config.event_window_timedelta)
    summaries = summarize_events(events)
    export_summaries(summaries, config.out_dir_path)
