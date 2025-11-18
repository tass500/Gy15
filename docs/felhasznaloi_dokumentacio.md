# Felhasználói dokumentáció

## Tartalomjegyzék
1. [Bevezetés](#bevezetés)
2. [Telepítés](#telepítés)
3. [Játék indítása](#játék-indítása)
4. [Játékmenet](#játékmenet)
5. [Vezérlés](#vezérlés)
6. [Póker kezek értékelése](#póker-kezek-értékelése)
7. [Gyakori kérdések](#gyakori-kérdések)

## Bevezetés

Üdvözöljük a Texas Hold'em póker játékban! Ez a dokumentáció segít megismerkedni a játék használatával és szabályaival.

## Telepítés

1. Győződjön meg róla, hogy a számítógépén telepítve van a Python 3.8 vagy újabb verzió
2. Töltse le a játék forráskódját
3. Telepítse a szükséges csomagokat:
   ```bash
   pip install -r requirements.txt
   ```

### Rendszerkövetelmények
- Legalább 16GB RAM ajánlott a modell betöltéséhez
- Internetkapcsolat szükséges az első futtatáshoz a modell letöltéséhez
- Körülbelül 10GB szabad lemezterület szükséges a modell tárolásához

## Játék indítása

A játék indításához futtassa a következő parancsot a parancssorban:

```bash
python ai_adventure_game.py
```

Az első indításkor a program letölti a szükséges AI modellt, ami néhány percig is eltarthat az internetkapcsolat sebességétől függően. A modell a következő helyre kerül mentésre:
- Windows: `C:\Users\[felhasználónév]\.cache\huggingface\hub`
- Linux/Mac: `~/.cache/huggingface/hub`

## Játékmenet

A játék a következő fázisokból áll:

1. **Pre-flop**
   - Mindkét játékos kap 2 lapot
   - Első tétkör

2. **Flop**
   - 3 közös lap kerül az asztalra
   - Második tétkör

3. **Turn**
   - Negyedik közös lap kerül ki
   - Harmadik tétkör

4. **River**
   - Ötödik közös lap kerül ki
   - Negyedik tétkör

5. **Showdown**
   - A játékosok felfedik a kártyáikat
   - A nyertes megkapja a kasszát

## Vezérlés

A játék során a következő parancsokat használhatja:

- `call` - Tartás (megegyeztetés az aktuális tétbehívással)
- `raise` - Emelés (növeli a tétet)
- `fold` - Passz (kártyák eldobása, a körből való kiszállás)

### AI játékos viselkedése

Az AI játékos a következőket veszi figyelembe döntése során:
- Saját kártyáinak erősségét
- A közös kártyákat (flop, turn, river)
- A játék aktuális állását (tétek, stack méretek)

Az AI válaszideje néhány másodperc lehet, amíg a modell feldolgozza a kérést.

## Póker kezek értékelése

A kezek erősségi sorrendje (legjobb a legfelső):

1. **Royal Flush** - 10-J-Q-K-A azonos színben
2. **Straight Flush** - Öt egymást követő lap azonos színben
3. **Póker** - Négy azonos értékű lap
4. **Full** - Pár + drill egy kézben
5. **Flush** - Öt azonos színű lap
6. **Sor** - Öt egymást követő lap
7. **Drill** - Három azonos értékű lap
8. **Két pár** - Két különböző pár
9. **Pár** - Két azonos értékű lap
10. **Magas lap** - A legmagasabb lap a kezében

## Gyakori kérdések

### Hogyan tudok új játékot kezdeni?
Egyszerűen indítsa újra a programot, vagy lépjen ki a játékból a `kilépés` paranccsal, majd indítsa újra.

### Mi történik, ha nincs elég zsetonom?
Ha egy játékosnak nincs elég zsetonja a tét megegyezéséhez, "all-in" kerül, és csak a saját zsetonjáig tarthat a tétben.

### Hogyan tudom megnézni az aktuális szabályokat?
A játék során bármikor írja be a `szabalyok` parancsot a játékmenetben a szabályok megtekintéséhez.

### Hogyan működik az AI?
Az AI a játék állapotát elemzi, és a keze ereje, a kassza mérete és a játékos viselkedése alapján hoz döntéseket.

### Hol találom a játék mentéseimet?
A jelenlegi verzió nem támogatja a játék mentését, de ez a funkció a jövőben hozzáadásra kerülhet.
