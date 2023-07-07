"""
Sequence class for DNA, RNA and modified Nucleic Acid sequences.
"""
import re
from enum import Enum


def is_valid_dna(sequence):
    """
    Check if a sequence is a valid DNA sequence.
    """
    pattern = r"^[ATCGatcg]*$"
    if re.match(pattern, sequence):
        return True
    return False


class Phosphoramidite(Enum):
    """All available Phosphoramidites."""

    A = "A"
    T = "T"
    G = "G"
    C = "C"
    U = "U"
    M5C = "5mC"
    GALNAC = "-GalNAc"


phosphoramidite_dict = {
    "A": "Adenosine",
    "T": "Thymidine",
    "G": "Guanosine",
    "C": "Cytidine",
    "U": "Uridine",
    "5mC": "5-Methylcytidine",
    "GalNAc": "N-Acetylgalactosamine",
}


# def parse_sequence(sequence: str) -> list[Phosphoramidite]:
#    """
#    Given a sequence in str, return a list of Phosphoramidite in the correct order.
#
#    Example:
#        AAT5mC5mCAT5mC-GalNAc -> [A, A, T, M5C, M5C, A, T, M5C, GALNAC]
#    """


def parse_sequence(sequence: str) -> list[Phosphoramidite]:
    """
    Given a sequence in str, return a list of Phosphoramidite in the correct order.

    Example:
        AAT5mC5mCAT5mC-GalNAc -> [A, A, T, M5C, M5C, A, T, M5C, GALNAC]
    """
    parsed_sequence = []
    buffer = ""
    for char in sequence:
        buffer += char
        if buffer in Phosphoramidite.__members__:
            parsed_sequence.append(Phosphoramidite[buffer])
            buffer = ""
    if buffer:
        raise ValueError(f"Invalid sequence: {buffer}")
    return parsed_sequence


class Seq:
    """
    Representation of the sequence as a string.
    """

    def __init__(self, seq: str) -> None:
        """
        Initialize the sequence.
        """
        self.seq = seq.upper()
        if not is_valid_dna(self.seq):
            raise ValueError("Invalid DNA sequence")
        self.index = 0

    def __iter__(self):
        """
        Allows iteration over the sequence.
        """
        return self

    def __next__(self) -> str:
        """
        Returns the next base in the sequence.

        raises:
            StopIteration: if the end of the sequence is reached.
        """
        if self.index < len(self.seq):
            result = self.seq[self.index]
            self.index += 1
            return result
        raise StopIteration

    def __repr__(self) -> str:
        """
        Returns string representation of the sequence.
        """
        return self.seq

    def __len__(self) -> int:
        """
        get the length of the sequence.
        """
        return len(self.seq)

    def __getitem__(self, key) -> str:
        """
        Allows indexing of the sequence.
        """
        return self.seq[key]

    def reverse_complement(self) -> "Seq":
        """Return the reverse complement of the input sequence"""
        complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
        return Seq("".join([complement[base] for base in self.seq[::-1]]))


class SeqCategory(str, Enum):
    """
    Enum for the different sequence categories.
    """

    DNA = "DNA"
    RNA = "RNA"
    MODIFIED = "MODIFIED"
