from espy.media.epubMedia import epubMedia
import pandas as pd
from espy.processing.Dictionary import Dictionary
from espy.processing.cleaner import *
from pprint import pprint
from espy.vocab.ankiBuilder import build_deck
from espy.vocab.vocabBuilder import VocabInfo, VocabInfos, user_process_vocab
from espy.vocab.vocabStatus import DEFAULT_CSV_PATH, VocabStatus
import numpy as np

SPANISH_DICTIONARY = Dictionary()

EPUBS = [
    "./espy/resources/epubs/Sofía Segovia - El murmullo de las abejas.epub",
    "./espy/resources/epubs/Mariana Enríquez - Las cosas que perdimos en el fuego.epub",
    "./espy/resources/epubs/Marquez, Gabriel Garcia - Cien años de soledad.epub",
    "./espy/resources/epubs/Quentin Tarantino - Érase una vez en Hollywood.epub",
    "./espy/resources/epubs/Sanderson, Brandon - El Imperio Final.epub",
]

vpub = epubMedia(EPUBS[4])
pprint({e: len("\n\n".join(epubMedia(e).get_docs_text())) for e in EPUBS})
print("Chapter Lengths: ")
pprint({i:len(s) for i,s in enumerate(vpub.get_docs_text())})
all_text = "\n\n".join(vpub.get_docs_text())
# token_dict = get_vocab(all_text, min_occurences=2)

vs = VocabStatus(csv_path=DEFAULT_CSV_PATH)


# vocab_dict = get_vocab("\n\n".join(vpub.get_docs_text()[2:]), min_occurences=1, vocab_status=vs)
#vocab_dict = get_vocab(vpub.get_docs_text()[4], min_occurences=1, vocab_status=vs)

vocab_dict = get_vocab(vpub.get_docs_text()[7], min_occurences=1, check_real = False)
vocab_dict = sort_vocabs_by_occurence(vocab_dict, all_text)

print("Non words:", len([k for k in vocab_dict if k not in SPANISH_DICTIONARY]))

vs = VocabStatus()
#vs.user_process_words(vocab_dict)

vocab_infos = VocabInfos()


#user_process_vocab(vocab_infos, vocab_dict, corpus=all_text)
deck_id = 2059400110
build_deck(deck_id, "Espanol::Mistborn Vocab", vocab_infos)

# print([len(x) for x in vocab_dicts])
print("Done.")
