import textwrap
import typing

import yaml


def get_named_instset_table() -> typing.Dict[str, str]:
    """Get dict mapping of all known instset names to their content."""
    raw_data = """
        transsmt: |
            INSTSET transsmt:hw_type=2
            INST Nop-A
            INST Nop-B
            INST Nop-C
            INST Nop-D
            INST Val-Shift-R
            INST Val-Shift-L
            INST Val-Nand
            INST Val-Add
            INST Val-Sub
            INST Val-Mult
            INST Val-Div
            INST Val-Mod
            INST Val-Inc
            INST Val-Dec
            INST SetMemory
            INST Inst-Read
            INST Inst-Write
            INST If-Equal
            INST If-Not-Equal
            INST If-Less
            INST If-Greater
            INST Head-Push
            INST Head-Pop
            INST Head-Move
            INST Search
            INST Push-Next
            INST Push-Prev
            INST Push-Comp
            INST Val-Delete
            INST Val-Copy
            INST IO
            INST Inject
            INST Divide-Erase
    """
    return yaml.safe_load(textwrap.dedent(raw_data))
