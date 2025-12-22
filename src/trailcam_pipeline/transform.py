import uuid
from datetime import timedelta

from trailcam_pipeline.models import Event, Observation


def group_into_events(
    observations: list[Observation], event_window: timedelta
) -> list[Event]:
    events: list[Event] = []

    sorted_obs = sorted(
        observations, key=lambda obs: (obs.camera_id, obs.species, obs.timestamp)
    )

    obs_list: list[Observation] = []

    for obs in sorted_obs:
        if not obs_list or _is_same_event(obs, obs_list[-1], event_window):
            obs_list.append(obs)
        else:
            events.append(_create_event(obs_list))
            obs_list = [obs]

    events.append(_create_event(obs_list))

    return events


def _create_event(obs_list: list[Observation]) -> Event:
    return Event(
        event_id=str(uuid.uuid4()),
        start_time=obs_list[0].timestamp,
        end_time=obs_list[-1].timestamp,
        camera_id=obs_list[0].camera_id,
        species=obs_list[0].species,
        observations=obs_list,
    )


def _is_same_event(
    new_obs: Observation, last_obs: Observation, event_window: timedelta
) -> bool:
    if new_obs.camera_id != last_obs.camera_id:
        return False
    if new_obs.species != last_obs.species:
        return False
    if new_obs.timestamp > last_obs.timestamp + event_window:
        return False
    return True
