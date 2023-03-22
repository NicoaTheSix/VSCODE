from typing import TYPE_CHECKING
from pathlib import Path
import re
import os
import zlib

import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix, save_npz, load_npz

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from tqdm.notebook import tqdm
from matplotlib import pyplot as plt
import seaborn as sns
import joblib

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from sklearn.base import ClassifierMixin
classes = ("Ramnit", "Lollipop", "Kelihos_ver3", "Vundo", "Simda", "Tracur", "Kelihos_ver1", "Obfuscator.ACY", "Gatak")
# Data directory.
data_dir = Path("data")

# Statistic directory.
stats_dir = Path("stats")

# Sample directory.
smp_dir = data_dir.joinpath("samples")

# Feature directories.
ftr_dir = Path("pre-extract")
if not ftr_dir.exists():
    ftr_dir.mkdir()
class Read:
    """
    Read different kinds of content from a sample file.
    """
    @staticmethod
    def bytes(id: str) -> list[str]:
        """
        Read a sample's byte content.
        """
        with smp_dir.joinpath(id + ".bytes").open() as file:
            data = file.read()
        items = data.split()
        byte_list = []
        for item in items:
            if len(item) == 2 and item != "??":
                byte_list.append(item)
        return byte_list

    @staticmethod
    def asm(id: str) -> str:
        """
        Read a sample's disassembly content as a large string.
        """
        with smp_dir.joinpath(id + ".asm").open(encoding="utf-8", errors="ignore") as file:
            return file.read()

    @staticmethod
    def asm_lines(id: str) -> list[str]:
        """
        Read a sample's disassembly content as a list of lines.
        """
        with smp_dir.joinpath(id + ".asm").open(encoding="utf-8", errors="ignore") as file:
            return file.readlines()
class CSVFeature:
    """
    Manage the saving and loading of a `.csv` feature file.
    """
    def __init__(self, file: str) -> None:
        """
        The constructor.

        -- PARAMETERS --
        file: A `.csv` file name.
        """
        self.file: str = file

    def save(self, data: pd.DataFrame) -> None:
        """
        Save a dataframe into a `.csv` file.

        -- PARAMETERS --
        data: A dataframe.
        """
        data.to_csv(ftr_dir.joinpath(self.file))

    def load(self) -> pd.DataFrame | None:
        """
        Load a dataframe from a `.csv` file.

        -- RETURNS --
        A dataframe or `None` if the file does not exist.
        """
        path = ftr_dir.joinpath(self.file)
        return pd.read_csv(path).set_index("ID") if path.exists() else None
class NpzFeature:
    """
    Manage the loading of a `.npz` feature file.
    """
    def __init__(self, file: str) -> None:
        """
        The constructor.

        -- PARAMETERS --
        file: A `.npz` file name.
        """
        self.file: str = file

    def load(self) -> pd.DataFrame | None:
        """
        Load a dataframe from a `.csv` file.

        -- RETURNS --
        A dataframe or `None` if the file does not exist.
        """
        path = ftr_dir.joinpath(self.file)
        return pd.DataFrame(load_npz(path).toarray()) if path.exists() else None
class List:
    """
    Manage the saving and loading of a list file.
    """
    Sequence=[]
    def __init__(self, file: str) -> None:
        """
        The constructor.

        -- PARAMETERS --
        file: A list file name.
        """
    def save(self, data) -> None:
        """
        Save a sequence into a list file.

        -- PARAMETERS --
        data: A list.
        """
        path = ftr_dir.joinpath(self.file)
        with path.open("w", encoding="utf-8") as file:
            for line in data:
                file.write(f"{str(line)}\n")

    def load(self) -> list[str] | None:
        """
        Load a sequence from a list file.

        -- RETURNS --
        A list or `None` if the file does not exist.
        """
        path = ftr_dir.joinpath(self.file)
        if path.exists():
            with path.open(encoding="utf-8") as file:
                return file.read().splitlines("\n")
        else:
            return None
lbls = pd.read_csv(data_dir.joinpath("labels.csv"))
lbls["ID"] = lbls["ID"].astype(str)
lbls["Class"] = lbls["Class"].astype("category")
lbls.set_index("ID", inplace=True)
def show_class_distribution(lbls: pd.DataFrame, title: str) -> None:
    """
    Show samples' class distribution.

    -- PARAMETERS --
    lbls: A label dataframe having `Class` column.
    title: The figure title.
    """
    nums = lbls["Class"].value_counts().sort_index()
    ax = sns.barplot(x=nums.index, y=nums.values)
    ax.set(xlabel="Class", ylabel="Number of Samples", title=title)
    plt.show()
