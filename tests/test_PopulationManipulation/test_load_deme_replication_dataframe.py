import os

from AvidaScripts.GenericScripts.PopulationManipulation import (
    load_deme_replication_dataframe,
)


def test_load_deme_replication_dataframe():
    pop_path = f"{os.path.dirname(__file__)}/assets/deme_replication.dat"
    res = load_deme_replication_dataframe(pop_path)

    assert len(res) == 49
    assert res.iloc[0].to_dict() == {
        "Epoch Update": 59,
        "Update": 59,
        "Source Deme ID": 4,
        "Target Deme ID": 0,
    }
    assert res.iloc[-1].to_dict() == {
        "Epoch Update": 4989,
        "Update": 4989,
        "Source Deme ID": 4,
        "Target Deme ID": 8,
    }
