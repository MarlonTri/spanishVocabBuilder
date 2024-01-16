import spacy
from collections import Counter

ES_NLP = spacy.load("es_core_news_md")

# Parts-of-Speech with large diversity & value
DEFAULT_STUDY_POS = {
    "ADJ",
    "NOUN",
    "VERB",
}

# Parts-of-Speech with small enough diversity to exhaustively study all instances
EXHAUST_POS = {"CCONJ", "INTJ", "SCONJ", "DET", "PRON", "AUX"}


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


def get_vocab(text, study_pos=DEFAULT_STUDY_POS, min_occurences=2, vocab_status=None):
    document = ES_NLP(text)

    vocab_dict = {}

    for token in document:
        if token.pos_ not in study_pos:
            continue
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

    # Sort dict by occurences
    vocab_dict = {
        k: v for k, v in sorted(vocab_dict.items(), key=lambda item: -len(item[1]))
    }
    return vocab_dict


def get_chapter_vocab(
    texts, study_pos=DEFAULT_STUDY_POS, min_occurences=2, vocab_status=None
):
    all_text = "\n\n".join(texts)
    all_vocab_dict = get_vocab(
        all_text,
        study_pos=study_pos,
        min_occurences=min_occurences,
        vocab_status=vocab_status,
    )

    chapter_vocab = []
    seen_vocabs = set()
    for text in texts:
        vocab_dict = get_vocab(
            text, study_pos=study_pos, min_occurences=0, vocab_status=vocab_status
        )
        vocab_dict = {
            k: all_vocab_dict[k]
            for k in vocab_dict
            if k not in seen_vocabs and k in all_vocab_dict
        }
        chapter_vocab.append(vocab_dict)

        seen_vocabs = seen_vocabs.union({k for k, v in vocab_dict.items()})
    return chapter_vocab