def count_instset_insts(instset_content: str) -> str:
    """Count number of instructions defined in instruction set."""
    return instset_content.count("INST ")
