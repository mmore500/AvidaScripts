"""
A class used to manipulate Avida genomes. 

"""

import gzip
import sys
import copy
import random
import os
import csv
import typing
from numpy import loadtxt, mean

from ..auxlib import get_avida_char_seq_val

__author__ = """Luis Zaman (luis.zaman@gmail.com)"""

class GenomeManipulator:
    """
    A class built to manipulate Avida genomes in various ways including 
    generating different types of mutations, converting genomes (list of 
    instructions) to sequences (string of letters representing instructions),
    and sequences to genomes.
    
    """
    
    def __init__(self, inst_set_path):
        """Initialize a GenomeManipulator object with a particular inst_set.
        
        Parameters
        ----------
        inst_set_path : path to instruction set file
            This instruction set file contains the definition and 
            configuration of instructions that may be used by
            Avida organisms in their genome.
        
        """
        self.inst_hash = {} #hash from instruction string to sequence char
        self.rev_inst_hash = {} #hash from sequence char to instruction string
        self.char_lookup = [] #list of characters used as shorthand

        try:
            inst_file = open(inst_set_path)
        except IOError as e:
            print("Cannot open instruction set file")
            raise
            
        inst_contents = inst_file.read()
        inst_file.close()
        inst_data =  [i.strip().split(' ')[1].strip() 
            for i in inst_contents.split('\n') if len(i) > 1 and 
            i[0] != "#" and (not i.startswith("INSTSET"))]

        for i in range(len(inst_data)):
            inst_char = get_avida_char_seq_val(i)
            self.char_lookup.append(inst_char)

        assert len(self.char_lookup) == len(inst_data), (
            len(self.char_lookup), len(inst_data)
        )

        for i in range(len(inst_data)):
        	self.inst_hash[self.char_lookup[i]] = inst_data[i]
        	self.rev_inst_hash[inst_data[i]] = self.char_lookup[i]

        assert (
            len(inst_data)
            == len(self.inst_hash)
            == len(self.rev_inst_hash)
            == len(self.char_lookup)
        )

    def extend_instset_for_hostification(self) -> None:
        assert len(self.inst_hash) == len(self.rev_inst_hash)
        for addend in "Divide", "Nop-X":
            if addend not in self.rev_inst_hash:
                char_num = len(self.rev_inst_hash)
                assert char_num
                addend_char = get_avida_char_seq_val(char_num)
                self.rev_inst_hash[addend] = addend_char
                self.char_lookup.append(addend_char)
                assert addend_char not in self.inst_hash
                self.inst_hash[addend_char] = addend

        assert len(self.inst_hash) == len(self.rev_inst_hash)

    def needs_instset_extension_for_hostification(self) -> bool:
        lookup = self.rev_inst_hash
        return not ("Divide" in lookup and "Nop-X" in lookup)

    def genome_to_sequence(self, genome):
        """Convert a list of instructions into a sequence of chars
        
        Parameters
        ----------
        genome :  list of instructions
            The genome is a list of instructions from the instruction set 
            used in the creation of this class, and is case sensitive.
            
        """
        return [self.rev_inst_hash[g] for g in genome]
  
    def sequence_to_genome(self, sequence):
        """Convert a sequence of chars into a list of instructions
        
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """

        return [self.inst_hash[s] for s in sequence]

    def hostify_parasite_sequence(self, sequence: str) -> typing.List[str]:
        """Replace inject instructions with divide instructions to convert
        viable parasite to viable host.

        Makes parasite genomes compatible with Avida analysis mode,
        """
        assert not self.needs_instset_extension_for_hostification()

        inst_lookup = self.rev_inst_hash
        inject_char = inst_lookup["Inject"]
        divide_char = inst_lookup["Divide"]
        divide_erase_char = inst_lookup.get(
            "Divide-Erase",
            "-".join(sequence),  # fallback guaranteed never in sequence
        )
        nop_x_char = inst_lookup["Nop-X"]

        return [
            inst.replace(
                divide_erase_char, nop_x_char  # noqa fmt
            ).replace(
                divide_char, nop_x_char  # noqa fmt
            ).replace(
                inject_char, divide_char  # noqa fmt
            )
            for inst in sequence
        ]

    def hostify_parasite_genome(
        self,
        genome: typing.List[str],
    ) -> typing.List[str]:
        """Replace inject instructions with divide instructions to convert
        viable parasite to viable host.

        Makes parasite genomes compatible with Avida analysis mode,
        """
        assert not self.needs_instset_extension_for_hostification()

        return [
            inst.replace(
                "Divide-Erase", "Nop-X"  # noqa fmt
            ).replace(
                "Divide", "Nop-X"  # noqa fmt
            ).replace(
                "Inject", "Divide"  # noqa fmt
            )
            for inst in genome
         ]

    def generate_all_insertion_mutants(self, sequence):
        """Return a list of sequences with all possible insertion mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """
        ancestor_sequence = list(sequence)
        all_insertion_mutants = []
  
        #make all insertions, (+1 for insertion off the last instruction)
        for i in range(len(sequence) + 1):
            for new_char in self.char_lookup:
                new_seq = list(ancestor_sequence)
                new_seq.insert(i, new_char)
                all_insertion_mutants.append(''.join(new_seq))
                
        return all_insertion_mutants
        
    def generate_all_deletion_mutants(self, sequence):
        """Return a list of sequences with all possible deletion mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """
        ancestor_sequence = list(sequence)
        all_deletion_mutants = []
  
        #deletions
        for i in range(len(sequence)):
            new_seq = list(ancestor_sequence)
            new_seq.pop(i)
            all_deletion_mutants.append(''.join(new_seq))
            
        return all_deletion_mutants
    
    def generate_all_point_mutants(self, sequence):
        """Return a list of sequences with all possible point mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """
        ancestor_sequence = list(sequence)
        all_point_mutants = []
  
        #and point mutations
        for i in range(len(sequence)):
            for new_char in self.char_lookup:
                new_seq = list(ancestor_sequence)
          
                #avoid calling ancestral state a "mutant"
                if new_seq[i] != new_char:
                    new_seq[i] = new_char
                    all_point_mutants.append(''.join(new_seq))
                    
        return all_point_mutants
  
    def generate_all_mutants(self, sequence):
        """Return a list of sequences with all possible mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """

        return(self.generate_all_deletion_mutants(sequence)
            + self.generate_all_insertion_mutants(sequence) 
            + self.generate_all_point_mutants(sequence))
