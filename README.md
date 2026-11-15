# UniConvert GUI

Interaktív, grafikus felületen alapuló okos mértékegység- és valutaátváltó alkalmazás Pythonban, Tkinter és saját modulos architektúrával.

## Projekt struktúra

A projekt a következő 3 fő fájlból áll a követelményeknek megfelelően:
1. **`main.py`**: A grafikus felhasználói felület (`tkinter`), az eseménykezelők, a bemenetellenőrzés és a dinamikus gombállapot-kezelés logikája.
2. **`sajat_modul_szm.py`**: A saját modul és osztály (`SzMUnitConverter`), amely az átváltási logikát (hosszúság, tömeg, hőmérséklet, valuta), a JSON alapú előzménymentést (max 20 elem) és a törlési funkciókat valósítja meg.
3. **`README.md`**: A projekt hivatalos dokumentációja.

## Főbb funkciók és extrák

- **Kategóriák**: Hosszúság (`Length`), Tömeg (`Weight`), Hőmérséklet (`Temperature`) és Valuta (`Currency`) átszámítása.
- **JSON előzménykezelés**: A konverziók automatikusan mentődnek egy helyi JSON fájlba (`conversion_history_szm.json`), és fordított sorrendben látszanak a listában.
- **Intelligens gombvédelem**: Ha a forrás és a cél mértékegység megegyezik, a "Convert" gomb automatikusan inaktívvá (szürkévé) válik, megakadályozva a felesleges műveleteket.
- **Előzmények kezelése**: 
  - Kijelölt elem egyedi törlése (*Delete*).
  - *"Ne kérdezze meg újra"* opció (Checkbox), amellyel a megerősítés átugorható a futási idő alatt.
  - Teljes előzménytörténet törlése megerősítő ablakkal (*Clear All*).

## Rendszerkövetelmények

- Python 3.x (tkinter beépített csomaggal)

## Futtatás

Válassza ki a main.py fájlt a mappában, majd futtassa a programot:

```bash
python main.py
