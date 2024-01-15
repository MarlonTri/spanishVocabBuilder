from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib
import re
from enum import Enum
from collections import Counter


class TextClean(Enum):
    LOWER = lambda x: x.lower()


class VocabEpub(object):
    def __init__(self, epub_path):
        self.book = epub.read_epub(epub_path)

    def get_docs_text(self, txt_clean_func=TextClean.LOWER):
        docs = list(self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        docs_text = []
        for doc in docs:
            soup = BeautifulSoup(doc.content, features="html.parser")
            txt = soup.get_text()
            if txt_clean_func is not None:
                txt = txt_clean_func(txt)
            docs_text.append(txt)
        return docs_text

    def get_docs_vocab(self, sum_vocab=False, **kwargs):
        docs_text = self.get_docs_text(**kwargs)
        vocabs = []
        for doc_text in docs_text:
            words = re.findall(r"(\w+)", doc_text, re.UNICODE)
            vocab = Counter(words)
            vocabs.append(vocab)

        if sum_vocab:
            return sum(vocab, start=Counter())
        
        return vocabs
s="""<div data-v-56b284df="" class="ProseMirror password-final"><p><span style="font-family: Monospace; font-size: 1px"><strong><em>1</em></strong></span><span style="font-family: Monospace; font-size: 0px"><strong><em>0</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em>:</em></strong></span><span style="font-family: Monospace; font-size: 1px"><strong><em>1</em></strong></span><span style="font-family: Monospace; font-size: 0px"><strong><em>0</em></strong></span><span style="font-family: Monospace; font-size: 4px"><strong><em>2</em></strong></span><span style="font-family: Monospace; font-size: 1px"><strong><em>1</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em> </em></strong></span><span style="font-family: Monospace; font-size: 9px"><strong><em>m</em></strong></span><span style="font-family: Monospace; font-size: 32px"><strong><em>a</em></strong></span><strong><em>yshel</em></strong><span style="font-family: Monospace; font-size: 36px"><strong><em>l</em></strong></span><span style="font-family: Times New Roman; font-size: 36px"><strong><em>X</em></strong></span><span style="font-family: Times New Roman; font-size: 9px"><strong><em>X</em></strong></span><span style="font-family: Times New Roman; font-size: 12px"><strong><em>X</em></strong></span><span style="font-family: Times New Roman; font-size: 28px"><strong><em>V</em></strong></span><strong><em>f</em></strong><span style="font-family: Monospace; font-size: 25px"><strong><em>la</em></strong></span><strong><em>nk🌒🐔🏋️‍♂️🏋️‍♂️🏋️‍♂️ db</em></strong><span style="font-family: Monospace; font-size: 25px"><strong><em>fen </em></strong></span><span style="font-family: Monospace; font-size: 32px"><strong><em>EuH</em></strong></span><span style="font-family: Monospace; font-size: 16px"><strong><em>e</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em>H</em></strong></span><span style="font-family: Monospace; font-size: 32px"><strong><em>f</em></strong></span><span style="font-family: Monospace; font-size: 16px"><strong><em>H</em></strong></span><span style="font-family: Monospace; font-size: 32px"><strong><em> n</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em>y Qx</em></strong></span><span style="font-family: Monospace; font-size: 36px"><strong><em>h</em></strong></span><span style="font-family: Monospace; font-size: 4px"><strong><em>2</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em>+   g</em></strong></span><span style="font-family: Monospace; font-size: 12px"><strong><em>e</em></strong></span><span style="font-family: Monospace; font-size: 16px"><strong><em>rmany</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em> i </em></strong></span><span style="font-family: Monospace; font-size: 36px"><strong><em>a</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em>m </em></strong></span><span style="font-family: Monospace; font-size: 36px"><strong><em>en</em></strong></span><span style="font-family: Monospace; font-size: 25px"><strong><em>ou</em></strong></span><span style="font-family: Monospace; font-size: 28px"><strong><em>g</em></strong></span><span style="font-family: Monospace; font-size: 42px"><strong><em>h</em></strong></span><strong><em>  </em></strong><span style="font-family: Monospace; font-size: 36px"><strong><em>🐛🐛🐛</em></strong></span><strong><em>   </em></strong><span style="font-family: Monospace; font-size: 32px"><strong><em>yo</em></strong></span><span style="font-family: Monospace; font-size: 16px"><strong><em>ut</em></strong></span><span style="font-family: Monospace; font-size: 9px"><strong><em>ube</em></strong></span><strong><em>.co</em></strong><span style="font-family: Monospace; font-size: 36px"><strong><em>m</em></strong></span><strong><em>/w</em></strong><span style="font-family: Monospace; font-size: 12px"><strong><em>a</em></strong></span><strong><em>t</em></strong><span style="font-family: Monospace; font-size: 12px"><strong><em>ch?v=tY</em></strong></span><span style="font-family: Monospace; font-size: 9px"><strong><em>h</em></strong></span><span style="font-family: Monospace; font-size: 16px"><strong><em>obx</em></strong></span><span style="font-family: Monospace; font-size: 64px"><strong><em>8</em></strong></span><span style="font-family: Monospace; font-size: 12px"><strong><em>k</em></strong></span><span style="font-family: Monospace; font-size: 9px"><strong><em>3</em></strong></span><span style="font-family: Monospace; font-size: 12px"><strong><em>zo</em></strong></span><strong><em> </em>#</strong><span style="font-family: Monospace; font-size: 12px"><strong>f</strong></span><strong>a</strong><span style="font-family: Monospace; font-size: 36px"><strong>d</strong></span><span style="font-family: Monospace; font-size: 1px"><strong>1</strong></span><span style="font-family: Monospace; font-size: 12px"><strong>b</strong></span><span style="font-family: Monospace; font-size: 25px"><strong>b</strong></span><strong> </strong><span style="font-family: Monospace; font-size: 1px"><strong>11111</strong>1</span></p><p><span style="font-family: Wingdings; font-size: 1px"><em>###############################################################################################################################################################  ############ ###################################################################################  ################ ########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################</em></span></p></div>"""
soup = BeautifulSoup(s, features="html.parser")
txt = soup.get_text()
print(txt)