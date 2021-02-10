"""
Ta datoteka izračuna kakšna je verjetnost, da oseba, ki migrira v našo občino
prihaja iz dotične druge občine in kakšna je verjetnost, 
da oseba iz dane občine migrira v dano drugo občino.

Končen rezultat sta zgenerirani tabeli, ki vsebuje verjetnosti, prehajanj med občinami.
"""

import pandas as pd
import numpy as np

import os.path

PODATKI = "./podatki"

razdalje = pd.read_csv(os.path.join(PODATKI, "razdalje.csv"), index_col="zacetek")
migracije = pd.read_csv(os.path.join(PODATKI, "sistat/migracije.csv"))
obcine = pd.read_csv(os.path.join(PODATKI, "obcine.csv"), index_col="ime")

# Nastavitve uteži -----------------------------------------------------------

THRESHOLD = 0.3 # kolikšen del poti je nekdo pripravljen prevozit brez upada
SPEED = 8 # kako hitro padajo vrednosti po znosni_oddakjenosti

# Pomožne funkcije -----------------------------------------------------------

def poti_iz_obcine(obcina):
   """
   Vrne podtke o tem, koliko časa (sekund) in kakšno razdaljo (metrov) 
   potrebuje oseba za pot iz dane občine do vseh ostalih občin.
   """
   return razdalje[razdalje.index == obcina].set_index("konec")

def utez(oddaljenost):
   """Vrne utež glede na relativno oddaljenost občine od druge občine."""
   return np.minimum(
      1, 
      pow((1 - THRESHOLD) + oddaljenost, -SPEED)
   )


"""
Najprej nas zanima kakšen delež migrantov iz posamezne regije 
gre povprečno v dano drugo občino. Povedano drugače, zanima nas 
kakšna je verjetnost, da oseba, ki živi v Ljubljani in migrira, 
migrira v Maribor, Koper...

To bomo izračunali na sledeč način:

1. Najprej bomo izračunali absolutno število ljudi, 
   ki vsak dan migrira v Ljubljano (našo občino). Ta podatek dobimo kot razliko 
   delavno aktivnih prebivalcev, ki delajo v Ljubljani (po delovnem mestu) 
   in delavno aktivnih prebivalcev, ki živijo v Ljubljani (po prebivališču), 
   pomnožen z deležem lokalnih delavcev. 

1. Glede na izbrano občino bomo izračunali kakšna je verjetnost, 
   da gre ta oseba v druge občine. To bom določili kot relativno število migracije
   v posamezno občino glede na vse ostale občine razen te, iz katere oseba prihaja.
   Ker ljudje raje delajo bližje doma, bom vrednosti obtežil
   glede na oddaljenost od dane občine.
"""

# Vzamemo povprečje vseh let.
migracije_po_obcinah = migracije.groupby('obcina').mean()


# Koliko ljudi pride vsak dan v to občino iz druih Slovenskih občin.
delez_lokalnih_delavcev = migracije_po_obcinah.delez_lokalnih_delavcev / 100
obcine["st_migrantov_v_obcino"] = obcine.st_delovno_aktivnih_po_delovnem_mestu - (obcine.st_delovno_aktivnih_po_prebivaliscu * delez_lokalnih_delavcev)

def doloci_konce(obcina):
   """Vrne vektor verjetnosti, da migrira nekdo iz dane občine v drugo občino."""

   # Odstranimo občino v kateri smo.
   ostale_obcine = obcine[obcine.index != obcina].st_migrantov_v_obcino

   # Verjetnost, da se prebivalec naše občine odpelje v drugo občino.
   verjetnost = ostale_obcine / ostale_obcine.sum()

   # Občine otežimo glede na razdaljo od naše občine.
   oddaljenost = poti_iz_obcine(obcina).razdalja
   relativna_oddaljenost = oddaljenost / oddaljenost.max()

   # Uteži rezultate.
   utezena_verjetnost = verjetnost * utez(relativna_oddaljenost)
   normalizirane_verjetnosti = utezena_verjetnost / utezena_verjetnost.sum()

   return normalizirane_verjetnosti.dropna()


"""
Za ugotavljanje porazdelitve delavcev glede na občino prebivališča
bom uporabil simetričen postopek zgornjemu. Izračunali bi radi, kakšna je
verjetnost, da je nekdo, ki dela v Ljubljani (dani občini), prišel iz 
poljubne druge občine.

1. Najprej bomo izračunali koliko ljudi iz posamezne občine migrira. Na primer, 
   izračunali bomo, da 50 Mariborčanov in 100 Koperčanov migrira. 
   Nato se bomo vprašali koliko ljudi, ki migrira v Ljubljano, prihaja iz Kopra - 2/3. 
   To bomo razširili na vse občine in dobili porazdelitev delavcev migrantov po občinah.

1. Ker ljudje iz bližnjih občin prihajajo v občine v večjem številu, 
   bom verjetnost obtežili še glede na bližino posamezne občine.
"""

delez_migrantov = migracije_po_obcinah.delez_migrantov / 100
obcine["st_migrantov_iz_obcine"] = obcine.st_delovno_aktivnih_po_prebivaliscu * delez_migrantov

def doloci_zacetke(obcina):
   """Vrne vektor verjetnosti, da migrira nekdo v dano občino iz drugih občin."""
   ostale_obcine = obcine[obcine.index != obcina].st_migrantov_iz_obcine

   # Verjetnost, da se prebivalec iz dane občine pripelje v našo.
   verjetnost = ostale_obcine / ostale_obcine.sum()

   # Občine otežimo glede na razdaljo od naše občine.
   oddaljenost = poti_iz_obcine(obcina).razdalja
   relativna_oddaljenost = oddaljenost / oddaljenost.max()

   utezena_verjetnost = verjetnost * utez(relativna_oddaljenost)
   normalizirane_verjetnosti = utezena_verjetnost / utezena_verjetnost.sum()

   return normalizirane_verjetnosti.dropna()



# Izpis izračunanih vrednosti ------------------------------------------------

vektor_obcin = pd.Series(obcine.index, index=obcine.index, name="obcina")

migracije_iz_obcine = vektor_obcin.apply(doloci_konce).transpose()
migracije_v_obcino = vektor_obcin.apply(doloci_zacetke).transpose()

migracije_iz_obcine.to_csv(os.path.join(PODATKI, "migracije_iz_obcine.csv"))
migracije_v_obcino.to_csv(os.path.join(PODATKI, "migracije_v_obcino.csv"))

