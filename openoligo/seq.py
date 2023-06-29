"""
Sequence class for DNA, RNA and modified Nucleic Acid sequences.
"""
import re


def is_valid_dna(sequence):
    """
    Check if a sequence is a valid DNA sequence.
    """
    pattern = r"^[ATCGatcg]*$"
    if re.match(pattern, sequence):
        return True
    return False


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
