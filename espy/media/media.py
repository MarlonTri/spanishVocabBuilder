import re
from enum import Enum
from collections import Counter


class TextClean(Enum):
    LOWER = lambda x: x.lower()


class Media(object):
    def __init__(self):
        raise NotImplementedError()

    def get_text(self, txt_clean_funcs=TextClean.LOWER):
        raise NotImplementedError()

    def get_vocab(self, sum_vocab=False, **kwargs):
        docs_text = self.get_docs_text(**kwargs)
        vocabs = []
        for doc_text in docs_text:
            words = re.findall(r"(\w+)", doc_text, re.UNICODE)
            vocab = Counter(words)
            vocabs.append(vocab)

        if sum_vocab:
            return sum(vocab, start=Counter())

        return vocabs
