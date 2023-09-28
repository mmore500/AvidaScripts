import os

from AvidaScripts.GenericScripts.PopulationManipulation import (
    load_deme_replication_dataframe,
    stitch_deme_replication_dataframes,
)


def test_load_deme_replication_dataframe():
    paths = [
        f"{os.path.dirname(__file__)}/assets/deme_replication.dat",
        f"{os.path.dirname(__file__)}/assets/deme_replication2.dat",
    ]
    dataframes = [*map(load_deme_replication_dataframe, paths)]

    res = stitch_deme_replication_dataframes(dataframes)

    assert len(res) == 49 * 2
    assert res["Update"].is_monotonic_increasing
    assert res.iloc[0].to_dict() == {
        "Epoch": 0,
        "Epoch Update": 59,
        "Update": 59,
        "Source Deme ID": 4,
        "Target Deme ID": 0,
    }
    assert res.iloc[-1].to_dict() == {
        "Epoch": 1,
        "Epoch Update": 4989,
        "Update": 4989 * 2 + 1,
        "Source Deme ID": 42,
        "Target Deme ID": 8,
    }


def test_load_deme_replication_dataframe_epoch_length():
    paths = [
        f"{os.path.dirname(__file__)}/assets/deme_replication.dat",
        f"{os.path.dirname(__file__)}/assets/deme_replication2.dat",
    ]
    dataframes = [*map(load_deme_replication_dataframe, paths)]

    res = stitch_deme_replication_dataframes(
        dataframes,
        num_updates_per_epoch=5000,
    )

    assert len(res) == 49 * 2
    assert res["Update"].is_monotonic_increasing
    assert res.iloc[0].to_dict() == {
        "Epoch": 0,
        "Epoch Update": 59,
        "Update": 59,
        "Source Deme ID": 4,
        "Target Deme ID": 0,
    }
    assert res.iloc[-1].to_dict() == {
        "Epoch": 1,
        "Epoch Update": 4989,
        "Update": 4989 + 5000,
        "Source Deme ID": 42,
        "Target Deme ID": 8,
    }
