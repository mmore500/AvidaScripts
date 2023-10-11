import pandas as pd


def load_germline_dataframe(data_path: str) -> pd.DataFrame:
    """Deserialze a .sgerm germline serialization file to Pandas DataFrame."""

    res = pd.read_csv(
        data_path,
        comment="#",
        index_col=False,
        sep=" ",
        names=[
            "Deme ID",  # column  1
            "Hardware Type ID",  # column  2
            "Inst Set Name",  # column  3
            "Genome Sequence",  # column  4
        ],
        dtype={
            "Deme ID": int,
            "Hardware Type ID": int,
            "Inst Set Name": str,
            "Genome Sequence": str,
        },
    )
    assert len([*res]) == 4  # 4 columns

    return res
