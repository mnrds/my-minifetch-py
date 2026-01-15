#!/usr/bin/env python3
import subprocess
import socket
import re
from datetime import datetime

memory = {}
try: 
    with open("memory_computerApp.txt", "r") as f:
        memory["name"] = f.read().strip()
except FileNotFoundError:
    pass

def main():
    print("\033[34m" + "[ minifetch ] \033[0m")
    art = r"""
                                                               
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
    """    

    artLogo = r"""
                _       _  __      _       _     
  _ __ ___ (_)_ __ (_)/ _| ___| |_ ___| |__  
 | '_ ` _ \| | '_ \| | |_ / _ \ __/ __| '_ \ 
 | | | | | | | | | | |  _|  __/ || (__| | | |
 |_| |_| |_|_|_| |_|_|_|  \___|\__\___|_| |_|
                                             
    """


    cmd = input("\033[34mEnter your command: \033[0m")

    #This is a test line for command 1
    command1 = "test"


    #Functions inside main loop
    def asciiArt(): 
        clearTerminal()
        print(art)
        print("Gerbil: Piip")
        
        if "name" in memory and memory["name"] != "": 
            print("Your gerbil's name is \033[1m " + memory["name"] + "\033[0m!")
            choice = input("Wanna rename? (y/n)")
            if choice in ("y"):
                clearTerminal()
                gerbilName = input("Give your gerbil a new name: ")
                with open("memory_computerApp.txt", "w") as f:
                    f.write(gerbilName)
                    memory["name"] = gerbilName
                print(memory["name"] + ": Piip Piip!")
            else:
                print("Okay, " + memory["name"] + " is a nice name!")
                return main()
            return main()
        else:
            gerbilName = input("Give your gerbil a name: ")
            with open("memory_computerApp.txt", "w") as f:
                f.write(gerbilName)
                memory["name"] = gerbilName
                print(memory["name"] + ": Piip Piip!")
            return main()
    
    #Clear Terminal function
    def clearTerminal():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    # Sceenshot function
    def takeScreenShot():
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        subprocess.run(["scrot", filename])

    # Computer system info
        # Distro 
    outSystem = subprocess.check_output("uname -a", shell=True)

        # GPU info
    GPUStats = "lspci -nn | grep -i 'vga\\|3d\\|display'"
    outGPU = subprocess.check_output(GPUStats, shell=True)

        # CPU info -function
    def get_cpu_model():
        commands = [
            "lscpu | grep -i 'model name'",
            "lscpu | grep -i 'model'",
            "cat /proc/cpuinfo | grep -i 'model name' | head -1",
            "cat /proc/cpuinfo | grep -i 'hardware' | head -1"
        ]

        for cmd in commands:
            try:
                out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
                if not out:
                    continue
                m = re.search(r'model name\s*:\s*(.+)', out, re.I)
                if m:
                    model = m.group(1).strip()
                else:
                    model = out.split(":", 1)[-1].strip()
                return model
            
            except subprocess.CalledProcessError:
                continue

            except Exception:
                continue

        return  "Your CPU: CPU model not found"


    # Find your own IP address function
    def get_ip_address():
        myS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        myS.connect(("8.8.8.8", 80))
        print(myS.getsockname()[0])
        myS.close()
    def get_ip_wifi():
        # Find other devices in the network
        timeout = 0.3
        verkko = "192.168.1."
        portti = 80
        socket.setdefaulttimeout(timeout)
        aktiiviset = []
        for i in range(1, 15):
            ip = verkko + str(i)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tulos = s.connect_ex((ip, portti))
            s.close()
        if tulos == 0: 
            aktiiviset.append(ip)
            print("Devices in your network: ")


        # RAM info
    RAMStats = "free -h | grep Mem | awk '{print $2}'"
    outRAM = subprocess.check_output(RAMStats, shell=True)

        # HDD/SSD info
    HDDStats = "lsblk -o NAME,SIZE,TYPE | grep disk"
    outHDD = subprocess.check_output(HDDStats, shell=True)


    if cmd == command1:
        print("Executing command 1")
        print("Try again ❌ 🤖 ")
        return main()
    elif cmd in ("kepe", "gerbil", "pet"):
        asciiArt()
    
    #kill program 
    elif cmd in ("exit", "quit", "q", "close"):
        print("Exiting program")
        clearTerminal()

    #clear screen 
    elif cmd in ("c", "clear"):
        clearTerminal()
        return main()
    
    #screenshot commands
    elif cmd in ("screenshot", "shot", "ss"):
        takeScreenShot()
        print("Screenshot taken! 📸")
        return main()
    
    #IP-address commands
    elif cmd == "ip":
        print(" 🌐 Your IP address is: ")
        get_ip_address()
        return main()
    
    elif cmd in ("wifi", "devices"):
        get_ip_wifi()
        device_count = get_ip_wifi()
        print(f"📶 Devices found in your network: {device_count}")
        return main()

    #Computer command / info 
    elif cmd in ("computer", "i", "info", "system"):
        clearTerminal()
        print(artLogo)
        print("\033[34m 💻 Your System info: \033[34m\033[31m" + outSystem.decode() + "\033[0m")
        print("\033[34m 📽️ Your GPU info: \033[34m\033[31m" + outGPU.decode() + "\033[0m")
        print("\033[34m 🔲 Your CPU model: \033[34m\033[31m" + get_cpu_model() + "\033[0m")
        print("")
        print("\033[34m ⚙️ Your RAM info: \033[34m\033[31m" + outRAM.decode() + "\033[0m")
        print("\033[34m 💾 Your HDD/SSD info: \033[34m")
        print("\033[31m" + outHDD.decode() + "\033[0m") 
        return main() 

    elif cmd == "help":
        clearTerminal()
        print("\033[33m" + "Available commands:\033[0m")
        print(" kepe / gerbil / pet - Interact with your gerbil")
        print(" screenshot / shot / ss - Take a screenshot")
        print(" ip - Show your IP address")
        print(" wifi / devices - Show devices in your network")
        print(" computer / i / info / system - Show computer system information")
        print(" clear / c - Clear the terminal")
        print(" exit / quit / q / close - Exit the program")
        return main()

    else:
        print("Unknown command")
        return main()
    
if __name__ == "__main__":
    main()
