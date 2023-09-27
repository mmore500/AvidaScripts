import os

import pytest

from AvidaScripts.GenericScripts.PopulationManipulation import (
    extract_dominant_taxon,
    load_population_dataframe,
)


def test_extract_dominant_taxon_host():
    pop_path = f"{os.path.dirname(__file__)}/assets/example-host-parasite.spop"
    pop_df = load_population_dataframe(pop_path)

    dominant_taxon_dict = extract_dominant_taxon(pop_df, "host")
    assert dominant_taxon_dict["role"] == "host"

    host_pop_df = pop_df[pop_df["is host"]]
    # check data is nontrivial
    assert host_pop_df["Number of currently living organisms"].nunique() > 1

    assert (
        dominant_taxon_dict["Number of currently living organisms"]
        == host_pop_df["Number of currently living organisms"].max()
    )


def test_extract_dominant_taxon_parasite():
    pop_path = f"{os.path.dirname(__file__)}/assets/example-host-parasite.spop"
    pop_df = load_population_dataframe(pop_path)

    dominant_taxon_dict = extract_dominant_taxon(pop_df, "parasite")
    assert dominant_taxon_dict["role"] == "parasite"

    parasite_pop_df = pop_df[pop_df["is parasite"]]
    # check data is nontrivial
    assert parasite_pop_df["Number of currently living organisms"].nunique() > 1

    assert (
        dominant_taxon_dict["Number of currently living organisms"]
        == parasite_pop_df["Number of currently living organisms"].max()
    )


@pytest.mark.parametrize("role", ["host", "parasite"])
def test_extract_dominant_taxon_exclude_monolithic_parasite(role: str):
    pop_path = f"{os.path.dirname(__file__)}/assets/monolithic-host-parasite.spop"
    pop_df = load_population_dataframe(pop_path)

    for exclude_monolithic in True, False:
        dominant_taxon_dict = extract_dominant_taxon(
            pop_df,
            role,
            exclude_monolithic=exclude_monolithic,
        )
        assert dominant_taxon_dict["role"] == role
        if exclude_monolithic:
            assert len(set(dominant_taxon_dict["Genome Sequence"])) > 1
        else:
            assert len(set(dominant_taxon_dict["Genome Sequence"])) == 1
