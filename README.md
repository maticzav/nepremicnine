# nepremicnine

Z nalogo bi rad ugotovil v kateri občini se najbolj splača postavit coworing-spacee. Zanimalo me bo v katere občine Slovenska podjetja izlijejo največji del potnih stroškov in ugotavljal

---

## Zajem podatkov

Podatke za raziskavo bom zajemal iz štirih strani.

- [nepremičnine.net](https://nepremicnine.net)
- [bizi.si](https://bizi.si)
- [stat.si](https://pxweb.stat.si/)

Za vsako nepremičnino s strani [nepremičnine.net](https://nepremicnine.net) bom zajel:

- način posredovanja
- naslov oglasa
- url do strani z oglasom
- kratek in daljši opis nepremičnine
- vrsto nepremičnine ("Poslovni prostor, Stanovanje...")
- regijo, upravno enoto ter občino v kateri nepremičnina stoji
- velikost nepremičnine v m2 in ceno
- seznam url-jev do slik
- agencijo, ki posreduje pri nepremičnini

Podatke o podjetjih bom pridobil iz strani [bizi.si](https://www.bizi.si).
O vsakem podjetju si bom zapisal:

- ime podjetja
- matično številko podjetja za identifikacijo
- občino v kateri je podjetje registrirano
- št. zaposlenih (ocena glede na spodnjo mejo, ki jo bizi.si prikaže)
- prihodek oziroma izgubo zadnjega leta (2019)

<!-- - panoge s katerimi se ukvarjajo -->

Podatke o občinah bom pridobil iz Statističnega urada RS in zemljevidov Google Maps.
O vsaki občini si bom shranil:

- ime občine

- število delovno aktivnih prebivalcev po prebivališču
- število delovno aktvnih prebivalcev po delovnem mestu
- delež delovno aktivnih prebivalcev, ki dnevno migrirajo
- delež delovno aktivnih prebivalcev, ki delajo v občini prebivališča
- število prebivalcev na 1. julij
- povprečna starost prebivalcev na 1. julij
- število vrtcev
- število otrok v vrtcih
- delež vseh otrok starih 1-5 let, ki obiskujejo vrtec
- število učencev v osnovnih šolah
- število dijakov
- povprečna mesečna plača na osebo bruto
- povprečna mesečna plača na osebo neto

- povprečen čas vožnje zjutraj (8:00)
- povprečen čas vožnje popoldan (17:00)
- razdaljo od središča občine do drugih občin

Poleg tega bom iz Statističnega urada RS pridobil še podatke o

- povprečni ceni goriva
- povprečno urno postavko glede na starostno skupino

> Povprečno urno postavko bom, predvidevam, moral izračunat glede na neto povprečno plačo s povprečnim delavnikom 4 x 5dni x 8h.

---

## Viri

#### Nrepremičnine

- https://www.nepremicnine.net/oglasi-prodaja/
- https://www.nepremicnine.net/oglasi-oddaja/
- https://www.nepremicnine.net/oglasi-nakup/
- https://www.nepremicnine.net/oglasi-najem/

> Za listanje dodaš `/n/` nakonec zgornjih naslovov. Primer `https://www.nepremicnine.net/oglasi-najem/3/`.

#### Stoja Nepremičnine

- https://www.stoja-trade.si/Nepremicnine/p33.html

> Za listanje spremeniš številjo na koncu `/pN.html`.

#### Bizi.si

Za pridobivanje podatkov iz bizi.si uporabljamo orodje Puppeteer, ki zažene headless Chrome in nam omogoča programsko upravljati spletni brskalnik. Znotraj Puppeteer-ja se prijavimo v bizi.si in izvršimo splošno iskanje, ki vrne veliko število podjetji.

Za pridobitev podatkov skripta bizi.si potrbuje podatke o dostopu, ki jih nastavimo znotraj datoteke `bizi.ts`.

#### SiStat

- https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/05C4002S.px/table/tableViewLayout2/
- https://www.gov.si/teme/cene-naftnih-derivatov/

- https://pxweb.stat.si/SiStat/sl/Home/GetSearchResultsRedirect?searchQuery=migracije&searchString=migracije

> Med delovne migrante so torej uvrščene delovno aktivne osebe (brez kmetov), za katere sta znani obe teritorialni enoti, tako tista, v kateri je delovno mesto, kot tudi tista, v kateri je prebivališče.

#### Povračilo potnih stroškov

https://mladipodjetnik.si/novice-in-dogodki/novice/obracun-prevoz-na-delo-ter-kilometrine-2

---

## Namestitev razvijalskega okolja

Zaženi naslednje ukaze, da ustvariš virtual environment v tem repositoryju in namestiš potrebne knjižnice.

```bash
python3 -m venv .
source bin/activate.fish

pip install -r requirements.txt
```
