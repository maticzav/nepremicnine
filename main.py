from bs4 import BeautifulSoup
import os

import orodja

# Nastavitve

NEPREMICNINE_NASLOV = 'https://www.nepremicnine.net'
STEVILO_OGLASOV = {
    "najem": 358,
    "oddaja": 4700,
    "nakup": 2100,
    "prodaja": 20100,
}
NEPREMICNINE_JSON_DATOTEKA = "podatki/nepremicnine.json"
NEPREMICNINE_CSV_DATOTEKA = "podatki/nepremicnine.csv"

# Zbiralnik podatkov

oglasi = dict() # slovar oglasov identificiranih z id-jem

"""
Posamezen oglas, ki ga preberemo ima sledečo obliko:

type Oglas {
    id: string

    # Informacije o oglasu
    tip: 'najem' | 'oddaja' | 'nakup' | 'prodaja'
    naslov: string
    opis: string
    spletna_stran: string

    # Podrobnosti oglasa
    vrsta: string "stanovanje"
    tipi: string "stirisobno"
    leto: string
    cena: string
    velikost: string

    # Dodatne informacije
    atributi: string
    agencija: string
}
"""

podvojeni_oglasi = set() # zabeležimo si vse podvojene oglase

for domena in STEVILO_OGLASOV:

    # Podatki o domeni
    STEVILO_OGLASOV_V_DOMENI = STEVILO_OGLASOV[domena]

    # Podatki o napredku
    stevilo_oglasov = 0
    stran = 1

    while stevilo_oglasov < STEVILO_OGLASOV_V_DOMENI:
        # Podatki o strani
        url = f'{NEPREMICNINE_NASLOV}/oglasi-{domena}/{stran}/'
        datoteka = f'podatki/nepremicnine/{domena}/{stran}.html'

        # Naloži stran
        orodja.shrani_spletno_stran(url, datoteka)
        vsebina = orodja.vsebina_datoteke(datoteka)

        # Analiziraj podatke
        soup = BeautifulSoup(vsebina, 'html.parser')
        oglasi_na_strani = soup.find_all("div", class_="oglas_container")

        # Preveri vsebino podatkov
        if len(oglasi_na_strani) == 0:
            raise ValueError('Ni več oglasov v {domena}. Zbrano {stevilo_oglasov}/{STEVILO_OGLASOV_V_DOMENI}')

        # Analiziraj posamezen oglas
        for oglas in oglasi_na_strani:

            # Oglas
            id = oglas.get('id')

            # Preveri ali oglas že obstaja
            if oglasi.get(id):
                podvojeni_oglasi.add(id)
                continue
                # raise ValueError(f'Podvojen oglas {id} v {domena} na strani {stran}.')

            # Informacije o oglasu
            tip = domena
            naslov = oglas.find("span", class_="title").string
            opis = getattr(oglas.find("div", itemprop="description"), "string", None)
            spletna_stran = f"{NEPREMICNINE_NASLOV}{oglas.find('a')['href']}"
            
            # Podrobnosti oglasa
            vrsta = oglas.find("span", class_="vrsta").string
            tipi = getattr(oglas.find("span", class_="tipi"), "string", None)
            leto = getattr(oglas.find("span", class_="leto"), "string", None)
            cena = oglas.find("span", class_="cena").string
            velikost = oglas.find("span", class_="velikost").string
            
            # Dodatne informacije
            atributi = oglas.find("div", class_="atributi").string
            agencija = oglas.find("span", class_="agencija").string

            # Zabeleži oglas
            oglasi[id] = {
                "id": id,

                # Informacije o oglasu
                "tip": tip,
                "naslov": naslov,
                "opis": opis,
                "spletna_stran": spletna_stran,

                # Podrobnosti oglasa
                "vrsta": vrsta,
                "tipi": tipi,
                "leto": leto,
                "cena": cena,
                "velikost": velikost,

                # Dodatne informacije
                "atributi": atributi,
                "agencija": agencija
            }

        # Posodobi informacije o napredku
        stran += 1
        stevilo_oglasov += len(oglasi_na_strani)

        print(f"Napredek: {domena}/{stevilo_oglasov}/{STEVILO_OGLASOV_V_DOMENI}")

    print(f"Našel {stevilo_oglasov} oglasov v {domena}!")

print(f"Podvojeni oglasi: {podvojeni_oglasi}")


# Shrani podatke v datotetki
json = {
    "oglasi": list(oglasi.values())
}
orodja.zapisi_json(json, NEPREMICNINE_JSON_DATOTEKA)

csv = list(oglasi.values())
stolpci = ["id", "tip", "naslov", "opis", "spletna_stran", "vrsta", "tipi", "leto", "cena", "velikost", "atributi", "agencija"]
orodja.zapisi_csv(csv, stolpci, NEPREMICNINE_CSV_DATOTEKA)

print(f"Shranil {sum(STEVILO_OGLASOV.values())} oglasov.")