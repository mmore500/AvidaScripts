import numpy as np
import pandas as pd


def load_population_dataframe(population_path: str) -> pd.DataFrame:
    res = pd.read_csv(
        population_path,
        comment="#",
        dtype={
            "Parent ID(s)": str,
            "Lineage Label": str,
            "Occupied Cell IDs": str,
            "Gestation (CPU) Cycle Offsets": str,
        },
        index_col=False,
        sep=" ",
        names=[
            "ID",  # column  1
            "Source",  # column  2
            "Source Args",  # column  3
            "Parent ID(s)",  # column  4
            "Number of currently living organisms",  # column  5
            "Total number of organisms that ever existed",  # column  6
            "Genome Length",  # column  7
            "Average Merit",  # column  8
            "Average Gestation Time",  # column  9
            "Average Fitness",  # column 10
            "Generation Born",  # column 11
            "Update Born",  # column 12
            "Update Deactivated",  # column 13
            "Phylogenetic Depth",  # column 14
            "Hardware Type ID",  # column 15
            "Inst Set Name",  # column 16
            "Genome Sequence",  # column 17
            "Occupied Cell IDs",  # column 18
            "Gestation (CPU) Cycle Offsets",  # column 19
            "Lineage Label",  # column 20
        ],
    )
    assert len([*res]) == 20  # 20 columns

    res["is host"] = res["Source"].str.contains("div")
    res["is parasite"] = res["Source"].str.contains("horz")
    assert (0 + res["is host"] + res["is parasite"]).unique() == [1]

    return res
