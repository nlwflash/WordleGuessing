# Windows Release Guide

## Prerequisites

- Windows
- Python 3.12+
- The dev dependencies installed with `python -m pip install -e .[dev]`

## Build Steps

1. Run the test suite.
2. Run Ruff and mypy.
3. Build the PyInstaller `onedir` package.
4. Zip the output for sharing.

```powershell
python -m pytest -q
python -m ruff check .
python -m mypy
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

## Output

The release script creates:

- `release\dist\WordleGuessing\`
- `release\WordleGuessing-windows.zip`

## Manual Smoke Check

1. Copy `release\WordleGuessing-windows.zip` to a clean Windows machine.
2. Unzip it anywhere outside the source repository.
3. Launch `WordleGuessing.exe`.
4. Enter several guesses, confirm candidate words are sorted, then click `New Puzzle`.
5. Confirm the app resets without restarting.
