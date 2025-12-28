from datetime import date, datetime, timedelta
from typing import Annotated

from pydantic import BaseModel, Field, FilePath, PositiveInt


class Config(BaseModel):
    input_csv_path: FilePath
    min_confidence: Annotated[float, Field(ge=0, le=1)]
    event_window: timedelta


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


class ValidationErrorReport(BaseModel):
    detection: RawDetection
    error_messages: list[str]


class ValidationResult(BaseModel):
    observations: list[Observation]
    errors: list[ValidationErrorReport]
    filter_count: int


class Event(BaseModel):
    event_id: str
    start_time: datetime
    end_time: datetime
    camera_id: str
    species: str
    observations: list[Observation]


class EventRow(BaseModel):
    event_id: str
    start_time: datetime
    end_time: datetime
    camera_id: str
    species: str
    duration: timedelta
    individual_count: int


class PipelineRun(BaseModel):
    run_id: str
    timestamp: datetime
    config: Config
    input_hash: str
    pipeline_version: str


class PipelineResult(BaseModel):
    observations: list[Observation]
    events: list[Event]
    validation_errors: list[ValidationErrorReport]
    confidence_filter_count: int


class DailySpeciesCount(BaseModel):
    date: date
    individual_count: dict[str, int] = {}
    event_count: dict[str, int] = {}


class DailySpeciesCountRow(BaseModel):
    date: date
    species: str
    individual_count: int
    event_count: int


class RelativeAbundanceIndexRow(BaseModel):
    species: str
    abundance_index: float


class ActivityHistogram(BaseModel):
    species: str
    bins: list[int]


class SmoothActivityHistogram(BaseModel):
    species: str
    bins: list[float]


class ActivityDensity(BaseModel):
    species: str
    bins: list[float]
