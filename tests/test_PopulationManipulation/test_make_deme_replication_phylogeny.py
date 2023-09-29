import os

from AvidaScripts.GenericScripts.PopulationManipulation import (
    load_deme_replication_dataframe,
    make_deme_replication_phylogeny,
)


def test_make_deme_replication_phylogeny():
    path = f"{os.path.dirname(__file__)}/assets/deme_replication.dat"
    df = load_deme_replication_dataframe(path)

    res = make_deme_replication_phylogeny(df)

    num_geneses = len({*df["Source Deme ID"], *df["Target Deme ID"]})
    assert len(res) == len(df) + num_geneses

    for id in res["id"]:
        source_deme_id = res.loc[res["id"] == id, "Source Deme ID"].squeeze()

        ancestor_id = res.loc[res["id"] == id, "ancestor_id"].squeeze()
        ancestor_mask = res["id"] == ancestor_id
        ancestor_deme_id = res.loc[ancestor_mask, "Target Deme ID"].squeeze()

        assert source_deme_id == ancestor_deme_id

    assert all(res["creation_time"] < res["destruction_time"])
    assert all(res["creation_time"] == res["Update"])
