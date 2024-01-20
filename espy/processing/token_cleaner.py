import re

REFLEXIVE_LEMMA_PAT = "^\w+r ..$"
LEMMA_FIX = {
    "skaa": "skaa",
    "hueles": "oler",
    "colarme": "colarse",
    "skaar": "skaa",
    "obligador": "obligador",
    "tatuaj": "tatuaje",
    "azot": "azote",
    "ejecuter": "ejecutar",
    "asinteír": "asentir",
    "negruro": "negrura",
    "requeer": "requerir",
    "mismísimo": "mismísimo",
    "oer": "oído",
    "tendrar": "tener",
    "muchachita": "muchachita",
    "llegarir": "llegar",
    "gimeír": "gimieron",
    "lor": "lore",
    "palideceír": "palidecer",
    "fuistir": "ir",
    "robastar": "robar",
    "descubrar": "descubren",
    "deprimentemente": "deprimente",
    "sirvient": "sirviente",
    "hazar": "hacer",
    "mandarse": "mandarla",
    "enrojecir": "enrojecer",
    "dame": "darse",
    "vear": "ver",
    "interrumpeír": "interrumpir",
    "goz": "goce",
    "traerir": "traer",
    "huel": "oler",
    "desvanecir": "desvanecido",
    "rebelaríar": "rebelar",
}


def is_reflexive_lemma(lemma):
    return bool(re.match(REFLEXIVE_LEMMA_PAT, lemma))


def clean_token(token):
    token.lemma_ = token.lemma_.strip().lower()
    if is_reflexive_lemma(token.lemma_):
        token.lemma_ = token.lemma_[:-3] + "se"

    if token.lemma_ in LEMMA_FIX:
        token.lemma_ = LEMMA_FIX[token.lemma_]

    return token
