from datetime import datetime, timedelta

from trailcam_pipeline.models import Event, Observation, RawDetection


class RawDetectionFactory:
    def __init__(self):
        self.base_time = datetime.now().replace(second=0, microsecond=0)
        self.counter = 1
        self.time_step = timedelta(minutes=1)

    def make(
        self,
        filename: str | None = None,
        timestamp: str | None = None,
        camera_id: str | None = None,
        species: str | None = None,
        count: int | None = None,
        confidence: float | None = None,
        location_id: str | None = None,
    ):
        detection = RawDetection(
            filename=filename or f"image{self.counter}.jpg",
            timestamp=timestamp
            or str(self.base_time + (self.time_step * self.counter)),
            camera_id=camera_id or "cam1",
            species=species or "deer",
            count=count or 1,
            confidence=confidence or 1.0,
            location_id=location_id or "trail1",
        )
        self.counter += 1
        return detection


class ObservationFactory:
    def __init__(self):
        self.base_time = datetime.now().replace(second=0, microsecond=0)
        self.counter = 1
        self.time_step = timedelta(minutes=1)

    def make(
        self,
        filename: str | None = None,
        timestamp: datetime | None = None,
        camera_id: str | None = None,
        species: str | None = None,
        count: int | None = None,
        confidence: float | None = None,
        location_id: str | None = None,
    ):
        obs = Observation(
            filename=filename or f"image{self.counter}.jpg",
            timestamp=timestamp or self.base_time + (self.time_step * self.counter),
            camera_id=camera_id or "cam1",
            species=species or "deer",
            count=count or 1,
            confidence=confidence or 1.0,
            location_id=location_id or "trail1",
        )
        self.counter += 1
        return obs


class EventFactory:
    def __init__(self):
        self.base_time = datetime.now().replace(second=0, microsecond=0)
        self.counter = 1
        self.time_step = timedelta(days=1)
        self.obs_factory = ObservationFactory()

    def make(
        self,
        interval: timedelta = timedelta(minutes=1),
        obs_count: int = 3,
        event_time: datetime | None = None,
        species: str = "deer",
        ind_count: int = 1,
    ):
        if event_time is None:
            event_time = self.base_time + (self.time_step * self.counter)
        obs: list[Observation] = []
        for i in range(obs_count):
            obs.append(
                self.obs_factory.make(
                    timestamp=event_time + interval * i,
                    species=species,
                    count=ind_count,
                )
            )
        event = Event(
            event_id=f"event_{self.counter}",
            start_time=obs[0].timestamp,
            end_time=obs[-1].timestamp,
            camera_id="cam1",
            species=species,
            observations=obs,
        )
        self.counter += 1
        return event
