from bs4 import BeautifulSoup
import ebooklib
import ebooklib.epub
from espy.media.media import TextClean, Media


class epubMedia(Media):
    def __init__(self, epub_path):
        self.book = ebooklib.epub.read_epub(epub_path)

    def get_docs_text(self, txt_clean_func=None):
        docs = list(self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        docs_text = []
        for doc in docs:
            soup = BeautifulSoup(doc.content, features="html.parser")
            txt = soup.get_text()
            if txt_clean_func is not None:
                txt = txt_clean_func(txt)
            docs_text.append(txt)
        return docs_text
