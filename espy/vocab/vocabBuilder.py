import json
import os
import time
from deep_translator import GoogleTranslator
import pandas as pd

ES_EN_TRANSLATOR = GoogleTranslator(source="es", target="en")
DEFAULT_SAVE_PATH = "./espy/resources/vocab_info.csv"


def clean_sentence(sent):
    return str(sent).replace("\n", "  ").strip()


def to_formatted_dicts(df):
    result = []
    for _, row in df.iterrows():
        parsed_row = {}
        for idx, val in row.iteritems():
            parsed_row[idx] = val

        result.append(parsed_row)
    return result


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
        print(
            "Selected sentence (-1 for exit, -2 for skip. Add sentence after number if desired)"
        )
        sel_num = input("Input: ")
        vocab_infos.load()
        custom_sent = None
        if " " in sel_num:
            sel_num, custom_sent = sel_num.split(maxsplit=1)
        sel_num = int(sel_num)
        if sel_num == -1:
            print("Exiting selection process.")
            break
        if sel_num == -2:
            print(f"Skipping '{word}'.")
            continue

        selected_token = tokens[sel_num]
        v_info = VocabInfo().load_token(
            selected_token, tags=tags, corpus=corpus, sentence_override=custom_sent
        )
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
        self.tags = tags or []
        self.sort_field = sort_field
        self.dict_init()
        return self

    def load_token(self, token, tags, corpus=None, sentence_override=None):
        self.lemma = token.lemma_
        self.pos = token.pos_

        self.sent = token.sent if (sentence_override is None) else sentence_override
        self.sent = str(self.sent).replace("\n", " ").strip()

        self.morph = token.morph.to_dict()
        self.text = token.text

        print(f"Running Google translate on {self.lemma}")
        self.english = ES_EN_TRANSLATOR.translate(self.lemma)
        time.sleep(2)
        print(f"Running Google translate on {self.lemma} sentence")
        self.english_sent = ES_EN_TRANSLATOR.translate(self.sent)
        self.tags = tags or []

        if corpus is not None and self.text in corpus:
            self.sort_field = "CHAR-" + str(corpus.index(self.text)).rjust(8, "0")

        self.dict_init()
        return self


class VocabInfos(object):
    COLS = [
        "lemma",
        "pos",
        "english",
        "text",
        "sort_field",
        "sent",
        "english_sent",
        "morph",
        "tags",
    ]

    def __init__(self, save_path=DEFAULT_SAVE_PATH):
        _, file_extension = os.path.splitext(DEFAULT_SAVE_PATH)

        if file_extension != ".csv" and file_extension != ".json":
            raise Exception("File extension bad")

        self.is_json = file_extension == ".json"

        self.infos_dict = dict()
        self.save_path = save_path
        self.load()

    def has(self, lemma):
        return lemma in self.infos_dict

    def list(self):
        return list(self.infos_dict.values())

    def add(self, vocab_info):
        assert vocab_info.lemma not in self.infos_dict
        self.infos_dict[vocab_info.lemma] = vocab_info

    def load(self):
        if self.is_json:
            self.load_json()
        else:
            self.load_csv()

    def save(self):
        if self.is_json:
            self.save_json()
        else:
            self.save_csv()

    def load_csv(self):
        df = pd.read_csv(self.save_path, encoding="utf-8")
        dicts = to_formatted_dicts(df)

        self.infos_dict = dict()
        for d in dicts:
            d["morph"] = json.loads(d["morph"])
            d["tags"] = json.loads(d["tags"])
            self.infos_dict[d["lemma"]] = VocabInfo().load_raw(**d)

    def save_csv(self):
        df = pd.json_normalize(self.infos_dict.values(), max_level=0)
        df = df.reindex(self.COLS, axis=1)
        df["morph"] = df["morph"].apply(json.dumps)
        df["tags"] = df["tags"].apply(json.dumps)
        df.to_csv(self.save_path, encoding="utf-8", index=False)

    def load_json(self):
        with open(self.save_path, "r") as f:
            raw_infos_dict = json.load(f)

        self.infos_dict = dict()

        for k, v in raw_infos_dict.items():
            self.infos_dict[k] = VocabInfo().load_raw(**v)

    def save_json(self):
        with open(self.save_path, "w") as f:
            json.dump(self.infos_dict, f, indent="\t")
