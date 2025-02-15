import warnings

import numpy as np
import pandas as pd


def _load_population_dataframe(
    population_path: str,
    engine: str,
) -> pd.DataFrame:
    """Deserialze a spop file as Pandas DataFrame.

    Generates additional columns with convenience statistics.
    """

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
            # "Gestation (CPU) Cycle Offsets",  # column 19
            # "Lineage Label",  # column 20
        ],
        usecols=range(18),
        engine=engine,
    )
    assert len([*res]) == 18  # 20 columns minus last two
    assert (res["Number of currently living organisms"] >= 0).all(), (
        population_path,
        res[~(res["Number of currently living organisms"] >= 0)][
            "Number of currently living organisms"
        ],
    )
    assert (res["Total number of organisms that ever existed"] >= 0).all(), (
        population_path,
        res[~(res["Total number of organisms that ever existed"] >= 0)][
            "Total number of organisms that ever existed"
        ],
    )
    assert (res["Genome Length"] > 0).all(), (
        population_path,
        res[~(res["Genome Length"] > 0)]["Genome Length"],
    )

    is_div = res["Source"].str.contains("div")
    is_dup = res["Source"].str.contains("dup")
    res["is host"] = is_div | is_dup
    is_horz = res["Source"].str.contains("horz")
    is_vert = res["Source"].str.contains("vert")
    res["is parasite"] = is_horz | is_vert

    bad_mask = res["is host"] & res["is parasite"] | ~(
        res["is host"] | res["is parasite"]
    )
    if any(bad_mask):
        raise ValueError(
            "is host and is parasite are not mutually exclusive "
            f"in {bad_mask.sum()} rows, {res[bad_mask]}."
        )

    assert list((0 + res["is host"] + res["is parasite"]).unique()) == [1]

    res["role"] = np.where(res["is host"], "host", "parasite")

    return res


def load_population_dataframe(population_path: str) -> pd.DataFrame:
    """Deserialze a spop file as Pandas DataFrame.

    Generates additional columns with convenience statistics.
    """

    for engine in "c", "python":
        try:
            return _load_population_dataframe(population_path, engine)
        except Exception as exception:
            if engine == "c":
                continue
            elif engine == "python":
                warnings.warn(
                    f"load_population_dataframe failed with {exception=} "
                    f"and {population_path=} under both c and python engines"
                )
                raise exception
            else:
                assert False, engine
