import os

from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    get_named_environment_content,
    load_phenotype_dataframe,
)


def test_load_phenotype_dataframe():
    environment_content = get_named_environment_content("top25")
    df_path = f"{os.path.dirname(__file__)}/assets/phenotype.dat"
    phenotype_df = load_phenotype_dataframe(df_path, environment_content)
    assert len(phenotype_df) == 2
    assert phenotype_df.iloc[0].equals(phenotype_df.iloc[1])

    assert not phenotype_df["Trait 0"].any()
    assert phenotype_df["Trait 1"].all()
    assert (phenotype_df["Num Traits"] == 1).all()

    assert not phenotype_df["Task NAND"].any()
    assert phenotype_df["Task NOT"].all()

    assert (phenotype_df["Phenotype"].str.len() == 25).all()
    assert (phenotype_df["Phenotype"].str.count("0") == 24).all()
    assert (phenotype_df["Phenotype"].str.count("1") == 1).all()
