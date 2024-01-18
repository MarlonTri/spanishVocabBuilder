import genanki
import hashlib

from espy.vocab.vocabBuilder import VocabInfo, VocabInfos

HASH_PREFIX = "HASH="

FRONT_TEXT_TEMPL = """
<div id="kard">
    <br><br>
    <b>{{lemma}}</b> - <span class="censored">{{english}}</span>
    <br><br>
		{{sent_left}}<b>{{text}}</b>{{sent_right}}
    <br>
    <span class="censored">{{english_sent}}</span>
    <br><br>
    {{pos}}
    <div class="tags" id='tags'>Tags:  {{Tags}}</div>
</div>
"""

BACK_TEXT_TEMPL = """
<div id="kard">
    <br><br>
    <b>{{lemma}}</b> - <i>{{english}}</i>
    <br><br>
		{{sent_left}}<b>{{text}}</b>{{sent_right}}
    <br>
    {{english_sent}}
    <br><br>
    {{pos}}
    <div class="tags" id='tags'>Tags:  {{Tags}}</div>
</div>

"""
DEFAULT_CSS_CARD_PATH = "./espy/resources/anki_card.css"

with open(DEFAULT_CSS_CARD_PATH, "r") as f:
    CARD_CSS = f.read()

ANKI_BUILDER_MODEL = genanki.Model(
    model_id=2043614750,
    name="AnkiBuilder",
    fields=[
        {"name": "sort_field"},
        {"name": "lemma"},
        {"name": "pos"},
        {"name": "sent"},
        {"name": "morph"},
        {"name": "text"},
        {"name": "english"},
        {"name": "english_sent"},
        {"name": "sent_left"},
        {"name": "sent_right"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": FRONT_TEXT_TEMPL,
            "afmt": BACK_TEXT_TEMPL,
        },
    ],
    css=CARD_CSS,
)


def morph_to_text(morph):
    t = ""
    for i, (k, v) in enumerate(morph.items()):
        if i % 3 == 0:
            t = t + "<br>"
        else:
            t = t + "|"
        t = t + k + "=" + v

    return t


def gen_guid(vocab_info: VocabInfo):
    hash_str = HASH_PREFIX + vocab_info.lemma

    h = int(hashlib.sha1(hash_str.encode("utf-8")).hexdigest(), 16) % (10**12)
    return h


def make_note(vocab_info: VocabInfo):
    morph_text = morph_to_text(vocab_info.morph)
    sent_left, sent_right = vocab_info.sent.split(vocab_info.text, 1)
    note = genanki.Note(
        model=ANKI_BUILDER_MODEL,
        fields=[
            vocab_info.sort_field,
            vocab_info.lemma,
            vocab_info.pos,
            vocab_info.sent,
            morph_text,
            vocab_info.text,
            vocab_info.english,
            vocab_info.english_sent,
            sent_left,
            sent_right,
        ],
        tags=vocab_info.tags,
        guid=gen_guid(vocab_info),
    )

    return note


def build_deck(deck_id, deck_name, vocab_infos: VocabInfos):
    deck = genanki.Deck(deck_id, deck_name)

    for vocab_info in sorted(vocab_infos.list(), key=lambda vi: vi.sort_field):
        note = make_note(vocab_info)
        deck.add_note(note)

    genanki.Package(deck).write_to_file("output.apkg")

    return deck
