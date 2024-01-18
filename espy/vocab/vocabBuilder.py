import json
import time
from deep_translator import GoogleTranslator

ES_EN_TRANSLATOR = GoogleTranslator(source="es", target="en")
DEFAULT_JSON_PATH = "./espy/resources/vocab_info.json"


def clean_sentence(sent):
    return str(sent).replace("\n", "  ").strip()


def user_process_vocab(vocab_infos, vocab_dict, tags=None, corpus=None):
    print(f"Beginning sentence selection with {len(vocab_dict)} candidates.")

    vocab_dict = {k: v for k, v in vocab_dict.items() if not vocab_infos.has(k)}
    print(f"{len(vocab_dict)} candidates remaining after filtering existing selections")

    selected = []
    for i, (word, tokens) in enumerate(vocab_dict.items()):
        tokens = sorted(tokens, key=lambda t: len(clean_sentence(t.sent)))
        print(f"({len(vocab_dict) - i}) Beginning selection on '{word}':")
        for j, token in enumerate(tokens):
            cleaned_sent = clean_sentence(token.sent)
            print(f"({j}):\t{cleaned_sent}")
        sel_num = input("Selected sentence (-1 for none)")
        sel_num = int(sel_num)
        if sel_num == -1:
            print("Exiting selection process.")
            break
        if sel_num == -2:
            print(f"Skipping '{word}'.")
            continue
        v_info = VocabInfo().load_token(tokens[sel_num], tags=tags, corpus=corpus)
        vocab_infos.add(v_info)
        vocab_infos.save()
    return selected


class VocabInfo(dict):
    def __init__(self):
        pass

    def dict_init(self):
        dict.__init__(
            self,
            lemma=self.lemma,
            pos=self.pos,
            sent=self.sent,
            morph=self.morph,
            text=self.text,
            english=self.english,
            english_sent=self.english_sent,
            tags=self.tags,
            sort_field=self.sort_field,
        )

    def load_raw(
        self,
        lemma=None,
        pos=None,
        sent=None,
        morph=None,
        text=None,
        english=None,
        english_sent=None,
        tags=None,
        sort_field=None,
    ):
        self.lemma = lemma
        self.pos = pos
        self.sent = sent
        self.morph = morph
        self.text = text
        self.english = english
        self.english_sent = english_sent
        self.tags = tags
        self.sort_field = sort_field
        self.dict_init()
        return self

    def load_token(self, token, tags, corpus=None):
        self.lemma = token.lemma_
        self.pos = token.pos_
        self.sent = str(token.sent).replace("\n", " ").strip()
        self.morph = token.morph.to_dict()
        self.text = token.text

        print(f"Running Google translate on {self.lemma}")
        self.english = ES_EN_TRANSLATOR.translate(self.lemma)
        time.sleep(2)
        print(f"Running Google translate on {self.lemma} sentence")
        self.english_sent = ES_EN_TRANSLATOR.translate(self.sent)
        self.tags = tags

        if corpus is not None and self.text in corpus:
            self.sort_field = "CHAR-" + str(corpus.index(self.text)).rjust(8, '0')

        self.dict_init()
        return self


class VocabInfos(object):
    def __init__(self, json_path=DEFAULT_JSON_PATH):
        self.infos_dict = dict()
        self.json_path = json_path
        self.load()

    def has(self, lemma):
        return lemma in self.infos_dict

    def list(self):
        return list(self.infos_dict.values())

    def add(self, vocab_info):
        assert vocab_info.lemma not in self.infos_dict
        self.infos_dict[vocab_info.lemma] = vocab_info

    def load(self):
        with open(self.json_path, "r") as f:
            raw_infos_dict = json.load(f)

        self.infos_dict = dict()

        for k, v in raw_infos_dict.items():
            self.infos_dict[k] = VocabInfo().load_raw(**v)

    def save(self):
        with open(self.json_path, "w") as f:
            json.dump(self.infos_dict, f, indent="\t")
