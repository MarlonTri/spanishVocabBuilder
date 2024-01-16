import pandas as pd
import os
import readchar

DEFAULT_CSV_PATH = "./espy/resources/vocab/main_vocab.csv"


class VocabStatus(object):
    COLS = ["Word", "Known", "Discard"]

    def __init__(self, csv_path=DEFAULT_CSV_PATH):
        self.csv_path = csv_path

        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
        else:
            self.df = pd.DataFrame(columns=self.COLS)

    # def add_terms(self, words):
    #     new_words = set(words).difference(self.df["Word"])
    #     new_words_df = pd.DataFrame(columns=self.COLS)
    #     new_words_df["Word"] = new_words
    #     new_words_df["Known"] = False
    #     new_words_df["Seen"] = False
    #     new_words_df["Discard"] = False

    #     self.df.concat(new_words_df)

    def is_seen(self, word: str):
        l = len(self.df[self.df["Word"] == word])
        if l == 0:
            return False
        assert l == 1
        return True

    def is_known(self, word: str):
        if not self.is_seen(word):
            return False
        return list(self.df[self.df["Word"] == word]["Known"])[0]
    
    def is_discarded(self, word: str):
        if not self.is_seen(word):
            return False
        return list(self.df[self.df["Word"] == word]["Discard"])[0]

    def save(self):
        self.df.to_csv(self.csv_path, encoding="utf-8", index=False)

    def set_word(self, word: str, known: bool, discard: bool):
        if self.is_seen(word):
            row = self.df[self.df["Word"] == word]
            row["Known"] = known
            row["Discard"] = discard
        else:
            self.df.loc[len(self.df.index)] = [word, known, discard]

    def user_process_words(self, vocabs):
        print()
        print("Key guide:")
        print(" 'k' = Known")
        print(" 'd' = Discard")
        print(" '?' = Hit debug line to view vocab context")
        print(" 'x' = End selecting")
        print(" 'any other' = Unknown")
        print()
        print(f"Beginning word selection with {len(vocabs)} candidates.")

        vocabs = {k:v for k,v in vocabs.items() if not self.is_seen(k)}
        print(f"{len(vocabs)} candidates remaining after filtering for is_seen")

        selected = []
        for i,(word, context) in enumerate(vocabs.items()):
            print(f"({len(vocabs) - i}) {word}:", end="")
            c = repr(readchar.readchar()).strip("'")
            if c == "?":
                # Debuggable line to get context on a vocab
                c = repr(readchar.readchar()).strip("'")
            if c == "k":
                print(f" ({c}) set to Known!")
                self.set_word(word, True, False)
            elif c == "d":
                print(f" ({c}) set to Discard!")
                self.set_word(word, False, True)
            elif c == "x":
                print(f" ({c}) Ending selection")
                break
            else:
                selected.append(word)
                print(f" ({c}) set to Unknown")
                self.set_word(word, False, False)
            self.save()
        return selected
