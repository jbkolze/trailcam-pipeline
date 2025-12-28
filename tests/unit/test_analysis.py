from datetime import date, datetime, time, timedelta

from pytest import approx  # type: ignore

from tests.factories import EventFactory
from trailcam_pipeline.analysis.abundance import calculate_relative_abundance_index
from trailcam_pipeline.analysis.activity import create_activity_histograms
from trailcam_pipeline.analysis.count import create_daily_species_counts
from trailcam_pipeline.models import Event


def test_daily_species_count():
    day1 = date(2025, 12, 20)
    day2 = day1 + timedelta(days=1)
    day3 = day1 + timedelta(days=2)
    day1_dt = datetime.combine(day1, time(6))
    dat3_dt = datetime.combine(day3, time(6))
    dat3_late_dt = dat3_dt + timedelta(hours=8)

    factory = EventFactory()
    events = [
        factory.make(event_time=day1_dt, obs_count=4, species="deer", ind_count=2),
        factory.make(event_time=day1_dt, obs_count=3, species="raccoon", ind_count=1),
        factory.make(event_time=dat3_dt, obs_count=2, species="deer", ind_count=1),
        factory.make(event_time=dat3_late_dt, species="deer", ind_count=4),
    ]

    daily_counts = create_daily_species_counts(events)

    assert daily_counts[day1].individual_count["deer"] == 2
    assert daily_counts[day1].event_count["deer"] == 1
    assert daily_counts[day1].individual_count["raccoon"] == 1
    assert daily_counts[day1].event_count["raccoon"] == 1

    assert daily_counts[day2].individual_count["deer"] == 0
    assert daily_counts[day2].event_count["deer"] == 0

    assert daily_counts[day3].individual_count["deer"] == 5
    assert daily_counts[day3].event_count["deer"] == 2
    assert daily_counts[day3].individual_count["raccoon"] == 0
    assert daily_counts[day3].event_count["raccoon"] == 0


def test_relative_abundance_index():
    day1 = date(2025, 12, 20)
    day3 = day1 + timedelta(days=2)
    day1_dt = datetime.combine(day1, time(6))
    dat3_dt = datetime.combine(day3, time(6))
    dat3_late_dt = dat3_dt + timedelta(hours=8)

    factory = EventFactory()
    events = [
        factory.make(event_time=day1_dt, obs_count=4, species="deer", ind_count=2),
        factory.make(event_time=day1_dt, obs_count=3, species="raccoon", ind_count=1),
        factory.make(event_time=dat3_dt, obs_count=2, species="deer", ind_count=1),
        factory.make(event_time=dat3_late_dt, species="deer", ind_count=4),
    ]

    abundance = calculate_relative_abundance_index(events)

    assert abundance["deer"] == approx(7 / 3, 0.1)
    assert abundance["raccoon"] == approx(1 / 3, 0.1)


def test_activity_histogram():
    dt = datetime(2025, 12, 20, 2, 2)
    factory = EventFactory()
    events: list[Event] = []
    for i in range(9):
        events.append(factory.make(event_time=dt + timedelta(days=i)))
    for i in range(18):
        events.append(factory.make(event_time=dt + timedelta(days=i, minutes=30)))

    activity = create_activity_histograms(events)["deer"]

    smoothed = (
        [0.0] * 4 + [1.0, 1.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0] + [0.0] * 81
    )

    assert activity.species == "deer"
    assert activity.bins == approx([x / sum(smoothed) for x in smoothed])
