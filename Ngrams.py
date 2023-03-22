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

SeqReader = Callable[[str], str]
Sequence=[]
def extract_ngrams(ids, seq_reader: SeqReader, n: int) -> tuple[CountVectorizer, csr_matrix]:
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
