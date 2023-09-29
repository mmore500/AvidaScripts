import copy

from hstrat import _auxiliary_lib as hstrat_auxlib
import pandas as pd


def make_deme_replication_phylogeny(
    deme_replication_dataframe: pd.DataFrame,
    mutate: bool = False,
) -> pd.DataFrame:
    """Convert deme replication data to an alifestd phylogeny.

    Parameters
    ----------
    deme_replication_df : pd.DataFrame
        Deserialized data from `load_deme_replication_dataframe`.
    mutate : bool, default False
        Are side effects on the input dataframe allowed?

    Returns
    -------
    pandas.DataFrame
        Stitched phylogeny in alife standard format.
    """

    df = deme_replication_dataframe
    if not mutate:
        df = copy.deepcopy(df)

    # prepare deme geneses
    records = []
    for deme_id in {
        *df["Source Deme ID"].unique(),
        *df["Target Deme ID"].unique(),
    }:
        record = {
            "Source Deme ID": deme_id,
            "Target Deme ID": deme_id,
            "Update": 0,
            "Epoch Update": 0,
        }
        if "Epoch" in deme_replication_dataframe:
            record["Epoch"] = 0
        records.append(record)

    df = pd.concat(
        [pd.DataFrame.from_records(records), df],
        ignore_index=True,
    )

    # convert to alifestd phylo format
    assert df["Update"].is_monotonic_increasing
    df.reset_index(inplace=True, drop=True)
    df["id"] = df.index

    def find_ancestor(row: pd.Series) -> int:
        source_deme = row["Source Deme ID"]
        # row.name gives the index of the current row
        above_rows = df.iloc[: row.name]

        return max(
            above_rows[above_rows["Target Deme ID"] == source_deme]["id"],
            default=row["id"],  # is genesis
        )

    df["ancestor_id"] = df.apply(find_ancestor, axis=1)

    df["ancestor_list"] = hstrat_auxlib.alifestd_make_ancestor_list_col(
        df["id"],
        df["ancestor_id"],
    )

    df["creation_time"] = df["Update"]

    def find_successor(row: pd.Series) -> int:
        target_deme = row["Target Deme ID"]
        # row.name gives the index of the current row
        below_rows = df.iloc[row.name + 1 :]

        return max(
            below_rows[below_rows["Target Deme ID"] == target_deme]["creation_time"],
            default=df["Update"].max() + 1,  # is not destroyed
        )
    df["destruction_time"] = df.apply(find_successor, axis=1)

    assert hstrat_auxlib.alifestd_validate(df)

    return df
