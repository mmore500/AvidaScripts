import os

from AvidaScripts.GenericScripts.PopulationManipulation import (
    load_population_dataframe,
)


def test_load_population_dataframe():
    pop_path = f"{os.path.dirname(__file__)}/assets/example-host-parasite.spop"
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
        "Gestation (CPU) Cycle Offsets": "0",  # row 19
        "Lineage Label": "0",  # row 20
    }
