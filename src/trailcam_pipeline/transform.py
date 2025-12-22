from datetime import timedelta

from trailcam_pipeline.models import Event, Observation


def group_into_events(
    observations: list[Observation], event_window: timedelta
) -> list[Event]:
    events: list[Event] = []

    return events
