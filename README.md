# WordleGuessing

WordleGuessing is a small desktop helper for narrowing down Wordle answers. You enter one
five-letter guess, mark each tile as gray, yellow, or green, and the app filters the
remaining candidates for the next guess.

## How To Use

1. Type a five-letter guess into the tile row.
2. Use `Space` to cycle a tile color, or press `1`, `2`, or `3` for gray, yellow, and green.
3. Press `Enter` or click `Submit Guess` to filter the word list.
4. Click `New Puzzle` when you want to reset the solver for a fresh game.

## Keyboard Shortcuts

- `A-Z`: enter letters and advance focus
- `Backspace`: clear the current tile, or move left and clear the previous tile
- `Left` / `Right`: move between tiles
- `Space`: cycle tile color
- `1` / `2` / `3`: set gray / yellow / green directly
- `Enter`: submit the current guess

## Run From Source

Install Python 3.12 or newer, then:

```powershell
python -m pip install -e .[dev]
python -m pytest -q
python -m source_code
```

You can also launch the packaged entrypoint after installation with `wordleguessing`.

## Shareable Windows Build

The first shareable release target is a zipped PyInstaller `onedir` build so friends can unzip
and double-click the app without installing Python.

```powershell
python -m pip install -e .[dev]
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

The build script writes the release bundle to `release\WordleGuessing-windows.zip`.

## Development Checks

```powershell
python -m pytest -q
python -m ruff check .
python -m mypy
```

## Notes

- The bundled word list is loaded from package resources, so startup does not depend on the
  current working directory.
- Mutable app data belongs under `%LOCALAPPDATA%\WordleGuessing`.
- Local `pickle` caching was intentionally removed for safety and simplicity.
