from trailcam_pipeline.models import Event


def calculate_relative_abundance_index(events: list[Event]):
    start_date = min(event.start_time for event in events).date()
    end_date = max(event.end_time for event in events).date()
    days = (end_date - start_date).days + 1

    all_species = sorted({event.species for event in events})

    count = {species: 0 for species in all_species}

    for event in events:
        count[event.species] += max(obs.count for obs in event.observations)

    abundance = {species: count[species] / days for species in all_species}
    return abundance
