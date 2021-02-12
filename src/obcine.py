"""
Ta datoteka obdela podatke o občinah in jih pripravi za uporabo v raziskavi.
"""

import pandas as pd

import os.path

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
PODATKI = os.path.join(FILE_DIR, "../podatki")

migracije = pd.read_csv(os.path.join(PODATKI, "sistat/migracije.csv"))
obcine = pd.read_csv(os.path.join(PODATKI, "sistat/obcine.csv"), index_col="ime")

"""
Izračunali bi radi število migantov, ki prihajajo v našo občino in število
občanov naše občine, ki migrirajo.
"""

# Vzamemo povprečje vseh let.
migracije_po_obcinah = migracije.groupby('obcina').mean()

# Koliko ljudi pride vsak dan v to občino iz druih Slovenskih občin.
delez_lokalnih_delavcev = migracije_po_obcinah.delez_lokalnih_delavcev / 100
obcine["st_migrantov_v_obcino"] = obcine.st_delovno_aktivnih_po_delovnem_mestu - (obcine.st_delovno_aktivnih_po_prebivaliscu * delez_lokalnih_delavcev)

# Koliko ljudi gre vsak dan iz te občine drugam.
delez_migrantov = migracije_po_obcinah.delez_migrantov / 100
obcine["st_migrantov_iz_obcine"] = obcine.st_delovno_aktivnih_po_prebivaliscu * delez_migrantov


"""
Podatke o občinah uredimo v novo tabelo, ki jo izvozimo za uporabo.
"""

# ime,st_prebivalcev,starost,st_vrtcev,st_otrok_v_vrtcih,delez_otrok_v_vrtcih,st_ucencev_v_osnovni_soli,st_dijakov,st_delovno_aktivnih_po_prebivaliscu,st_delovno_aktivnih_po_delovnem_mestu,placa_bruto,placa_neto
df = pd.DataFrame(
    {
        "st_prebivalcev": obcine.st_prebivalcev,
        "st_migrantov_v_obcino": obcine["st_migrantov_v_obcino"],
        "st_migrantov_iz_obcine": obcine["st_migrantov_iz_obcine"],
        "placa_bruto": obcine.placa_bruto,
        "placa_neto": obcine.placa_neto,
    },
    index=obcine.index
)

df.to_csv(os.path.join(PODATKI, "obcine.csv"))