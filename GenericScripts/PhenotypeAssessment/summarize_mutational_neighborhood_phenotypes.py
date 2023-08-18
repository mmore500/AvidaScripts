import numpy as np
import pandas as pd

from .count_environment_tasks import count_environment_tasks
from .iter_environment_tasks import iter_environment_tasks


def summarize_mutational_neighborhood_phenotypes(
    phenotype_df: pd.DataFrame,
) -> pd.DataFrame:
    """Condense genome-row phenotype data to summary statistics.

    Postprocessing applicable to `assess_mutational_neighborhood_phenotypes`.
    """

    phenotype_df = phenotype_df.copy()
    phenotype_df.drop(columns="Genome Sequence", inplace=True)
    phenotype_df.drop(columns="Phenotype", inplace=True)

    groupby = phenotype_df.groupby("Mutational Distance")
    grouped = groupby.mean()
    grouped["Num Sampled at Mutational Distance"] = groupby.size()

    return grouped.reset_index()
