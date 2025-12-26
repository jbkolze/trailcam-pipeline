from trailcam_pipeline.models import Event, EventRow


def events_to_event_rows(events: list[Event]):
    event_rows: list[EventRow] = []

    for event in events:
        duration = event.end_time - event.start_time
        detection_count = max(obs.count for obs in event.observations)
        event_row = EventRow(
            event_id=event.event_id,
            start_time=event.start_time,
            end_time=event.end_time,
            camera_id=event.camera_id,
            species=event.species,
            duration=duration,
            detection_count=detection_count,
        )
        event_rows.append(event_row)

    return event_rows
