# Windows Poker

A simple **play-money Texas Hold'em-style poker game for Windows**, written in Python with Tkinter.

## Features
- Player vs computer
- Flop, turn and river
- Hand evaluation
- Fold, check and 50-chip bet
- Play-money chips only
- No internet connection required

## Run from source

Install Python 3, then:

```bash
python poker.py
```

## Build the `.exe`

Install PyInstaller:

```bash
pip install pyinstaller
```

Then:

```bash
pyinstaller --onefile --windowed --name WindowsPoker poker.py
```

The finished executable will be in:

`dist/WindowsPoker.exe`

## GitHub

Upload the project files to a GitHub repository. You can also add the GitHub Actions workflow in `.github/workflows/build.yml` to automatically build the Windows `.exe`.
