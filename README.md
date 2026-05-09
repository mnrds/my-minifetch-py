# my-minifetch-py

my-minifetch-py is a lightweight terminal application written in Python that displays basic system information, inspired by screenfetch. 

This project was created as a Python learning exercise and idea was to build a simple copy of popular screenfetch for personal use. Goal was to learn code python and how to build a terminal-based applications. 
Maybe in the future I modify it and add some more features. 

---

## Features

- **Command-based terminal interface**
- **System information**:
  - Operating system
  - Root filesystem usage
  - Total RAM
  - Graphics card / GPU summary
  - CPU model
- **Take screenshots** and save them to the project folder
- **Show local IP address**
- **Lightweight local network device discovery** (TCP connect scan)
- **Small interactive "gerbil" mascot** with a persistent name stored on disk
- **Cross-platform support** for Linux and macOS with fallbacks and checks for required external tools
- Simple and readable terminal output

---


## Updates

**Version**: Added macOS support and improved cross-platform compatibility

**What changed**
- **macOS support**: the script detects macOS and uses `screencapture`, `sysctl`, and `system_profiler` to collect CPU, RAM, and GPU information.
- **Improved Linux support**: uses `lscpu`, `/proc/cpuinfo`, `free`, `lsblk`, `lspci`, and `scrot` when available.
- **Command availability checks**: the script verifies external commands with `shutil.which` before calling them and prints helpful messages if a tool is missing.
- **Better error handling**: `try/except` blocks prevent crashes when commands or files are missing or return unexpected output.
- **Smarter network scan**: the local subnet is inferred from the current IP address when possible; the scan range is lightweight by default.
- **Persistent gerbil name**: the mascot name is stored in `memory_computerApp.txt` and read/written safely.
- **Platform detection**: uses `platform` and `shutil` to improve reliability across environments.
- **README**: installation instructions and an Updates section were added.

---

## Installation

### Requirements
- **Python 3.8+**
- **Linux**: tested on Ubuntu/Debian
- **macOS**: Big Sur and newer tested for basic functionality 
- **Optional system tools**:
  - Linux: `scrot`, `lspci` (package `pciutils`), `lsblk` (package `util-linux`), `free` (package `procps`)
  - macOS: `screencapture`, `sysctl`, `system_profiler` are typically available by default

### Clone and prepare
```bash
git clone https://github.com/mnrds/my-minifetch-py.git
cd my-minifetch-py
python3 -m venv .venv
source .venv/bin/activate
chmod +x my-minifetch.py

---


## Disclaimer

This project is for educational purposes only.