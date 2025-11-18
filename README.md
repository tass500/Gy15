# AI Póker Játék

Ez egy egyszerű Texas Hold'em póker játék, ahol egy mesterséges intelligenciával játszhatsz. A játék Python nyelven íródott és a `transformers` könyvtárat használja az AI játékos megvalósításához.

## Követelmények

A játék futtatásához a következők szükségesek:
- Python 3.8 vagy újabb
- Internetkapcsolat (csak az első futtatáshoz, a modell letöltéséhez)

## Telepítés

1. Klónozd le a repository-t vagy töltsd le a forráskódot
2. Telepítsd a szükséges csomagokat a következő paranccsal:
   ```bash
   pip install -r requirements.txt
   ```

## Futtatás

A játék indításához futtasd a következő parancsot a parancssorban:

```bash
python ai_adventure_game.py
```

## Játék menete

1. Minden játékos 1000 zsetonnal kezd
2. A játék körökre oszlik, minden körben új lapokat osztanak
3. A játékosok felváltva tétet tehetnek, emelhetnek vagy passzolhatnak
4. A játék addig tart, amíg az egyik fél el nem fogy a zsetonokból

## Játékvezérlés

- `call` - A tét megegyezése
- `raise` - Tét emelése (a program kérni fogja az emelés mértékét)
- `fold` - Passz (kártyák eldobása, a kör vége)

## Megjegyzés

Az első futtatáskor a program letölti az AI modellt (kb. 2-3 GB), ami néhány percig is eltarthat a kapcsolat sebességétől függően. Ezután a modell a gépeden lesz elérhető, és nem lesz szükség internetkapcsolatra.

## Modell kezelése

A letöltött modellfájlok a következő helyen találhatók:
```
C:\Users\[felhasználónév]\.cache\huggingface\hub
```

### Modell törlése
A modellfájlok törléséhez töröld a fenti mappát. Ez felszabadítja a lemezterületet, de a játék újraindításakor újra letöltődik a modell.

A `transformers` csomag eltávolításához futtasd a következő parancsot:
```bash
pip uninstall transformers
```

### Alternatív modell használata
A programban a `ai_adventure_game.py` fájlban módosíthatod a használt modell nevét a `model_name` változóban.

## Hibaelhárítás

Ha problémád lenne a modell letöltésével, próbáld meg a következőket:
1. Ellenőrizd az internetkapcsolatodat
2. Győződj meg róla, hogy van elegendő szabad hely a merevlemezeden (legalább 5 GB)
3. Ha a letöltés megszakad, egyszerűen indítsd újra a programot, és folytatja a letöltést onnan, ahol abbahagyta
