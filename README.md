# nepremicnine

Analiziral bom oglase za prodajo in najem nepremičnin v večjih Slovenskih mestih na strani [Nepremičnine.net](http://nepremicnine.net/) in podatke združil z informacijami o naseljenosti posameznih regij v katerih nepremičnine stojijo ter odaljenost od prometnic in večjih mest.

### Zajem podatkov

Za vsako nepremičnino bom zajel:

- naslov in datum objave oglasa
- velikost stanovanja ter število sob
- ceno najema oziroma prodajno ceno
- kraj nepremičnine
- tip nepremičnine (poslovni prostor, kmetijsko zemljišči, bivalni prostor)

Podatke o odaljenosti od prometnic bom zajemal s pomočjo Google Maps.
Glede na razdaljo bom ocenil predviden čas in razdaljo vožnje na delo, ki ju bom ocenil glede na povprečno ceno goriva in urno postavko delavca v Sloveniji.

Podatke o gorivih in urnih postavkah bom pridobil iz:

- https://www.gov.si/teme/cene-naftnih-derivatov/
- https://www.stat.si/statweb
- https://pxweb.stat.si/SiStat/sl

Podatke o podjetjih bom pridobil iz strani [bizi.si](https://www.bizi.si).
O vsakem podjetju si bom zapisal:

- naslov (kraj)
- št. zaposlenih
- ime podjetja
- panoge s katerimi se ukvarjajo
- prihodek zadnjih treh let

Podatke o dnevnih migracijah bom pridobil iz Statističnega urada RS.

### Viri

#### Nrepremičnine

- https://www.nepremicnine.net/oglasi-prodaja/
- https://www.nepremicnine.net/oglasi-oddaja/
- https://www.nepremicnine.net/oglasi-nakup/
- https://www.nepremicnine.net/oglasi-najem/

> Za listanje dodaš `/n/` nakonec zgornjih naslovov. Primer `https://www.nepremicnine.net/oglasi-najem/3/`.

#### Stoje Nepremičnine

- https://www.stoja-trade.si/Nepremicnine/p33.html

> Za listanje spremeniš številjo na koncu `/pN.html`.

#### Bizi.si

Za pridobivanje podatkov iz bizi.si uporabljamo orodje Puppeteer, ki zažene headless Chrome in nam omogoča programsko upravljati spletni brskalnik. Znotraj Puppeteer-ja se prijavimo v bizi.si in izvršimo splošno iskanje, ki vrne veliko število podjetji.

Za pridobitev podatkov skripta bizi.si potrbuje podatke o dostopu, ki jih nastavimo znotraj datoteke `bizi.ts`.

### Obdelava podatkov

Izračunal bom:

- povprečno ceno na kvadratni meter nepremičnine v dani občini ter primerjal podatke o ceni nepremičnin med občinami,
- razdaljo med posameznimi občinami ter ocenil stroške tranzita med občinami ter povprečni čas tranzita,
- povprečno ceno najema poslovnih prostorov v posamezni občini,
- analizral podjetja z največjim dobičkom glede na občine,
- ocenil absolutni delež ljudi v tranzitu znotraj posamezne firme na podlagi podatkov o dnevnih migracijah,
- ocenil skupno vrednost dnevnih migracij glede na čas in stroške prometa posamezne občine ter pri tem upošteval koliko denarja ljudje v tranzitu porabijo v povprečju v drugi občini.

Delovne hipoteze:

- Ali obstaja povezava med povprečno najemnino in prodajno ceno nepremičnin.
- Kolikšen bi moral bit dodatek k plči glede na odaljenost od delovnega mesta za obdobje 10 let.
- Katere občine delajo največjo izgubo z dnevnimi migracijami.

---

## Namestitev razvijalskega okolja

Zaženi naslednje ukaze, da ustvariš virtual environment v tem repositoryju in namestiš potrebne knjižnice.

```bash
python3 -m venv .
source bin/activate.fish

pip install -r requirements.txt
```
