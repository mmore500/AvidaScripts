import math


def calc_num_twostep_pointmuts(num_sites: int, num_insts: int) -> int:
    num_distinct_site_pairs = math.comb(num_sites, 2)
    num_mutated_char_pairs = (num_insts - 1) ** 2
    return num_distinct_site_pairs * num_mutated_char_pairs
