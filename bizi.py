import json

from bs4 import BeautifulSoup

import orodja

# Nastavitve

BIZI_PODATKI = "podatki/bizi/tabele.json"
BIZI_JSON_DATOTEKA = "podatki/bizi/podjetja.json"
BIZI_CSV_DATOTEKA = "podatki/bizi/podjetja.csv"

PODATKI = orodja.vsebina_json_datoteke(BIZI_PODATKI)

# Zbiralnik podatkov ---------------------------------------------------------

PODJETJA = dict()

for tabela in PODATKI:
    soup = BeautifulSoup(tabela, 'html.parser')

    podjetja = soup.find_all("tr")

    for podjetje in podjetja:
        informacije = podjetje.find_all("td")

        # Neznana oblika informacije.
        if len(informacije) < 6:
            continue

        ime = informacije[1].getText().strip()
        maticna_stevilka = informacije[2].getText().strip()
        obcina = informacije[3].getText().strip()
        zaposleni = informacije[4].getText().strip()
        dobicek = informacije[5].getText().strip().replace(".", "").replace(" ", "")
        if dobicek:
            dobicek = int(dobicek)
        else:
            dobicek = None

        if maticna_stevilka in PODJETJA:
            print(f"Podvojeno podjetje {ime} {maticna_stevilka}")
            continue

        PODJETJA[maticna_stevilka] = {
            "id": maticna_stevilka,
            # Podatki
            "ime": ime,
            "maticna_stevilka": maticna_stevilka,
            "obcina": obcina,
            "zaposleni": zaposleni,
            "dobicek": dobicek
        }

    # Print progress
    print(f"Našel {len(PODJETJA)} podjetji.")




# Shrani podatke v datotetko -------------------------------------------------

# JSON
json = {
    "podjetja": list(PODJETJA.values())
}
orodja.zapisi_json(json, BIZI_JSON_DATOTEKA)

# # CSV
csv = list(PODJETJA.values())
stolpci = [
    "id", 
    "ime",
    "maticna_stevilka",
    "obcina",
    "zaposleni",
    "dobicek"
]
orodja.zapisi_csv(csv, stolpci, BIZI_CSV_DATOTEKA)

print("Shranil!")
