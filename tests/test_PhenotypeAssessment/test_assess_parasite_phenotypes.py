from AvidaScripts.GenericScripts.GenomeManipulation import (
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    assess_parasite_phenotypes,
    get_named_environment_content,
)


def test_assess_parasite_phenotypes():
    environment_content = get_named_environment_content("top25")
    instset_content = get_named_instset_content("transsmt")

    sequences = [
        # inviable
        "aaa",
        # zero traits
        "ycdAoaxccccypqvcrFaddxab",
        # one trait
        "ycdAoaxccctccEEEccccccccccgccccccccccccccccccEcccccccccccccccccccypqvcrFaddxab",
        # three traits
        "ycAEFlocEcxccwcgegEtgECgEypqvcsxFueFa",
        # three traits
        "yciiAsowbCiDocEEcxcgcwcjEcgiEujwcCcgjCEypqvcrFxqna",
    ]

    phenotype_df = assess_parasite_phenotypes(
        sequences,
        environment_content,
        instset_content,
    )
    assert len(phenotype_df) == 5

    assert phenotype_df["Viable"].tolist() == [0, 1, 1, 1, 1]
    assert phenotype_df["Num Traits"].tolist() == [0, 0, 1, 3, 3]
    assert phenotype_df["Genome Sequence"].tolist() == sequences

    assert phenotype_df["Phenotype"].iloc[0] == "inviable"
    assert (phenotype_df["Phenotype"].iloc[1:].str.len() == 25).all()
    assert phenotype_df["Phenotype"].iloc[1].count("0") == 25
    assert phenotype_df["Phenotype"].iloc[1].count("1") == 0
    assert phenotype_df["Phenotype"].iloc[2].count("0") == 24
    assert phenotype_df["Phenotype"].iloc[2].count("1") == 1
    assert (phenotype_df["Phenotype"].iloc[3:].str.count("0") == 22).all()
    assert (phenotype_df["Phenotype"].iloc[3:].str.count("1") == 3).all()
