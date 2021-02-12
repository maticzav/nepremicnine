import googlemaps
from bs4 import BeautifulSoup
import math

import orodja

# Nastavitve -----------------------------------------------------------------

MAPS_API_KEY = ""

MAPS_OBCINE_PODATKI = "../../podatki/sistat/obcine.html"

MAPS_JSON_DATOTEKA = "../../podatki/razdalje.json"
MAPS_CSV_DATOTEKA = "../../podatki/razdalje.csv"

# Obdelava -------------------------------------------------------------------

vsebina_obcin = orodja.vsebina_datoteke(MAPS_OBCINE_PODATKI)
soup_obcine = BeautifulSoup(vsebina_obcin, 'html.parser')

# Seznam občin v Sloveniji

obcine = []

for obcina in soup_obcine.select("tbody tr"):

    # Obdelaj vsako občino posebaj
    vrstica = obcina.find_all("td")
    ime = vrstica[0].getText()

    obcine.append(ime)
  

# Podatki o razdaljah

gmaps = googlemaps.Client(key=MAPS_API_KEY)

# geocodes = []

# for obcina in obcine:
#     geocode = gmaps.geocode(f"{obcina}")

#     geocodes.append({
#         "obcina": obcina,
#         "geocode": geocode
#     })

RAZDALJE = []

for zacetek in obcine:
    for konec in obcine:
        # Razdalje občine same do sebe ne potrebujemo.
        if zacetek == konec:
            continue

        # Izračunaj razdaljo
        razdalja = None

        # Poglej če že imamo podatek v obratni smeri.
        for shranjena_razdalja in RAZDALJE:
            if shranjena_razdalja["konec"] == zacetek and shranjena_razdalja["zacetek"] == konec:
                razdalja = shranjena_razdalja

        # Pridobi podatek iz googla.
        if not razdalja:
            grazdalja = gmaps.distance_matrix(
                origins=zacetek,
                destinations=konec,
                mode="driving",
                units="metric",
                region="si"
            )
            podatki = grazdalja["rows"][0]["elements"][0]

            if podatki["status"] == "ZERO_RESULTS":
                print(f"Ni podatka za {zacetek} in {konec}")
                continue

            if podatki["distance"]["value"] > 500_000:
                print("WARNING! 1000km distance.")

            razdalja = {
                # Razdalja je podana v metrih.
                "razdalja": podatki["distance"]["value"],
                # Čas je podan v sekundah.
                "cas": podatki["duration"]["value"]
            }

        RAZDALJE.append({
            "zacetek": zacetek,
            "konec": konec,
            # Razdalja je podana v metrih.
            "razdalja": razdalja["razdalja"],
            # Čas je podan v sekundah.
            "cas": razdalja["cas"]
        })

        # Shrani podatke
        json = { "razdalje": RAZDALJE }
        orodja.zapisi_json(json, MAPS_JSON_DATOTEKA)

        kms = math.floor(razdalja["razdalja"] / 1000)

        print(f"Shranil razdaljo med {zacetek} in {konec}: {kms}km")





# Shrani podatke v datotetko -------------------------------------------------

# JSON
json = { "razdalje": RAZDALJE }
orodja.zapisi_json(json, MAPS_JSON_DATOTEKA)

# CSV
orodja.zapisi_csv(RAZDALJE, [ "zacetek", "konec", "razdalja", "cas" ], MAPS_CSV_DATOTEKA)

print("Shranil!")
