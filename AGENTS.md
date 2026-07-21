# AGENTS.md

## Cursor Cloud specific instructions

This repo is a small collection of standalone Python 3 command-line scripts (a Rubik's Cube move/analysis toolkit). There are no long-running services, servers, databases, build system, linter, or automated test suite.

### Running the scripts
- Always run from the repo root. `TestMoves.py`, `Test_Moves_HTM.py`, and `TestPerformance.py` load `mappings*.json` from the current working directory (so CWD must be the repo root), while the cube start state (`csv_export-StartPos.csv`) is loaded relative to the script file itself.
- Most scripts read moves interactively via `input()`. For non-interactive runs, pipe stdin, e.g. `printf "R U R'\nstop\n" | python3 Test_Moves_HTM.py`.
- `TestPerformance.py` prompts for three integers (moves per sequence, iterations per run, runs): `printf "50\n1000\n2\n" | python3 TestPerformance.py`.
- Correctness sanity check: applying any face move 4x returns to the start position (e.g. `printf "R R R R\nstop\n" | python3 Test_Moves_HTM.py` yields the starting cube).

### GUI / clipboard scripts (non-obvious)
- `Transfom_HTM_single.py` reads the move sequence from the system clipboard via `pyperclip`; it needs a display and a clipboard backend (`xclip`/`xsel`). The VM has `DISPLAY=:1` and `xclip` available. Seed input with `printf "..." | DISPLAY=:1 xclip -selection clipboard` before running. With an empty clipboard it runs but produces zero moves.
- `Stats_Plot.py` opens a Tkinter file-picker dialog (`filedialog.askopenfilename`), so it requires `python3-tk` and a display; it blocks on file selection. To render a plot headlessly you can run its plotting code path with `MPLBACKEND=Agg` against a stats CSV (e.g. `Stats.csv`).

### Dependencies
- Python deps are in `requirements.txt` (`numpy pandas matplotlib seaborn pyperclip`). System package `python3-tk` is required only for `Stats_Plot.py`'s GUI dialog and is not pip-installable.
