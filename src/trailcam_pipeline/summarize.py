from trailcam_pipeline.models import Event, EventSummary


def summarize_events(events: list[Event]):
    summaries: list[EventSummary] = []

    for event in events:
        duration = event.end_time - event.start_time
        detection_count = max(obs.count for obs in event.observations)
        summary = EventSummary(
            event_id=event.event_id,
            start_time=event.start_time,
            end_time=event.end_time,
            camera_id=event.camera_id,
            species=event.species,
            duration=duration,
            detection_count=detection_count,
        )
        summaries.append(summary)

    return summaries
