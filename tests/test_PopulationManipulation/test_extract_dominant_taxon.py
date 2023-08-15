import os

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
