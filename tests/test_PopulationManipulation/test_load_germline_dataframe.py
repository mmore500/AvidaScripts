import os

from AvidaScripts.GenericScripts.PopulationManipulation import (
    load_germline_dataframe,
)


def test_load_germline_dataframe():
    pop_path = f"{os.path.dirname(__file__)}/assets/detailgermlines-5000.sgerm"
    res = load_germline_dataframe(pop_path)

    assert len(res) == 40
    assert res.iloc[0].to_dict() == {
        "Deme ID": 0,
        "Hardware Type ID": 2,
        "Inst Set Name": "transsmt",
        "Genome Sequence": "ycdBCiEdimFjfCDaknmsAjemEEcgccgssmhEEcsdseDcAcBcggclEEcDEgcvrsAmlzessjhcdcggkhamtmciEEvjDdhjidzoAyndvmEdbgznjDmcjohohooayaxdyalbcekzebjcogEtjgjacblDvubADnslyyocgsAcjCbobffhmvnnAdbDfkmxcagBFfndytqhutjdzfdjsnflfoqCwcvhsjcvbmlsqcjrgyiDivvnFhrArcsmifbClvluDqmCBbtiDhiEfACcarpEczijdljujACbfzuDEFyaqqekizDosbbzjgmpczypqvcrGxab",
    }
    assert res.iloc[-1].to_dict() == {
        "Deme ID": 39,
        "Hardware Type ID": 2,
        "Inst Set Name": "transsmt",
        "Genome Sequence": "ycdBCiEdimFjfCDaknmsAjemEEcgccgssmhEEcsdseDcAcBcggclEEcDEgcvrsAmlzessjhcdcggkhamtmciEEvjDdhjidzoAyndvmEdbgznjDmcjohohooayaxdyalbcekzebjcogEtjgjacblDvubADnslyyocgsAcjCbobffhmvnnAdbDfkmxcagBFfndytqhutjdzfdjsnflfoqCwcvhsjcvbmlsqcjrgyiDivvnFhrArcsmifbClvluDqmCBbtiDhiEfACcarpEczijdljujACbfzuDEFyaqqekizDosbbzjgmpczypqvcrGxab",
    }
