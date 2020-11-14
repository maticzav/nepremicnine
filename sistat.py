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

print(f"Nalagam podatke o občinah...")

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

        "migracije": dict()
    }

    print(f"Naložil občino {ime}!")

# Podatki o migracijah


soup_migracije = BeautifulSoup(vsebina_migracij, 'html.parser')

print(f"Nalagam podatke o skupnem številu migracij...")

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
    

    OBCINE[ime]["migracije"][leto] = {
        "leto": leto,
        # Delež med vsemi delovno aktivnimi prebivalci v občini
        "delez_migrantov": delez_migrantov,
        "delez_migrantov_moski": delez_migrantov_moski,
        "delez_migrantov_zenske": delez_migrantov_zenske,

        "delez_lokalnih_delavcev": delez_lokalnih_delavcev,
        "delez_lokalnih_delavcev_moski": delez_lokalnih_delavcev_moski,
        "delez_lokalnih_delavcev_zenske": delez_lokalnih_delavcev_zenske,
    }

    print(f"Obdelal migracije v {ime} leta {leto}!")


# Podatki o migracijeah med regijami

soup_migracije_med_regijami = BeautifulSoup(vsebina_migracij_med_regijami, 'html.parser')

print(f"Nalagam migracije med občinami...")

for obcina in soup_migracije_med_regijami.select("tbody tr"):

    # Obdelaj vsako občino posebaj
    podatki = obcina.find_all("td")

    spol = podatki[0].getText()

    if spol != "Spol - SKUPAJ":
        continue

    # Obcini
    delo = podatki[1].getText().replace("[delo]", "").strip()
    prebivalisce = podatki[2].getText().replace("[prebivališče]", "").strip()

    # Preberi podatke po letih
    for i in range(0, 20):
        leto = 2000 + i
        indeks = i + 3 # podatki o letih se začnejo na četrtem mestu
        st_migrantov = int(podatki[indeks].getText())

        # Število ljudi iz posamezne občine, ki prihaja v občino na delovno mesto.
        if delo in OBCINE:
            if "prilivi" not in OBCINE[delo]["migracije"][leto]:
                OBCINE[delo]["migracije"][leto].update({ "prilivi": dict() })
                
            OBCINE[delo]["migracije"][leto]["prilivi"][prebivalisce] = st_migrantov
        else:
            print(f"Neznana občina {delo}")

        # Podatek o tem koliko ljudi iz te občine migrira v doditično drugo občino.
        if prebivalisce in OBCINE:
            if "migracije" not in OBCINE[prebivalisce]["migracije"][leto]:
                OBCINE[prebivalisce]["migracije"][leto].update({ "migracije": dict() })
                    
            OBCINE[prebivalisce]["migracije"][leto]["migracije"][delo] = st_migrantov
        else:
            print(f"Neznana občina {prebivalisce}")

    print(f"Obdelal migracije za prebivalce {prebivalisce}, ki delajo v {delo}!")



# Shrani podatke v datotetko -------------------------------------------------

# JSON
json = { "obcine": list(OBCINE.values()) }
orodja.zapisi_json(json, SISTAT_JSON_DATOTEKA)

# CSV

csv_obcine = []
csv_migracije = []

for obcina in list(OBCINE.values()):
    for migracija in obcina.pop('migracije').values():

        # Dodaj podatek o občini
        migracija.update({
            "obcina": obcina["ime"]
        })

        if "prilivi" in migracija:
            migracija.pop("prilivi")
        if "migracije" in migracija:
            migracija.pop("migracije")

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
