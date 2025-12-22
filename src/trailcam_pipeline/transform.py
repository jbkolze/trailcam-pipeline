from datetime import timedelta

from trailcam_pipeline.models import Event, Observation


def group_into_events(
    observations: list[Observation], event_window_minutes: timedelta
) -> list[Event]:
    events: list[Event] = []

    return events
