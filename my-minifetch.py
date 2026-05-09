#!/usr/bin/env python3
import os
import re
import socket
import subprocess
import shutil
import sys
from datetime import datetime
from pathlib import Path
import platform

# Path for persistent gerbil name
MEMORY_FILE = Path("memory_computerApp.txt")

memory = {}
if MEMORY_FILE.exists():
    try:
        memory["name"] = MEMORY_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        memory = {}

IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def command_exists(cmd):
    return shutil.which(cmd) is not None

def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    try:
        if IS_MAC and command_exists("screencapture"):
            subprocess.run(["screencapture", "-x", filename], check=False)
        elif IS_LINUX and command_exists("scrot"):
            subprocess.run(["scrot", filename], check=False)
        else:
            print("Screenshot command not available. Install 'scrot' on Linux or use macOS built-in screencapture.")
            return
        print(f"Screenshot taken: {filename}")
    except Exception as e:
        print("Failed to take screenshot:", e)

def get_cpu_model():
    try:
        if IS_MAC and command_exists("sysctl"):
            out = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], stderr=subprocess.DEVNULL)
            return out.decode().strip()
        if IS_LINUX:
            if Path("/proc/cpuinfo").exists():
                text = Path("/proc/cpuinfo").read_text(errors="ignore")
                m = re.search(r"model name\s*:\s*(.+)", text, re.I)
                if m:
                    return m.group(1).strip()
            # fallback to lscpu
            if command_exists("lscpu"):
                out = subprocess.check_output(["lscpu"], stderr=subprocess.DEVNULL).decode()
                m = re.search(r"Model name:\s*(.+)", out)
                if m:
                    return m.group(1).strip()
    except Exception:
        pass
    return "CPU model not found"

def get_gpu_info():
    try:
        if IS_MAC and command_exists("system_profiler"):
            out = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], stderr=subprocess.DEVNULL)
            lines = [line.strip() for line in out.decode().splitlines() if line.strip()]
            
            # return a compact summary
            return " | ".join(lines[:6])
        if IS_LINUX and command_exists("lspci"):
            out = subprocess.check_output("lspci -nn | grep -i 'vga\\|3d\\|display'", shell=True, stderr=subprocess.DEVNULL)
            return out.decode().strip()
    except Exception:
        pass
    return "GPU info not available"

def get_ram_info():
    try:
        if IS_MAC and command_exists("sysctl"):
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], stderr=subprocess.DEVNULL).decode().strip()
            size_bytes = int(out)
            size_gb = size_bytes / 1024**3
            return f"{size_gb:.1f} GB"
        if IS_LINUX:
            if command_exists("free"):
                out = subprocess.check_output(["free", "-h"], stderr=subprocess.DEVNULL).decode()
                m = re.search(r"Mem:\s+(\S+)", out)
                if m:
                    return m.group(1)
                
            # fallback: /proc/meminfo
            if Path("/proc/meminfo").exists():
                text = Path("/proc/meminfo").read_text()
                m = re.search(r"MemTotal:\s+(\d+)\s+kB", text)
                if m:
                    kb = int(m.group(1))
                    gb = kb / 1024**2
                    return f"{gb:.1f} GB"
    except Exception:
        pass
    return "RAM info not available"

def get_disk_info():
    try:
        # Use df -h for root filesystem on both platforms
        out = subprocess.check_output(["df", "-h", "/"], stderr=subprocess.DEVNULL).decode().strip().splitlines()
        if len(out) >= 2:
            return out[-1]
    except Exception:
        pass
    # fallback to lsblk on linux
    try:
        if IS_LINUX and command_exists("lsblk"):
            out = subprocess.check_output(["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT"], stderr=subprocess.DEVNULL).decode().strip()
            return out
    except Exception:
        pass
    return "Disk info not available"

