import numpy as np
from copy import deepcopy
import pandas as pd
from collections import Counter
import os


class SpanishDictionary(object):
    def __init__(self, csv_path="spanish_dictionary.csv"):
        self.df = pd.read_csv(csv_path)
        self.vocab_set = set(self.df["Spanish Word"])
        self.remove_dups()

    def remove_dups(self):
        self.df.sort_values("Prevalence", inplace=True)
        self.df.drop_duplicates(subset=["Spanish Word"], inplace=True)
        self.df.sort_values("Spanish Word", inplace=True)

    def filter(self, vocab_dict):
        return {k: v for k, v in vocab_dict.items() if k in self.vocab_set}


class VocabStatus(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path

        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
        else:
            self.df = pd.DataFrame(columns=["Word", "Known"])

    def is_seen(self, word):
        if word not in self.df["Word"]:
            return False
        assert len(self.df["Word"] == word) == 1
        return True
    def is_known(self, word):
        if not self.is_seen(word):
            return False
        return self.df[self.df["Word"] == word]["Known"]

    def save(self):
        self.df.to_csv(self.csv_path, encoding="utf-8", index=False)

    def set_known(self, word: str, known: bool):
        if self.is_seen(word):
            self.df[self.df["Word"] == word]["Known"] = known
        else:
            self.df.loc[len(self.df.index)] = [word, known]
