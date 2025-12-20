# trailcam-pipeline

trailcam-pipeline is a command-line tool for creating summary reports from annotated camera trap data.

## Input

trailcam-pipeline expects a CSV file with the following fields:

- Required
  - filename
  - timestamp
  - camera_id

- Optional
  - species
  - count
  - confidence
  - location_id
  - reviewer

## Processing
trailcam-pipeline performs the following processing steps on provided data:
1. **Ingest** - Convert the data into a normalized internal format
2. **Validate** - Check the data to remove and log any erroneous entries
3. **Transform** - Transform the data into analysis-ready events
4. **Summarize** - Quantify data into reportable groups and clusters
5. **Export** - Generate reports based on summarized data

## Output
trailcam-pipeline can generate the following outputs:
- CSV files
- Plots