def get_system_info():
    try:
        return subprocess.check_output(["uname", "-a"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return platform.platform()

def get_ip_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "IP address not available"

def get_network_devices():
    # Lightweight TCP connect scan on common local subnet ranges
    timeout = 0.25
    socket.setdefaulttimeout(timeout)
    devices = []
    # try to infer local base network from current IP
    ip = get_ip_address()
    if ip and ip.count(".") == 3 and ip != "IP address not available":
        base = ".".join(ip.split(".")[:3]) + "."
        start, end = 1, 30
    else:
        # fallback common private range
        base = "192.168.1."
        start, end = 1, 15
    port = 80
    for i in range(start, end + 1):
        target = base + str(i)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex((target, port)) == 0:
                    devices.append(target)
        except Exception:
            continue
    return devices

def ascii_art():
    clear_terminal()
    print(r"""
                                                               
                                        . ..:=             
                                .:::::.==--::::.           
                              .:::::::.:-=::-=-==-         
                            ...:::::....::::=*--=++.       
     ....                  .....::::::.::::-::-==++=       
     .:-====++.            .....:::::::.::::--::--:        
             .-=+:        ......:::::::::::::::            
                .---==:   .....::::.::::::--. .:           
                    .:--=-....::::::::::.   ..             
                         ...:.::-==-+=.                    
                           ...-===----==+++:               
                              .::--::::::..........        
    """)
    print("Gerbil: Piip")
    if memory.get("name"):
        print(f"Your gerbil's name is \033[1m{memory['name']}\033[0m!")
        if input("Wanna rename? (y/n) ").lower().startswith("y"):
            clear_terminal()
            gerbil_name = input("Give your gerbil a new name: ").strip()
            try:
                MEMORY_FILE.write_text(gerbil_name, encoding="utf-8")
                memory["name"] = gerbil_name
                print(f"{memory['name']}: Piip Piip!")
            except Exception as e:
                print("Could not save name:", e)
        else:
            print(f"Okay, {memory['name']} is a nice name!")
    else:
        gerbil_name = input("Give your gerbil a name: ").strip()
        try:
            MEMORY_FILE.write_text(gerbil_name, encoding="utf-8")
            memory["name"] = gerbil_name
            print(f"{memory['name']}: Piip Piip!")
        except Exception as e:
            print("Could not save name:", e)

def print_help():
    clear_terminal()
    print("\033[33mAvailable commands:\033[0m")
    print(" kepe / gerbil / pet - Interact with your gerbil")
    print(" screenshot / shot / ss - Take a screenshot")
    print(" ip - Show your IP address")
    print(" wifi / devices - Scan local network devices")
    print(" computer / i / info / system - Show computer system information")
    print(" clear / c - Clear the terminal")
    print(" help - Show this help")
    print(" exit / quit / q / close - Exit the program")

def main():
    art_logo = r"""
                _       _  __      _       _     
  _ __ ___ (_)_ __ (_)/ _| ___| |_ ___| |__  
 | '_ ` _ \| | '_ \| | |_ / _ \ __/ __| '_ \ 
 | | | | | | | | | | |  _|  __/ || (__| | | |
 |_| |_| |_|_|_| |_|_|_|  \___|\__\___|_| |_|
                                             
    """
    clear_terminal()
    print(art_logo)
    print("Type 'help' for commands")
    while True:
        try:
            cmd = input("\033[34mEnter your command: \033[0m").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting program")
            break
        if not cmd:
            continue
        if cmd == "test":
            print("Executing command 1")
            print("Try again ❌ 🤖")
        elif cmd in ("kepe", "gerbil", "pet"):
            ascii_art()
        elif cmd in ("exit", "quit", "q", "close"):
            print("Exiting program")
            clear_terminal()
            break
        elif cmd in ("c", "clear"):
            clear_terminal()
        elif cmd in ("screenshot", "shot", "ss"):
            take_screenshot()
        elif cmd == "ip":
            print(" 🌐 Your IP address is:")
            print(get_ip_address())
        elif cmd in ("wifi", "devices"):
            print("Scanning local network (this may take a few seconds)...")
            devices = get_network_devices()
            if devices:
                print("Devices in your network:")
                for ip in devices:
                    print(f" - {ip}")
            else:
                print("No devices found in the scanned range.")
        elif cmd in ("computer", "i", "info", "system"):
            clear_terminal()
            print(art_logo)
            print(f"\033[34m 💻 Your System info: \033[31m{get_system_info()}\033[0m")
            print(f"\033[34m 📽️ Your GPU info: \033[31m{get_gpu_info()}\033[0m")
            print(f"\033[34m 🔲 Your CPU model: \033[31m{get_cpu_model()}\033[0m")
            print(f"\033[34m ⚙️ Your RAM info: \033[31m{get_ram_info()}\033[0m")
            print(f"\033[34m 💾 Your HDD/SSD info: \033[31m{get_disk_info()}\033[0m")
        elif cmd == "help":
            print_help()
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
