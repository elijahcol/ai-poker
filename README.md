# Poker Lab — Windows Practice Game

A play-only Texas Hold'em learning game for Windows.

### Features
- 3 computer opponents
- Hidden hole cards for opponents
- Five community cards
- Practice-point wheel (not wagering)
- Animated practice-point score changes
- Hand evaluation
- Flop / turn / river progression
- Fold Practice and Check
- No money, betting, deposits, or cash-out system

Texas Hold'em uses two private cards and five community cards, with the best five-card hand determining the result. Standard hand rankings are used.

## Run

Install Python 3 and run:

```bash
python poker_lab.py
```

## Build Windows EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name PokerLab poker_lab.py
```

The executable will be:

`dist/PokerLab.exe`

## GitHub Actions

The included workflow builds the Windows executable automatically.
