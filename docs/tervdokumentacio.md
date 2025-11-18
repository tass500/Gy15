# Tervezési dokumentáció

## 1. Bevezetés
Ez a dokumentum a Texas Hold'em póker játék tervezését és fejlesztését dokumentálja.

## 2. Célok
- Felhasználóbarát, szórakoztató póker játék készítése
- Mesterséges intelligencia implementálása ellenfélként
- Valósághű póker szabályok implementálása

## 3. Funkcionális követelmények

### 3.1 Játékmenet
- [x] Kártyaosztás
- [x] Tétkörök kezelése (pre-flop, flop, turn, river)
- [x] Kézértékelés
- [x] Nyertes meghatározása

### 3.2 Felhasználói felület
- [x] Konzolos felület
- [ ] Grafikus felület (jövőbeli fejlesztés)
- [ ] Hanghatások (jövőbeli fejlesztés)

### 3.3 AI játékos
- [x] Alapvető döntéshozatal
- [ ] Stratégia szintek (kezdő, haladó, profi)
- [ ] Tanuló képesség (jövőbeli fejlesztés)

## 4. Nem funkcionális követelmények
- Teljesítmény: A játéknak akár 10 éves számítógépen is futnia kell
- Használhatóság: Könnyen érthető kezelőfelület
- Biztonság: A játék ne legyen sebezhető a csalásra

## 5. Technológiai verem
- Programozási nyelv: Python 3.8+
- Könyvtárak:
  - transformers: AI modell kezeléséhez
  - torch: Gépi tanulási műveletekhez
  - random: Kártyák keveréséhez

## 6. Fejlesztési fázisok

### 1. Alapok (1 hét)
- [x] Kártya és pakli osztályok implementálása
- [x] Alap játékmenet megvalósítása
- [x] Egyszerű konzolos felület

### 2. AI integráció (1 hét)
- [x] Alap AI implementálása
- [x] Döntéshozatali mechanizmus

### 3. Tesztelés és finomhangolás (3 nap)
- [ ] Egységtesztek
- [ ] Teljesítménytesztek
- [ ] Felhasználói tesztelés

## 7. Kockázatok és megoldásaik

| Kockázat | Lehetséges hatás | Megelőzési/kezelési terv |
|----------|------------------|--------------------------|
| Lassú AI válasz | Rossz felhasználói élmény | Kisebb modell használata, gyorsítótárazás |
| Memória túlcsordulás | Összeomlás | Memóriahasználat optimalizálása |
| Biztonsági rések | Csalási lehetőség | Input validáció, kód áttekintés |

## 8. Jövőbeli bővítések
- Többjátékos mód hálózaton keresztül
- Ranglista és statisztikák
- Grafikus felület
- Mobil alkalmazás változat
