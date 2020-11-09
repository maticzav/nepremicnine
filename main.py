from json import load
from bs4 import BeautifulSoup
import re
import os

import orodja
from orodja import vsebina_datoteke

# Nastavitve

NEPREMICNINE_NASLOV = 'https://www.nepremicnine.net'
NEPREMICNINE_POSREDOVANJA = [ "oddaja", "prodaja"]
# NEPREMICNINE_POSREDOVANJA = [ "najem", "oddaja", "nakup", "prodaja"]

NEPREMICNINE_JSON_DATOTEKA = "podatki/nepremicnine.json"
NEPREMICNINE_CSV_DATOTEKA = "podatki/nepremicnine.csv"

# Zbiralnik podatkov

OGLASI = dict() # slovar oglasov identificiranih z id-jem

"""
Posamezen oglas, ki ga preberemo ima sledečo obliko:

type Oglas {
    id: string

    # Informacije o oglasu
    posredovanje: 'najem' | 'oddaja' | 'nakup' | 'prodaja'
    naslov: string
    url: string

    # Podrobnosti oglasa
    kratek_opis: string
    daljsi_opis: string

    vrsta: string
    regija: string
    upravna_enota: string
    obcina: string
    
    velikost: float
    cena: float

    slike: [string]

    # Dodatne informacije
    agencija: string

}
"""

PODVOJENI_OGLASI = set() # zabeležimo si vse podvojene oglase

for posredovanje in NEPREMICNINE_POSREDOVANJA:

    # Podatki o napredku
    stevilo_oglasov_v_posredovanju = 0
    stran = 1

    while True:
        # Podatki o strani
        url = f'{NEPREMICNINE_NASLOV}/oglasi-{posredovanje}/{stran}/'
        datoteka = f'podatki/nepremicnine/{posredovanje}/{stran}.html'

        # Naloži stran
        orodja.shrani_spletno_stran(url, datoteka)
        vsebina_oglasov = orodja.vsebina_datoteke(datoteka)

        # Analiziraj podatke
        soup = BeautifulSoup(vsebina_oglasov, 'html.parser')
        oglasi = soup.find_all("div", class_="oglas_container")

        # Preveri vsebino podatkov
        if len(oglasi) == 0:
            break

        # Analiziramo posamezen oglas tako, da uporabimo 
        # funkcije iz BS na match-u enega oglasa.
        for oglas in oglasi:

            # Oglas
            id = oglas.get('id')

            # Preveri ali oglas že obstaja
            if OGLASI.get(id):
                PODVOJENI_OGLASI.add(id)
                continue

            # Informacije o oglasu
            posredovanje = posredovanje
            naslov = oglas.find("span", class_="title").string
            url_oglasa = f"{NEPREMICNINE_NASLOV}{oglas.find('a')['href']}"

            # Podrobne informacije o oglasu dobimo iz strani posameznega
            # oglasa. Z vsebino strani naredimo nov BS soup_oglasa.
            datoteka_oglasa = f'podatki/nepremicnine/oglasi/{id}.html'

            orodja.shrani_spletno_stran(url_oglasa, datoteka_oglasa)
            vsebina_oglasa = orodja.vsebina_datoteke(datoteka_oglasa)

            # Analiziraj podatke o oglasu
            soup_oglasa = BeautifulSoup(vsebina_oglasa, 'html.parser')

            if soup_oglasa.find(string=[ "Not Found", "Oglas ni več aktiven." ]):
                print(f"Napaka: {url_oglasa}")
                continue

            # Podrobnosti oglasa
            kratek_opis = soup_oglasa.find("div", itemprop="description").getText()
            daljsi_opis = getattr(soup_oglasa.find("div", _class="web-opis"), "string", None)

            informacije = soup_oglasa.find("div", class_="more_info").string

            vrsta = re.compile("Vrsta: ([\w\sščž.]+)").search(informacije)
            if vrsta:
                vrsta = vrsta.group(1).strip()

            regija = re.compile("Regija: ([\w\sščž.]+)").search(informacije)
            if regija:
                regija = regija.group(1).strip()

            upravna_enota = re.compile("Upravna enota: ([\w\sščž.]+)").search(informacije)
            if upravna_enota:
                upravna_enota = upravna_enota.group(1).strip()

            obcina = re.compile("Občina: ([\w\sščž.]+)").search(informacije)
            if obcina:
                obcina = obcina.group(1).strip()

            
            vzorec_velikosti = re.compile("([\d,.]+)")
            velikost = oglas.find("span", class_="velikost").string
            if velikost:
                velikost = vzorec_velikosti.search(velikost).group(1)
                velikost = velikost.replace(".", "").replace(",", ".")
                velikost = float(velikost)

            cena = oglas.find("meta", itemprop="price")
            if cena:
                if cena["content"]:
                    cena = float(cena["content"])
                else:
                    cena = None

            slike = []
            for slika in soup_oglasa.find_all("a", class_="rsImg"):
                slike.append(slika["href"].replace("sIo", "slo"))
            
            # Dodatne informacije
            agencija = oglas.find("span", class_="agencija").string

            # Zabeleži oglas
            OGLASI[id] = {
                "id": id,

                # Informacije o oglasu
                "posredovanje": posredovanje,
                "naslov": naslov,
                "url": url_oglasa,

                # Podrobnosti oglasa
                "kratek_opis": kratek_opis,
                "daljsi_opis": daljsi_opis,

                "vrsta": vrsta,
                "regija": regija,
                "upravna_enota": upravna_enota,
                "obcina": obcina,

                "cena": cena,
                "velikost": velikost,

                "slike": slike,

                # Dodatne informacije
                "agencija": agencija
            }

            stevilo_oglasov_v_posredovanju += 1

        # Posodobi informacije o napredku
        stran += 1
        # Shrani podatke v datotetko
        orodja.zapisi_json(
            { "oglasi": list(OGLASI.values()) }, 
            NEPREMICNINE_JSON_DATOTEKA
        )

        print(f"Napredek: {posredovanje}/{stevilo_oglasov_v_posredovanju}")
    # Konec zanke

print(f"Podvojeni oglasi: {PODVOJENI_OGLASI}")


# Shrani podatke v datotetko
# JSON
json = {
    "oglasi": list(OGLASI.values())
}
orodja.zapisi_json(json, NEPREMICNINE_JSON_DATOTEKA)

# CSV
json_vsebina = orodja.vsebina_datoteke(NEPREMICNINE_JSON_DATOTEKA)
json = load(json_vsebina)

csv = list(json["oglasi"])
stolpci = [
    "id", 
    "tip", 
    "naslov", 
    "opis", 
    "spletna_stran", 
    "vrsta", 
    "tipi", 
    "leto", 
    "cena", 
    "velikost", 
    "atributi", 
    "agencija"
]
orodja.zapisi_csv(csv, stolpci, NEPREMICNINE_CSV_DATOTEKA)

print("Shranil!")