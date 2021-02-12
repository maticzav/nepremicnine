"""
Ta datoteka uredi podatke podjetji v podatke, ki jih uporabimo v analizi.
"""

import pandas as pd
import re

import os.path

from orodja import levensthein

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
PODATKI = os.path.join(FILE_DIR, "../podatki")

podjetja = pd.read_csv(os.path.join(PODATKI, "bizi/bizi.csv"), index_col="id")
obcine = pd.read_csv(os.path.join(PODATKI, "obcine.csv"), index_col="ime")

"""
Podatke o podjetjih bomo popravili tako, da bodo imela vsa podjetja veljavno
ime občine (t.j. tako ime, ki ga lahko najdemo v seznamu občin). Da bi ocenili
katero ime je pravo bomo uporabili Levenshteinov algoritem.
"""

imena_obcin = obcine.index.array

def obcina(ime_obcine):
    """Vrne predvideno ime občine."""

    # Če je občina že v seznamu občin, potem lahko vrnemo kar dano ime.
    if obcina in imena_obcin:
        return obcina

    # Drugače vrni najbližjo.
    return min(imena_obcin, key=lambda obcina: levensthein(ime_obcine, obcina))


"""
Prav tako bomo ocenili spodnje število zaposlenih v podjetju. S pomočjo regularnih
izrazov bomo poiskali vse številke znotraj stolpca o zaposlenih in vzeli najmanjšo.
"""

stevilo = re.compile("\d+", flags=re.M)

def st_zaposlenih(niz):
    """Vrne najmanjše število v nizu - število zaposlenih."""
    stevila = [int(stevilo) for stevilo in stevilo.findall(niz)]
    return min(stevila)


"""
Izračunamo uporabne podatke o podjetjih glede na podatke iz bizija.
"""

p_obcine = podjetja["obcina"].apply(obcina)
p_zaposleni = podjetja["zaposleni"].apply(st_zaposlenih)

# id,ime,maticna_stevilka,obcina,zaposleni,dobicek
df = pd.DataFrame(
    {
        "ime": podjetja["ime"],
        "maticna_stevilka": podjetja["maticna_stevilka"],
        "obcina": p_obcine,
        "st_zaposlenih": p_zaposleni,
        "dobicek": podjetja["dobicek"]
    },
    index=podjetja.index
)

df.to_csv(os.path.join(PODATKI, "podjetja.csv"))