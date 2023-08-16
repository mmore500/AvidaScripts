import os
from pathlib import Path

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    get_named_instset_content,
    make_named_instset_path,
)
from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    assess_phenotypes,
    get_named_environment_content,
)


def test_assess_phenotypes():
    environment_content = get_named_environment_content("top25")
    instset_content = get_named_instset_content("transsmt")

    genome_text = Path(
        f"{os.path.dirname(__file__)}/assets/host-smt.org",
    ).read_text()
    genome_list = genome_text.rstrip().split("\n")

    gm = GenomeManipulator(make_named_instset_path("transsmt"))
    sequence = "".join(gm.genome_to_sequence(genome_list))

    phenotype_df = assess_phenotypes(
        [sequence] * 2,
        environment_content,
        instset_content,
    )
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
