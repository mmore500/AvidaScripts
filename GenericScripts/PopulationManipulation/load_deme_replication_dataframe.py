import numpy as np
import pandas as pd


def load_deme_replication_dataframe(data_path: str) -> pd.DataFrame:
    """Deserialze a deme replication data file as Pandas DataFrame."""

    res = pd.read_csv(
        data_path,
        comment="#",
        index_col=False,
        sep=",",
        names=[
            "Update",  # column  1
            "Source Deme ID",  # column  2
            "Target Deme ID",  # column  3
        ],
    )
    assert len([*res]) == 3  # 3 columns
    for key in res:
        assert (res[key] >= 0).all(), (
            data_path, res[~(res[key] >= 0)][key]
        )

    res["Epoch Update"] = res["Update"]

    return res
