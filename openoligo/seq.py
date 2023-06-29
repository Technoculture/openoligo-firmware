"""
Sequence class for DNA, RNA and modified Nucleic Acid sequences.
"""
import re


def is_valid_dna(sequence):
    pattern = r"^[ATCGatcg]*$"
    if re.match(pattern, sequence):
        return True
    return False


class Seq:
    def __init__(self, seq: str):
        self.seq = seq.upper()
        if not is_valid_dna(self.seq):
            raise ValueError("Invalid DNA sequence")
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.seq):
            raise StopIteration
        base = self.seq[self.index]
        self.index += 1
        return base
