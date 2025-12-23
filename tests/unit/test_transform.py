from datetime import timedelta

from trailcam_pipeline.transform import group_into_events

from ..factories import ObservationFactory


def test_events_grouped_within_window():
    factory = ObservationFactory()
    observations = [
        factory.make(),
        factory.make(),
        factory.make(timestamp=factory.base_time + timedelta(minutes=15)),
    ]
    events = group_into_events(observations, timedelta(minutes=10))

    assert len(events) == 2
    assert len(events[0].observations) == 2
    assert len(events[1].observations) == 1


def test_different_cameras_not_grouped():
    factory = ObservationFactory()
    observations = [
        factory.make(),
        factory.make(),
        factory.make(camera_id="cam2"),
        factory.make(camera_id="cam2"),
        factory.make(camera_id="cam3"),
    ]
    events = group_into_events(observations, timedelta(minutes=10))

    assert len(events) == 3
    assert len(events[0].observations) == 2
    assert len(events[1].observations) == 2
    assert len(events[2].observations) == 1
