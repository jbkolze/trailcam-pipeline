from trailcam_pipeline.validate import validate_detections

from ..factories import RawDetectionFactory


def test_low_confidence_detections_filtered():
    factory = RawDetectionFactory()
    detections = [
        factory.make(confidence=1.0),
        factory.make(confidence=0.9),
        factory.make(confidence=0.8),
        factory.make(confidence=0.7),
        factory.make(confidence=0.6),
    ]
    observations = validate_detections(detections, 0.9)

    assert len(observations) == 2


def test_blank_count_or_confidence_populated():
    factory = RawDetectionFactory()
    detections = [
        factory.make(),
        factory.make(),
        factory.make(),
    ]

    # Set blanks manually to avoid default overrides
    detections[1].count = None
    detections[2].confidence = None

    observations = validate_detections(detections, 0.5)

    assert len(observations) == 3
    assert observations[1].count == 1
    assert observations[2].confidence == 1.0


def test_drops_blank_species():
    factory = RawDetectionFactory()
    detections = [
        factory.make(),
        factory.make(),
        factory.make(),
    ]

    # Set blanks manually to avoid default overrides
    detections[0].species = None
    detections[2].species = None

    observations = validate_detections(detections, 0.5)

    assert len(observations) == 1
