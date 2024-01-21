# import spacy
from collections import Counter
from enum import Enum

from espy.processing.Dictionary import Dictionary
from espy.processing.token_cleaner import clean_token


class NLP_MODULE(Enum):
    SM = "es_core_news_sm"
    MD = "es_core_news_md"
    LG = "es_core_news_lg"
    TRF = "es_dep_news_trf"
    STANZA = "stanza"


nlp_module = NLP_MODULE.TRF

if nlp_module == NLP_MODULE.STANZA:
    import stanza
    import spacy_stanza

    stanza.download("es")
    ES_NLP = spacy_stanza.load_pipeline("es")
else:
    import spacy
    spacy.require_gpu() #TODO 
    ES_NLP = spacy.load(nlp_module.value)

ES_NLP.max_length = 1_500_000

# Parts-of-Speech with large diversity & value
DEFAULT_STUDY_POS = {
    "ADJ",
    "NOUN",
    "VERB",
}

# Parts-of-Speech with small enough diversity to exhaustively study all instances
EXHAUST_POS = {"CCONJ", "INTJ", "SCONJ", "DET", "PRON", "AUX"}


class pseudo_token(object):
    pass


def check_reps(document):
    pd = dict()
    for token in document:
        if token.pos_ not in DEFAULT_STUDY_POS:
            continue
        if token.lemma_ in pd and pd[token.lemma_] != token.pos_:
            print("REP: ", token.lemma_, token.pos_, pd[token.lemma_])
        pd[token.lemma_] = token.pos_


def get_pos_distribution(text):
    document = ES_NLP(text)
    pos_list = {token.pos_ for token in document}
    pos_dict = dict()
    for pos in pos_list:
        pos_dict[pos] = Counter(
            [token.lemma_ for token in document if token.pos_ == pos]
        )
        pos_dict[pos] = {k: v for k, v in pos_dict[pos].items() if v > 2}
    return pos_dict


def sort_vocabs_by_occurence(vocab_dict, corpus):
    def occurence(kv):
        _, ts = kv
        l = [corpus.find(t.text) for t in ts]
        return min([x for x in l if x != -1] + [99_999_999])

    vocab_dict = {k: v for k, v in sorted(vocab_dict.items(), key=occurence)}
    return vocab_dict


def get_vocab(
    text,
    study_pos=DEFAULT_STUDY_POS,
    min_occurences=2,
    vocab_status=None,
    check_real=True,
    token_cleaning=True,
):
    document = ES_NLP(text)

    vocab_dict = {}

    for token in document:
        if token.pos_ not in study_pos:
            continue
        if token_cleaning:
            token = clean_token(token)
        vocab_dict[token.lemma_] = vocab_dict.get(token.lemma_, []) + [token]

    # Remove all entries with less than min_occurences
    vocab_dict = {k: v for k, v in vocab_dict.items() if len(v) >= min_occurences}

    if vocab_status is not None:
        # Remove all entries with unknown or not seen
        vocab_dict = {
            k: v
            for k, v in vocab_dict.items()
            if (not vocab_status.is_discarded(k) and not vocab_status.is_known(k))
        }

    if check_real:
        SPANISH_DICTIONARY = Dictionary()
        vocab_dict = {k: v for k, v in vocab_dict.items() if k in SPANISH_DICTIONARY}

    # Sort dict by occurences
    vocab_dict = {
        k: v for k, v in sorted(vocab_dict.items(), key=lambda item: -len(item[1]))
    }
    return vocab_dict


def get_chapter_vocab(
    texts, study_pos=DEFAULT_STUDY_POS, min_occurences=2, vocab_status=None
):
    all_vocab_dict = dict()
    vocab_dicts = []
    for text in texts:
        vocab_dict = get_vocab(
            text, study_pos=study_pos, min_occurences=0, vocab_status=vocab_status
        )
        vocab_dicts.append(vocab_dict)
        for k, ts in vocab_dict.items():
            all_vocab_dict[k] = all_vocab_dict.get(k, []) + ts
    all_vocab_dict = {
        k: v for k, v in all_vocab_dict.items() if len(v) >= min_occurences
    }

    chapter_vocab = []
    seen_vocabs = set()
    for text, vocab_dict in zip(texts, vocab_dicts):
        vocab_dict = {
            k: all_vocab_dict[k]
            for k in vocab_dict
            if k not in seen_vocabs and k in all_vocab_dict
        }

        # Sort dict by occurences
        vocab_dict = {
            k: v for k, v in sorted(vocab_dict.items(), key=lambda item: -len(item[1]))
        }

        chapter_vocab.append(vocab_dict)

        seen_vocabs = seen_vocabs.union({k for k, v in vocab_dict.items()})
    return chapter_vocab
