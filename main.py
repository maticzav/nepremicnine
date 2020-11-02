from bs4 import BeautifulSoup

import orodja

# Nastavitve

NEPREMICNINE_NASLOV = 'https://www.nepremicnine.net'
STEVILO_OGLASOV = {
    "najem": 358,
    "oddaja": 4700,
    "nakup": 2100,
    "prodaja": 20100,
}

# Zbiralnik podatkov

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
        oglasi = soup.find_all("div", class_="oglas_container")

        # Preveri vsebino podatkov
        if len(oglasi) == 0:
            raise ValueError('Ni več oglasov v {domena}. Zbrano {stevilo_oglasov}/{STEVILO_OGLASOV_V_DOMENI}')

        # Analiziraj posamezen oglas
        

        # Posodobi informacije o napredku
        stran += 1
        stevilo_oglasov += len(oglasi)

        print(f"Napredek: {domena}/{stevilo_oglasov}/{STEVILO_OGLASOV_V_DOMENI}", end=" ")

    print(f"Našel {stevilo_oglasov} oglasov v {domena}!")


