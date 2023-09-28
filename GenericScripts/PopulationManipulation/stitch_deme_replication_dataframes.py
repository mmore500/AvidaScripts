from collections import Counter
import copy
import typing
import warnings

import opytional as opyt
import pandas as pd
from hstrat import _auxiliary_lib as hstrat_auxlib


def stitch_deme_replication_dataframes(
    deme_replication_df_sequence: typing.Iterable[pd.DataFrame],
    num_updates_per_epoch: typing.Optional[int] = None,
    mutate: bool = False,
) -> pd.DataFrame:
    """Join deme replication data from sequential evolutionary epochs.

    Parameters
    ----------
    deme_replication_df_sequence : Iterable[pd.DataFrame]
        Deserialized data from `load_deme_replication_dataframe`, sequenced
        chronologically.
    mutate : bool, default False
        Are side effects on the input dataframes allowed?

    Returns
    -------
    pandas.DataFrame
        Stitched dataframe with cumulative update values.
    """
    apply = (lambda x: x) if mutate else copy.deepcopy
    deme_replication_dfs = [*map(apply, deme_replication_df_sequence)]

    running_update_offset = 0
    for i, df in enumerate(deme_replication_dfs):
        df["Epoch"] = i

        assert df["Update"].is_monotonic_increasing
        if num_updates_per_epoch is not None:
            assert all(df["Update"] < num_updates_per_epoch)

        df["Update"] += running_update_offset
        if num_updates_per_epoch is not None:
            running_update_offset += num_updates_per_epoch
        else:
            running_update_offset = df["Update"].max() + 1

    agg_df = pd.concat(deme_replication_dfs, ignore_index=True)

    return agg_df
