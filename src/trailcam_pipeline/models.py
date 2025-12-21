from datetime import datetime, timedelta
from typing import Annotated

from pydantic import BaseModel, DirectoryPath, Field, FilePath, PositiveInt


class Config(BaseModel):
    input_csv_path: FilePath
    out_dir_path: DirectoryPath
    min_confidence: Annotated[float, Field(ge=0, le=1)]
    event_window_timedelta: timedelta


class RawDetection(BaseModel):
    filename: str
    timestamp: str
    camera_id: str
    species: str | None = None
    count: int | None = None
    confidence: float | None = None
    location_id: str | None = None
    reviewer: str | None = None


class Observation(BaseModel):
    filename: str
    timestamp: datetime
    camera_id: str
    species: str
    count: PositiveInt = 1
    confidence: Annotated[float, Field(ge=0, le=1)] = 1.0
    location_id: str | None = None
    reviewer: str | None = None


class Event(BaseModel):
    event_id: str
    start_time: datetime
    end_time: datetime
    detections: list[Observation]


class EventSummary(BaseModel):
    event_id: str
    start_time: datetime
    end_time: datetime
    duration: timedelta
    species: str | None = None
    detection_count: int


class PipelineRun(BaseModel):
    run_id: str
    timestamp: datetime
    config: Config
    input_hash: str
    pipeline_version: str
