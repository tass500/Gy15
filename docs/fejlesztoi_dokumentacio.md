# Fejlesztői dokumentáció

## Bevezetés
Ez a dokumentáció a Texas Hold'em póker játék fejlesztői számára készült, amely egy mesterséges intelligenciával játszható póker implementációja.

## Projekt struktúra

```
.
├── ai_adventure_game.py  # Fő játékfájl
├── requirements.txt      # Függőségek
└── docs/                # Dokumentációk
    ├── fejlesztoi_dokumentacio.md
    ├── tervdokumentacio.md
    ├── felhasznaloi_dokumentacio.md
    └── tesztelesi_dokumentacio.md
```

## Fő osztályok

### 1. Card osztály
- **Felelősség**: Egy kártya reprezentálása
- **Attribútumok**:
  - `suit`: A kártya színe (Suit enum)
  - `rank`: A kártya értéke (Rank enum)

### 2. Deck osztály
- **Felelősség**: Pakli kezelése
- **Főbb metódusok**:
  - `__init__`: Új pakli létrehozása
  - `shuffle`: Kártyák összekeverése
  - `draw`: Kártya húzása

### 3. PokerGame osztály
- **Felelősség**: A játék fő logikájának kezelése
- **Főbb metódusok**:
  - `play_round`: Egy kör lejátszása
  - `betting_round`: Tétkör kezelése
  - `evaluate_hand`: Kéz értékelése
  - `compare_hands`: Két kéz összehasonlítása

### 4. PokerAI osztály
- **Felelősség**: AI játékos implementációja a Hugging Face modell használatával
- **Attribútumok**:
  - `pipe`: A betöltött nyelvi modell folyamata
- **Főbb metódusok**:
  - `__init__`: Inicializálja az AI modellt a HuggingFaceH4/zephyr-7b-beta modelllel
  - `get_ai_decision`: AI döntéshozatal a játékállapot alapján

## Modell kezelése

A játék a HuggingFaceH4/zephyr-7b-beta modellt használja a mesterséges intelligencia döntéshozatalához. A modell automatikusan letöltődik az első futtatáskor.

### Modell betöltése
A modellt a `PokerAI` osztály `__init__` metódusában inicializáljuk:
```python
self.pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")
```

### Döntéshozatal
A `get_ai_decision` metódus a következő lépéseket hajtja végre:
1. Létrehoz egy promptot a játék aktuális állapotával
2. A modell generál egy választ a prompt alapján
3. A választ feldolgozza és visszaadja a döntést ('call', 'raise' vagy 'fold')

### Modell konfiguráció
- Modell: HuggingFaceH4/zephyr-7b-beta
- Generálási paraméterek:
  - `max_new_tokens`: 10
  - `do_sample`: True
  - `temperature`: 0.7

## Függőségek
- Python 3.8+
- transformers >= 4.30.0
- torch >= 2.0.0
- datasets (a modell működéséhez szükséges)
- accelerate (a modell gyorsításához)
- bitsandbytes (opcionális, 8-bit-s kvantáláshoz)

## Telepítés fejlesztői környezetben

```bash
# Klónozd le a repository-t
git clone <repo-url>
cd <project-dir>

# Virtuális környezet létrehozása és aktiválása
python -m venv venv
.\venv\Scripts\activate

# Függőségek telepítése
pip install -r requirements.txt
```

## Futtatás fejlesztői módban

```bash
python ai_adventure_game.py --debug
```

## Hibakeresés
- A `--debug` kapcsolóval részletesebb kimenetet kaphatsz
- A naplófájlok a `logs/` könyvtárban találhatók
