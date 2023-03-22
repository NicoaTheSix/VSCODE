import re
import pandas as pd
from typing import TYPE_CHECKING
from collections.abc import Callable, Sequence
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import tqdm
import zlib
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
    def asm_lines() :
         with open('0AnoOZDNbPXIr2MRBSCJ.asm',encoding="utf-8", errors="ignore") as file:
            return file.readlines()
    def bytes():
        """
        Read a sample's byte content.
        """
        
        with open('0AnoOZDNbPXIr2MRBSCJ.bytes') as file:
            data = file.read()
        items = data.split()
        byte_list = []
        for item in items:
            if len(item) == 2 and item != "??":
                byte_list.append(item)
        return byte_list

SeqReader = Callable[[str], str]    


df = pd.DataFrame(columns=["ID", "Asm-Len", "Zip-Asm-Len", "Asm-Zip-Ratio", "Byte-Len", "Zip-Byte-Len", "Byte-Zip-Ratio"], dtype=float).set_index("ID")
ids="0AnoOZDNbPXIr2MRBSCJ"
asm = Read.asm().encode("utf-8")
bytes = Read.bytes()
bytes = " ".join([str(byte) for byte in bytes]).encode("utf-8")
df.at[ids, "Asm-Len"] = len(asm)
df.at[ids, "Zip-Asm-Len"] = len(zlib.compress(asm))
df.at[ids, "Byte-Len"] = len(bytes)
df.at[ids, "Zip-Byte-Len"] = len(zlib.compress(bytes))

df[["Asm-Len", "Zip-Asm-Len", "Byte-Len", "Zip-Byte-Len"]] = df[["Asm-Len", "Zip-Asm-Len", "Byte-Len", "Zip-Byte-Len"]].astype(int)
df["Asm-Zip-Ratio"] = (df["Asm-Len"] / df["Zip-Asm-Len"]).round(5)
df["Byte-Zip-Ratio"] = (df["Byte-Len"] / df["Zip-Byte-Len"]).round(5)

print(df.at[ids, "Asm-Len"])
print(df.at[ids, "Zip-Asm-Len"])
print(df.at[ids, "Byte-Len"])
print(df.at[ids, "Zip-Byte-Len"])
print(df["Asm-Zip-Ratio"])
print(df["Byte-Zip-Ratio"])
print(df[["Asm-Len", "Zip-Asm-Len", "Byte-Len", "Zip-Byte-Len"]])