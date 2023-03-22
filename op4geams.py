import re
import pandas as pd
from typing import TYPE_CHECKING
from collections.abc import Callable, Sequence
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import os
import pathlib

ftr_dir = pathlib.Path("pre-extract")
# Data directory.
data_dir = pathlib.Path("data")

# Statistic directory.
stats_dir = pathlib.Path("stats")

# Sample directory.
smp_dir = data_dir.joinpath("samples")

lbls = pd.read_csv(data_dir.joinpath("labels.csv"))
lbls.set_index("Id", inplace=True)

if not ftr_dir.exists():
    ftr_dir.mkdir()
class Read():
    def asm():
        with open('0AnoOZDNbPXIr2MRBSCJ.asm',encoding="utf-8", errors="ignore") as file:
            return file.read()
    def asm_lines(id: str) -> list[str]:
         with open('0AnoOZDNbPXIr2MRBSCJ.asm',encoding="utf-8", errors="ignore") as file:
            return file.readlines()
class Section:
    """
    Save a section's attributions.
    """
    def __init__(self) -> None:
        self.name: str = ""
        self.virtual_size: int = 0
        self.raw_size: int = 0
        self.executable: bool = False
        self.writable: bool = False

    @staticmethod
    def load():
        """
        Extract a sample's section attributions.
        """
        asm = Read.asm()
        sctns = []
        for attr in call_rgx.findall(asm):
            sctn = Section()
            sctn.name, sctn.virtual_size, sctn.raw_size, access = attr[0].lower(), int(attr[1]), int(attr[2]), set(attr[3].split())
            if "Executable" in access:
                sctn.executable = True
            if "Writable" in access:
                sctn.writable = True
            sctns.append(sctn)
        return sctns
if TYPE_CHECKING:
    SeqReader = Callable[[str], str]


opcode_rgx = re.compile(r"\s[\dA-F]{2}(?:\+)?\s+([a-z]+)\s")
opcode_rgx.findall(Read.asm())

print(type(opcode_rgx.findall(Read.asm())))
print(list(opcode_rgx.findall(Read.asm())))
def extract_opcode_sequence():
    """
    Extract a sample's operation code sequence.

    -- PARAMETERS --
    id: A sample ID.

    -- RETURNS --
    An operation code sequence.
    """
    opcodes = []
    for line in Read.asm_lines():
        for opcode in opcode_rgx.findall(line):
            opcodes.append(opcode.lower())
    return " ".join(opcodes)
opcode_ngrm_vct, opcode_ngrms = extract_ngrams(lbls.index, extract_opcode_sequence, 4)
joblib.dump(opcode_ngrm_vct, ftr_dir.joinpath("opcode_4gram.joblib"))