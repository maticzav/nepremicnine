# https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/0772750S.px/footnotes/footnoteView/
from json import load
from bs4 import BeautifulSoup
import re

import orodja

# Nastavitve

SISTAT_MIGRACIJE_MED_REGIJAMI_PODATKI = "podatki/sistat/migracije_med_regijami.html"
SISTAT_MIGRACIJE_PODATKI = "podatki/sistat/migracije.html"
SISTAT_OBCINE_PODATKI = "podatki/sistat/obcine.html"

SISTAT_JSON_DATOTEKA = "podatki/sistat.json"
SISTAT_CSV_MIGRACIJE_DATOTEKA = "podatki/migracije.csv"
SISTAT_CSV_OBCINE_DATOTEKA = "podatki/obcine.csv"

# Podatki

OBCINE = dict() # slovar občin identificiranih z imenom

vsebina_migracij = orodja.vsebina_datoteke(SISTAT_MIGRACIJE_PODATKI)
vsebina_obcin = orodja.vsebina_datoteke(SISTAT_OBCINE_PODATKI)
vsebina_migracij_med_regijami = orodja.vsebina_datoteke(SISTAT_MIGRACIJE_MED_REGIJAMI_PODATKI)

# Obdelava -------------------------------------------------------------------

# Osnovni podatki o občini

soup_obcine = BeautifulSoup(vsebina_obcin, 'html.parser')

for obcina in soup_obcine.select("tbody tr"):

    # Obdelaj vsako občino posebaj
    podatki = obcina.find_all("td")

    ime = podatki[0].getText()
    st_prebivalcev = int(podatki[2].getText())
    starost = float(podatki[8].getText().replace(",", "."))

    st_vrtcev = podatki[9].getText()
    try:
        st_vrtcev = int(st_vrtcev)
    except:
        st_vrtcev = None

    st_otrok_v_vrtcih = podatki[10].getText()
    try:
        st_otrok_v_vrtcih = int(st_otrok_v_vrtcih)
    except:
        st_otrok_v_vrtcih = None

    delez_otrok_v_vrtcih = float(podatki[11].getText().replace(",", "."))
    st_ucencev_v_osnovni_soli = int(podatki[12].getText())
    st_dijakov = int(podatki[13].getText())

    # Ljudje, ki delajo in živijo v občini
    st_delovno_aktivnih_po_prebivaliscu = int(podatki[14].getText())
    # Ljudje, ki živijo ali v občini ali drugje in imajo delovno mesto v občini
    st_delovno_aktivnih_po_delovnem_mestu = int(podatki[15].getText())

    placa_bruto = float(podatki[16].getText().replace(",", "."))
    placa_neto = float(podatki[17].getText().replace(",", "."))

    OBCINE[ime] = {
        "ime": ime,

        "st_prebivalcev": st_prebivalcev,
        "starost": starost,

        "st_vrtcev": st_vrtcev,
        "st_otrok_v_vrtcih": st_otrok_v_vrtcih,
        "delez_otrok_v_vrtcih": delez_otrok_v_vrtcih,
        "st_ucencev_v_osnovni_soli": st_ucencev_v_osnovni_soli,
        "st_dijakov": st_dijakov,

        "st_delovno_aktivnih_po_prebivaliscu": st_delovno_aktivnih_po_prebivaliscu,
        "st_delovno_aktivnih_po_delovnem_mestu": st_delovno_aktivnih_po_delovnem_mestu,

        "placa_bruto": placa_bruto,
        "placa_neto": placa_neto,

        "migracije": []
    }

# Podatki o migracijah


soup_migracije = BeautifulSoup(vsebina_migracij, 'html.parser')

for obcina in soup_migracije.select("tbody tr"):

    # Obdelaj vsako občino posebaj
    podatki = obcina.find_all("td")

    ime = podatki[0].getText()

    leto = int(podatki[1].getText())
    # Delež med vsemi delovno aktivnimi prebivalci v občini
    try:
        delez_migrantov = float(podatki[2].getText().replace(",", "."))
        delez_migrantov_moski = float(podatki[3].getText().replace(",", "."))
        delez_migrantov_zenske = float(podatki[4].getText().replace(",", "."))

        delez_lokalnih_delavcev = float(podatki[5].getText().replace(",", "."))
        delez_lokalnih_delavcev_moski = float(podatki[6].getText().replace(",", "."))
        delez_lokalnih_delavcev_zenske = float(podatki[7].getText().replace(",", "."))
    except:
        continue
    

    OBCINE[ime]["migracije"].append({
        "leto": leto,
        # Delež med vsemi delovno aktivnimi prebivalci v občini
        "delez_migrantov": delez_migrantov,
        "delez_migrantov_moski": delez_migrantov_moski,
        "delez_migrantov_zenske": delez_migrantov_zenske,

        "delez_lokalnih_delavcev": delez_lokalnih_delavcev,
        "delez_lokalnih_delavcev_moski": delez_lokalnih_delavcev_moski,
        "delez_lokalnih_delavcev_zenske": delez_lokalnih_delavcev_zenske,
    })


# Podatki o migracijeah med regijami

soup_migracije_med_regijami = BeautifulSoup(vsebina_migracij_med_regijami, 'html.parser')

for obcina in soup_migracije_med_regijami.select("tbody tr"):

    # Obdelaj vsako občino posebaj
    podatki = obcina.find_all("td")

    spol = podatki[0].getText()

    if spol != "Spol - SKUPAJ":
        continue
        
    # Preberi podatke po letih
    try:
        delez_migrantov = float(podatki[2].getText().replace(",", "."))

    except:
        continue
    

    # OBCINE[ime]["migracije"][leto]



# Shrani podatke v datotetko -------------------------------------------------

# JSON
json = { "obcine": list(OBCINE.values()) }
orodja.zapisi_json(json, SISTAT_JSON_DATOTEKA)

# CSV

csv_obcine = []
csv_migracije = []

for obcina in list(OBCINE.values()):
    for migracija in obcina.pop('migracije'):

        # Dodaj podatek o občini
        migracija.update({
            "obcina": obcina["ime"]
        })

        csv_migracije.append(migracija)

    csv_obcine.append(obcina)

orodja.zapisi_csv(csv_obcine, [
   "ime",

    "st_prebivalcev",
    "starost",

    "st_vrtcev",
    "st_otrok_v_vrtcih",
    "delez_otrok_v_vrtcih",
    "st_ucencev_v_osnovni_soli",
    "st_dijakov",

    "st_delovno_aktivnih_po_prebivaliscu",
    "st_delovno_aktivnih_po_delovnem_mestu",

    "placa_bruto",
    "placa_neto",
], SISTAT_CSV_OBCINE_DATOTEKA)

orodja.zapisi_csv(csv_migracije, [
    "obcina",
    "leto",

    "delez_migrantov",
    "delez_migrantov_moski",
    "delez_migrantov_zenske",

    "delez_lokalnih_delavcev",
    "delez_lokalnih_delavcev_moski",
    "delez_lokalnih_delavcev_zenske",
], SISTAT_CSV_MIGRACIJE_DATOTEKA)

print("Shranil!")
