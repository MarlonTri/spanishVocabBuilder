from espy.media.epubMedia import epubMedia
import spacy
from spacy import displacy
from collections import Counter
import pandas as pd
from espy.processing.cleaner import *
from pprint import pprint
from espy.vocab.vocabStatus import VocabStatus

EPUBS = [
    "./espy/resources/epubs/Sofía Segovia - El murmullo de las abejas.epub",
    "./espy/resources/epubs/Mariana Enríquez - Las cosas que perdimos en el fuego.epub",
    "./espy/resources/epubs/Marquez, Gabriel Garcia - Cien años de soledad.epub",
    "./espy/resources/epubs/Quentin Tarantino - Érase una vez en Hollywood.epub",
    "./espy/resources/epubs/Sanderson, Brandon - El Imperio Final.epub",
]

vpub = epubMedia(EPUBS[4])
pprint({e:len("\n\n".join(epubMedia(e).get_docs_text())) for e in EPUBS})
#all_text = "\n\n".join(vpub.get_docs_text())
#token_dict = get_vocab(all_text, min_occurences=2)

vs = VocabStatus()
#vs.user_process_words(token_dict)

token_dicts = get_chapter_vocab(vpub.get_docs_text(), min_occurences=2, vocab_status=vs)
#vs = VocabStatus()
#vs.user_process_words(token_dicts[2])

print([len(x) for x in token_dicts])
print("Done.")
