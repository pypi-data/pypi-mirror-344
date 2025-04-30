# pip-sequencer

[![PyPI version](https://badge.fury.io/py/pip-sequencer.svg)](https://badge.fury.io/py/pip-sequencer)

**Record, replay, and export pip/uv installation sequences with user-selectable backend to ensure consistent and reproducible Python environments, especially when package installation order is critical.**

## Project description

Standard `pip freeze > requirements.txt` captures the final state of your environment but loses the *history* and *sequence* of how packages were installed. In complex projects, the order in which packages are installed can sometimes affect dependency resolution, leading to subtle differences or "works on my machine" issues when setting up the environment elsewhere.

### The Problem

Standard `pip freeze > requirements.txt` captures the final state of your environment but loses the *history* and *sequence* of how packages were installed. In complex projects, the order in which packages are installed can sometimes affect dependency resolution, leading to subtle differences or "works on my machine" issues when setting up the environment elsewhere.

### The Solution: `pip-sequencer`

`pip-sequencer` (aliased as `ps`) acts as a wrapper around `pip install`/`uninstall` or `uv pip install`/`uninstall`. It meticulously logs:

* **Which packages you explicitly install** and the exact versions the backend (`pip` or `uv`) resolves for them.
* **Which packages you explicitly uninstall**.
* **The order** in which you perform these actions.

This recorded history allows you to recreate the environment by replaying the installations *in the same sequence*, using the backend you choose, significantly increasing reproducibility.

## Key Features

* **Sequential Recording:** Logs `install` and `uninstall` operations chronologically.
* **Version Pinning:** Automatically records the installed version during `install` actions.
* **User-Selectable Backend:** Choose to execute installs/uninstalls/replays using either `pip` (default) or `uv` (if installed).
* **Command Alias:** Use the shorter `ps` command for convenience.
* **History File:** Stores the detailed sequence in a human-readable JSON file (`.pip_sequence.json`).
* **Environment Replay:** Reinstalls packages sequentially using the recorded history or an export file, with your chosen backend (`replay` command).
* **State Export:** Generates a filtered sequence file (`pip_sequence_export.json`) containing only the install steps relevant to the *currently installed* packages (`export` command).
* **Standard Freeze Output:** Creates a regular `requirements_frozen.txt` alongside the export for compatibility.
* **Command-Line Interface:** Simple wrapper commands (`ps install`, `ps uv install`, `ps uninstall`, etc.).

## Installation

Install `pip-sequencer` directly from PyPI:

```bash
pip install pip-sequencer
```

To use the `uv` backend, you also need to install `uv` separately:

```bash
# Example using pip:
pip install uv
# Or follow official uv installation instructions: https://github.com/astral-sh/uv
```

## Usage Guide

**Important:** Always use `ps` (or `pip-sequencer`) within an activated Python virtual environment for the project you want to manage.

**Command Structure:**

```
ps [BACKEND] ACTION [OPTIONS] [PACKAGES] [-- <backend_args>]
```

* **`ps`**: The command (or use `pip-sequencer`).
* **`[BACKEND]`**: Optional. Specify `uv` or `pip`. If omitted, defaults to `pip` for actions that need a backend.
* **`ACTION`**: Required. One of `install`, `uninstall`, `replay`, `export`.
* **`[OPTIONS]`**: Options specific to the `ps` ACTION (e.g., `--from-export`, `--start`).
* **`[PACKAGES]`**: Packages for `install`/`uninstall`.
* **`-- <backend_args>`**: Optional. Arguments passed directly to the underlying `pip` or `uv pip` command (must come after `--`).

### 1. Activate Your Environment:

```bash
# Example:
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# .\ .venv\Scripts\activate  # Windows
```

### 2. Recording Installations

Use `ps [BACKEND] install ...`

```bash
# Install using pip (default backend)
ps install requests
ps install "flask>=2.0,<3.0"

# Install using uv backend (requires uv installed)
ps uv install django djangorestframework

# Install using pip explicitly, passing args to pip install
ps pip install colorama -- --no-cache-dir --upgrade

# Install from requirements file using uv
ps uv install -r requirements.txt
```

* This executes the install using the chosen backend and logs the action to `.pip_sequence.json`.

### 3. Recording Uninstallations

Use `ps [BACKEND] uninstall ...`

```bash
# Uninstall using pip (default)
ps uninstall requests

# Uninstall using uv
ps uv uninstall django djangorestframework

# Explicitly use pip, pass args to pip uninstall
ps pip uninstall colorama -- --no-save
```

* This executes the uninstall using the chosen backend and logs the action to `.pip_sequence.json`.

### 4. Exporting the Current Sequence (`ps export`)

This command is backend-independent as it only reads history and checks the environment.

```bash
# Creates pip_sequence_export.json and requirements_frozen.txt
ps export

# Specify custom output/history files
ps export -o my_final_sequence.json
ps --file old_history.json export
```

* Reads history, checks installed packages, creates export files.

### 5. Replaying Installations (`ps [BACKEND] replay ...`)

Use this command in a **new, clean virtual environment** to recreate the setup. Choose the backend you want to use for the replay installation process.

```bash
# Activate the NEW clean environment first!
# source new_env/bin/activate
# pip install pip-sequencer # Install ps in the new env
# pip install uv # Optional: Install uv if you want to replay using it

# Option A: Replay installs from history using pip (default)
# (Copies .pip_sequence.json or uses --file)
ps replay

# Option B: Replay installs from history using uv
ps uv replay

# Option C: Replay from export file using pip (default)
# (Copies pip_sequence_export.json or uses path)
ps replay --from-export
ps replay --from-export my_final_sequence.json

# Option D: Replay from export file using uv
ps uv replay --from-export

# Replay specific sequence ranges (applies to the file being read)
ps pip replay --start 5 --end 10 # Explicit pip
ps uv replay --from-export --start 2
```

* Reads the specified file and runs `pip install` or `uv pip install` sequentially based on the chosen backend.

## Generated Files Explained

* **.pip_sequence.json** (Default name)
  * **Purpose:** Complete log of all recorded `install`/`uninstall` actions performed via `ps`. Contains timestamps, original commands, and results (package==version for installs).
  * **Handling:** **Commit this file to version control.** It's the source of truth for your project's setup history.

* **pip_sequence_export.json** (Default name)
  * **Purpose:** A filtered sequence generated by the `export` command. Contains only the `install` steps from the history whose explicitly recorded packages were still installed at the time of export. Preserves original sequence numbers.
  * **Handling:** **Commit this file to version control.** Useful for recreating the *final* state sequentially.

* **requirements_frozen.txt**
  * **Purpose:** Standard `pip freeze` output generated alongside the export file. Lists all installed packages (including dependencies) with exact versions.
  * **Handling:** Optional. Useful for compatibility or comparison, but **lacks sequence info**. You might commit it or add it to `.gitignore`, depending on whether the export JSON is your primary sequenced definition.

## Limitations & Considerations

* **Requires Explicit Use:** Only tracks actions performed via `ps` or `pip-sequencer` commands. Direct `pip` calls, `uv` calls outside `ps`, editable installs (`pip install -e .`), or tools like `conda`, `poetry`, `pdm` are not tracked.
* **Backend Availability:** Using the `uv` backend requires `uv` to be installed and accessible in the system's PATH. The tool will error if `uv` is requested but not found.
* **Dependency Nuances:** While sequence helps, the chosen backend's (`pip` or `uv`) dependency resolution can still vary based on package availability changes on PyPI between recording and replay.
* **Parsing Limitations:** Complex requirements (VCS links, URLs, local paths) might not have their versions perfectly auto-detected and recorded, although the install itself should proceed via the backend.
* **Uninstall Tracking:** Only records the *request* to uninstall specific packages. It does not track precisely which dependencies the backend might have removed. Replay *does not* perform uninstalls.
* **Export Scope:** `export` includes install steps only if the *explicitly* installed package from that step is still present. Dependencies installed implicitly are not included in the export sequence file (but are in `requirements_frozen.txt`).

## Contributing

Contributions, bug reports, and feature requests are welcome! Please check the [Issues page](https://github.com/Rahil-Maniar/pip-sequencer/issues) on GitHub.

To contribute code:
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests if applicable.
4. Submit a pull request.