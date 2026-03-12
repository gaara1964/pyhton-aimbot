 Python Aimbot (Learning Project)

FREE FIRE Aimbot | mem editing ✨

A Windows-only Python memory editing project that attaches to `HD-Player` and applies AoB-based runtime patches from hotkeys.

## Author

- **Muhammad Saad**
- GitHub: [@gaara1964](https://github.com/gaara1964)

## What This Project Does

This project includes:

- A console dashboard with hotkey controls.
- Automatic attach to the target process (`HD-Player`).
- An AoB scan + memory write flow to apply an "aimbot" style value copy.
- Toggleable memory hacks (currently `Speed Hack` and a `No Recoil` placeholder).
- A custom memory module (`beyondmem.py`) with multithreaded chunk scanning.

## Project Structure

- `aimbot.py` - main app, UI, hotkeys, patch logic, and process attach loop.
- `beyondmem.py` - low-level process memory read/write + AoB scanner.

## Requirements

- Windows (uses WinAPI via `ctypes`).
- Python 3.10+ recommended.
- Administrator rights (the script auto-prompts for elevation).
- Python packages:
  - `keyboard`
  - `psutil`

## Installation

```bash
git clone https://github.com/gaara1964/Python-Aimbot.git
cd Python-Aimbot
pip install keyboard psutil
```

If your repository name is different, replace `Python-Aimbot` with your actual repo folder.

## Usage

```bash
python aimbot.py
```

Behavior on launch:

1. Script elevates to admin (UAC prompt) if needed.
2. Waits until process `HD-Player` is available.
3. Shows the dashboard and starts listening for hotkeys.

## Default Hotkeys

- `F` - Inject aimbot memory write pass.
- `S` - Toggle Speed Hack.
- `R` - Toggle No Recoil (template value, needs real AoB values).
- `Q` - Exit.

## Configuration Points (aimbot.py)

- `PROCESS` - target process name (`HD-Player` by default).
- `AIMBOT_AOB` - scan pattern used to find candidate entity blocks.
- `TARGET_OFFSET` - source offset currently set to body (`0x80`).
- `WRITE_OFFSET` - destination offset currently set to head (`0x7C`).
- `HACKS` - dictionary for toggle hacks and their AoB patches.

Edit these values to match your target build/version.

## Notes

- `No Recoil` is currently a placeholder with `Your AOB HERE`.
- AoB patterns and offsets can break after target updates.
- The script is highly version-dependent and process-specific.

## Troubleshooting

- **Stuck on waiting for process**: confirm `HD-Player` is running and process name matches.
- **Nothing patched**: your AoB patterns likely changed for the current target build.
- **Permission errors**: run terminal as Administrator and retry.
- **Hotkeys not working**: verify `keyboard` installed and script is running with sufficient privileges.

## Disclaimer

This repository is for educational and reverse engineering practice. You are responsible for how you use it and for following the terms of service, rules, and laws that apply in your region and target platform.
