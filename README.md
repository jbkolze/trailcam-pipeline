# trailcam-pipeline

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![GitHub License](https://img.shields.io/github/license/jbkolze/trailcam-pipeline)
![Status](https://img.shields.io/badge/status-stable-green)


A Python-based CLI tool for summarizing annotated camera trap data into biologically meaningful metrics

This tool is intended for ecologists, conservation practitioners, and hobbyists working with annotated camera trap datasets.

trailcam-pipeline produces standard wildlife monitoring metrics, including:
- Event-level detection summaries (using configurable temporal grouping)
- Daily species counts
- Relative abundance indices
- Species-specific activity histograms

## Installation

trailcam-pipeline is a Python CLI tool. The recommended installation method is via `pipx`, which installs it in an isolated environment.

### Option 1: pipx (recommended)
```bash
pipx install git+https://github.com/jbkolze/trailcam-pipeline
```

### Option 2: pip
```bash
pip install git+https://github.com/jbkolze/trailcam-pipeline
```

## Usage
```
trailcam [input_file] [output_directory]
```
e.g.

```bash
trailcam ./data/example.csv ./output --event-window-minutes 10
```

See `trailcam --help` for more options.

## Methodology

### Input
Input data must be provided as a CSV file with one row per detection. Expected fields are as follows:

- Required
  - filename (str)
  - timestamp (str, ISO 8601)
  - camera_id (str)

- Optional
  - species (str)
  - count (int)
  - confidence (float)
  - location_id (str)
  - reviewer (str)

### Preparation

Input data flows through a quick pipeline to become analysis-ready:

1. **Ingest** - Normalize raw CSV rows into a consistent internal schema
2. **Validate** - Remove malformed, missing, or low-confidence detections
3. **Group** - Aggregate detections into events using a configurable time window

### Analysis

Three main analyses are conducted on the provided data for the active camera period:

- **Daily Counts** - Total number of observed species individuals for each date
- **Relative Abundance** - Average species individuals observed per day
- **Activity Histogram** - Typical time of detection for each species, by 15-minute bin

### Output

The pipeline writes results to the specified output directory. All outputs are deterministic and reproducible given the same input data and parameters.

#### CSV files
- `events_summary.csv` — grouped detection events
- `daily_counts.csv` — daily counts by species
- `relative_abundance.csv` — mean individuals observed per day

#### Plots
- `activity/[species].png` — activity patterns by 15-minute bin