def show_feature_importances(names: Sequence[str], vals: Sequence[float], title: str, figsize: tuple[int, int] = (8, 5)) -> None:
    """
    Show feature importances.

    -- PARAMETERS --
    names: Feature names.
    vals: Feature importances.
    title: The figure title.
    figsize: The figure size.
    """
    plt.figure(figsize=figsize)
    ax = sns.barplot(x=vals, y=names)
    ax.set(xlabel="Importance", ylabel="Feature", title=title)
    plt.show()
def show_1d_distribution(X: pd.DataFrame, x: str, xlabel: str, title: str, figsize: tuple[int, int] = (8, 5)) -> None:
    """
    Show the distribution of two variables.

    -- PARAMETERS --
    data: A dataframe.
    x: A column name shown on the X-axis.
    xlabel: The X-axis label.
    title: The figure title.
    figsize: The figure size.
    """
    plt.figure(figsize=figsize)
    x_lim = (0, X[x].mean() + X[x].std() * 3)
    ax = sns.boxplot(y="Class", x=x, data=X.assign(Class=lbls["Class"]))
    ax.set(xlim=x_lim, xlabel=xlabel, title=title)
    plt.show()
def show_2d_distribution(X: pd.DataFrame, x: str, y: str, xlabel: str, ylabel: str, title: str, figsize: tuple[int, int] = (8, 5)) -> None:
    """
    Show the distribution of two variables.

    -- PARAMETERS --
    X: A dataframe.
    x: A column name shown on the X-axis.
    y: A column name shown on the Y-axis.
    xlabel: The X-axis label.
    ylabel: The Y-axis label.
    title: The figure title.
    figsize: The figure size.
    """
    plt.figure(figsize=figsize)
    x_lim = (0, X[x].mean() + X[x].std() * 3)
    y_lim = (0, X[y].mean() + X[y].std() * 3)

    # Create a temporary dataframe containing the class column with the `assign` method.
    ax = sns.scatterplot(x=x, y=y, hue="Class", data=X.assign(Class=lbls["Class"]))
    ax.set(xlim=x_lim, ylim=y_lim, xlabel=xlabel, ylabel=ylabel, title=title)
    ax.legend(loc="upper right", title="Class")
    plt.show()
if TYPE_CHECKING:
    SeqReader = Callable[[str], str]

def extract_ngrams(ids: Sequence[str], seq_reader: SeqReader, n: int) -> tuple[CountVectorizer, csr_matrix]:
    """
    Extract samples' n-grams.

    -- PARAMETERS --
    ids: Sample IDs.
    seq_reader: A callback function used to extract a sequence content from a sample.
    n: The N value.

    -- RETURNS --
    A fitted `CountVectorizer` model.
    A sparse count matrix.
    """
    class Reader:
        """
        A wrapper for file-like input of `CountVectorizer`.
        """
        def __init__(self, id: str) -> None:
            self._id: str = id

        def read(self) -> str:
            return seq_reader(self._id)

    seqs = [Reader(id) for id in ids]
    # Name mangling should be considered, `token_pattern` cannot be the default.
    ngrm_vct = CountVectorizer(ngram_range=(n, n), stop_words=None, token_pattern=r"(?u)\b[\w@?]{2,}\b", lowercase=False, input="file")
    ngrms = ngrm_vct.fit_transform(seqs)
    return ngrm_vct, ngrms
def extract_file_sizes(ids: Sequence[str]) -> pd.DataFrame:
    """
    Extract samples' file sizes:

    -- PARAMETERS --
    ids: Sample IDs.

    -- RETURNS --
    A dataframe having the following columns:
      - The disassembly size.
      - The byte size.
      - The ratio of the disassembly size and byte size.
    """
    df = pd.DataFrame(columns=["ID", "Asm-Size", "Byte-Size", "Ratio"], dtype=float).set_index("ID")
    for id in tqdm(ids):
        df.at[id, "Asm-Size"] = os.path.getsize(smp_dir.joinpath(id + ".asm"))
        df.at[id, "Byte-Size"] = os.path.getsize(smp_dir.joinpath(id + ".bytes"))

    df[["Asm-Size", "Byte-Size"]] = df[["Asm-Size", "Byte-Size"]].astype(int)
    df["Ratio"] = (df["Asm-Size"] / df["Byte-Size"]).round(5)
    return df