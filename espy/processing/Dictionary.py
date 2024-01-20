import unicodedata
import numpy as np
import pandas as pd

SPANISH_DICT_PATH1 = "./espy/resources/spanish_dictionary.csv"
SPANISH_DICT_PATH2 = "./espy/resources/spanish_dictionary2.csv"

ES_DICT1_WORDS = pd.read_csv(
    SPANISH_DICT_PATH1,
    encoding="utf-8",
    usecols=["Word"],
    dtype=np.dtype(str),
    na_filter=False,
)
ES_DICT2_WORDS = pd.read_csv(
    SPANISH_DICT_PATH2,
    encoding="utf-8",
    usecols=["Word"],
    dtype=np.dtype(str),
    na_filter=False,
)

ES_ALL_WORDS = set(ES_DICT1_WORDS["Word"]).union(ES_DICT2_WORDS["Word"])


def remove_accents(s):
    out = ""
    for c in s:
        if c == "ñ":
            out += c
        else:
            nc = unicodedata.normalize("NFD", c)
            for ncp in nc:
                if unicodedata.category(ncp) != "Mn":
                    out += ncp

    return out


class Dictionary(object):
    def __init__(self, split=True, symbols=True):
        self.split = split
        self.symbols = symbols

    def __contains__(self, word):
        if self.split:
            word = word.split(" ")[0]

        if self.symbols:
            return (word in ES_ALL_WORDS) or (remove_accents(word) in ES_ALL_WORDS)
        return word in ES_ALL_WORDS
