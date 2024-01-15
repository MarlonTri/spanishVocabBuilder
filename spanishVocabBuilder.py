import ebooklib
from ebooklib import epub
import re
from collections import Counter
import readchar
from copy import deepcopy as copy
import random
from vocab_epub import VocabEpub
from word_intelligence import SpanishDictionary, VocabStatus

with open("known_words.txt") as file:
    KNOWN_WORDS = file.readlines()
KNOWN_WORDS = set([line.rstrip() for line in KNOWN_WORDS])

with open("spanish_words.txt") as file:
    SPANISH_WORDS = file.readlines()
SPANISH_WORDS = [line.rstrip() for line in SPANISH_WORDS]

EPUBS = [
    "epubs/Sofía Segovia - El murmullo de las abejas.epub",
    "epubs/Mariana Enríquez - Las cosas que perdimos en el fuego.epub",
    "epubs/Marquez, Gabriel Garcia - Cien años de soledad.epub",
    "epubs/Quentin Tarantino - Érase una vez en Hollywood.epub",
]


KNOWN_BUFFER = []
MAX_BUF_SIZE = 10


def add_known_word(word):
    global KNOWN_BUFFER
    KNOWN_BUFFER.append(word)
    if len(KNOWN_BUFFER) > MAX_BUF_SIZE:
        save_known_buf()
        KNOWN_BUFFER = []


def save_known_buf():
    global KNOWN_WORDS
    KNOWN_WORDS = KNOWN_WORDS.union(KNOWN_BUFFER)
    with open("known_words.txt", "w") as f:
        f.write("\n".join(KNOWN_WORDS))


def user_select_words(words, vocab_status: VocabStatus):
    selected = []
    print()
    print("Beginning word selection.")
    for word in words:
        if vocab_status.is_seen(word):
            continue
        print(f"{word}:", end="")
        c = repr(readchar.readchar()).strip("'")
        if c == "k":            
            print(f" ({c}) set to Known!")
            vocab_status.set_known(word, True)
        else:
            selected.append(word)
            print(f" ({c}) set to Unknown")
            add_known_word(word)
            vocab_status.set_known(word, False)
    return selected


vpub = VocabEpub(EPUBS[3])
vocabs = vpub.get_docs_vocab()
sd = SpanishDictionary()
filtered_vocab = sd.filter(vocabs[1])
vs = VocabStatus("stored.csv")

out = user_select_words(list(filtered_vocab)[:10], vs)

print()
