# Sportinės gimnastikos rezultatų sistema

Ši Streamlit aplikacija skirta sportinės gimnastikos varžybų rezultatų skaičiavimui pagal dviejų teisėjų vertinimus. Ji leidžia:

- Įkelti du Excel failus su teisėjų vertinimais (vienoda struktūra),
- Apskaičiuoti D ir E balų vidurkį,
- Sugeneruoti galutinį rezultatą,
- Rikiuoti dalyvius ir priskirti vietas,
- Atsisiųsti rezultatus kaip PDF ir Excel dokumentus.

##  Naudojimas

1. Paleisk aplikaciją su Streamlit:
```
streamlit run app.py
```

2. Įkelk:
- `DejaVuSans.ttf` šriftą PDF generavimui su lietuviškomis raidėmis
- Du Excel failus: vieną nuo kiekvieno teisėjo

3. Pasirink rungtį, programą ar komandą.
4. Atsisiųsk rezultatus kaip PDF ar Excel failą.

##  Excel reikalavimai

- Abu failai turi būti su vienoda struktūra (tie patys stulpeliai).
- Kiekviena rungtis turi būti atskirame lapelyje.
- Privalomi stulpeliai: `Programa`, `Komanda`, `D`, `E` (su dalyvių info).

##  Priklausomybės

Nurodytos `requirements.txt` faile. Diegti galima su:
```
pip install -r requirements.txt
```

##  Paleidimas naršyklėje

Ši aplikacija puikiai veikia su [Streamlit Cloud](https://streamlit.io/cloud).
