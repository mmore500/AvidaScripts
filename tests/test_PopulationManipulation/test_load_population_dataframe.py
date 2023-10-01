import os

import pytest

from AvidaScripts.GenericScripts.PopulationManipulation import (
    load_population_dataframe,
)


@pytest.mark.parametrize(
    "filename",
    ["example-host-parasite.spop", "example-host-parasite-bad.spop"],
)
def test_load_population_dataframe(filename: str):
    pop_path = f"{os.path.dirname(__file__)}/assets/{filename}"
    res = load_population_dataframe(pop_path)

    assert res.iloc[0].to_dict() == {
        "ID": 89769,  # row  1
        "Source": "div:int",  # row  2
        "Source Args": "(none)",  # row  3
        "Parent ID(s)": "58425",  # row  4
        "Number of currently living organisms": 1,  # row  5
        "Total number of organisms that ever existed": 13,  # row  6
        "Genome Length": 320,  # row  7
        "Average Merit": 305.733,  # row  8
        "Average Gestation Time": 1839.73,  # row  9
        "Average Fitness": 0.166183,  # row 10
        "Generation Born": 59,  # row 11
        "Update Born": 4429,  # row 12
        "Update Deactivated": -1,  # row 13
        "Phylogenetic Depth": 7,  # row 14
        "Hardware Type ID": 2,  # row 15
        "Inst Set Name": "transsmt",  # row 16
        "Genome Sequence": "ycdBCiEdimFjfCDaknmsAjemEEcgccgssmhEDcsdseDcAcBcggclEEcDEgcvysAmlzessjhcdcggkhamtmciEEvjDdhjidziAyndvmEdboznjDmcjohohooayaxdyalboekzebjcogEtjgjacblDvubADnslyyocgsAcjCbobffhmvnnAdbDfkmxcagBFfnqytqhutjdzfdjsnflfoqCwcvhsjcvbmlsqcjrgyiDivvnFhrArcsmifbClvluDqmCBbtiDhiEfACcarpmczijdljujACbfzuDEFyaqqekizDosbbzjgmpczypqvcrGxab",  # row 17
        "Occupied Cell IDs": "1245",  # row 18
        "is host": True,  # from additional postprocessing
        "is parasite": False,  # from additional postprocessing
        "role": "host",  # from additional postprocessing
    }

    assert not res.iloc[-1]["is host"]
    assert res.iloc[-1]["is parasite"]
    assert res.iloc[-1]["role"] == "parasite"
