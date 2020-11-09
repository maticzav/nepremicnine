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



### Obdelava podatkov

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
