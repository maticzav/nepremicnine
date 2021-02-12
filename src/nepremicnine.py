"""
Ta datoteka obdela podatke o nepremičninah in poskrbi, da jih bomo
lahko pravilno uporabili v raziskavi v Jupyter Notebook-u.
"""

import numpy as np
import pandas as pd

import os.path

from orodja import levensthein

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
PODATKI = os.path.join(FILE_DIR, "../podatki")

nepremicnine = pd.read_csv(os.path.join(PODATKI, "nepremicninenet/nepremicnine.csv"), index_col="id")
obcine = pd.read_csv(os.path.join(PODATKI, "obcine.csv"), index_col="ime")

"""
S pomočjo Levenshteina določimo občino v kateri se nepremičnina nahaja.
"""

imena_obcin = obcine.index.array

def obcina(ime_obcine):
    """Vrne predvideno ime občine."""

    # Če je občina že v seznamu občin, potem lahko vrnemo kar dano ime.
    if obcina in imena_obcin:
        return obcina

    if type(ime_obcine) != str:
        return np.nan

    # Drugače vrni najbližjo.
    return min(imena_obcin, key=lambda obcina: levensthein(ime_obcine, obcina))



"""
Izpišemo podatke v novo datoteko o nepremičninah.
"""

# id,posredovanje,naslov,url,kratek_opis,vrsta,regija,upravna_enota,obcina,velikost,cena,leto,sobe,agencija
n_obcina = nepremicnine["obcina"].apply(obcina).dropna()

# id,ime,maticna_stevilka,obcina,zaposleni,dobicek
df = pd.DataFrame(
    {
        "naslov": nepremicnine["naslov"],
        "posredovanje": nepremicnine["posredovanje"],
        "vrsta": nepremicnine["vrsta"],
        "obcina": n_obcina,
        "velikost": nepremicnine["velikost"],
        "cena": nepremicnine["cena"],
        "leto": nepremicnine["leto"],
        "sobe": nepremicnine["sobe"],
    },
    index=nepremicnine.index
)

df.to_csv(os.path.join(PODATKI, "nepremicnine.csv"))