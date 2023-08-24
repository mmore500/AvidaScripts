import pandas as pd


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

    res = grouped.reset_index()

    assert res["Viable"].astype(int).between(0, 1).all(), res[
        res["Viable"].astype(int).between(0, 1)
    ][
        "Viable"
    ].tolist()  # noqa fmt

    for col in [col for col in res.columns if col.startswith("Trait ")]:
        assert res[col].astype(int).between(0, 1).all(), (
            col,
            res[res[col].astype(int).between(0, 1)][col].tolist(),
        )  # noqa fmt

    return res
