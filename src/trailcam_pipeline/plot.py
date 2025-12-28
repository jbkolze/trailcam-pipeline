from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from trailcam_pipeline.models import ActivityDensity
from trailcam_pipeline.projection import activity_density_to_df


def export_activity_density_plots(densities: dict[str, ActivityDensity], out_dir: Path):
    for species in densities.keys():
        df = activity_density_to_df(densities[species])

        plt.figure(figsize=(10, 4))

        sns.lineplot(data=df, x="hour", y="density")
        plt.fill_between(df["hour"], df["density"], alpha=0.3)  # type: ignore

        plt.xlim(0, 23.75)
        plt.xlabel("Time of day (hour)")
        plt.ylabel("Normalized activity density")
        plt.title(f"{species.capitalize()} activity window")

        plt.savefig(out_dir / f"{species}.png")
