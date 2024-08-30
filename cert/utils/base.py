import string
import random
import win32api
import win32gui
import win32con
import win32process
import ctypes
from cert.mempy.api import Memopy

Window = None
Process = Memopy(0)

def RBXString(Address: int):
    string_pointer = Address
    string_check = Process.read_long(
        string_pointer + 0x18
    )

    if string_check > 15:
        string_pointer = Process.read_longlong(
            string_pointer
        )

    return Process.read_string(string_pointer)

def fetch_roblox_pid():
    global Window, Process

    Window = win32gui.FindWindow(None, "Roblox")
    ProcessId = win32process.GetWindowThreadProcessId(Window)[1]

    return ProcessId

def random_string(length: int = 5) -> str:
    result = "".join((random.choice(string.ascii_lowercase) for x in range(length)))
    return result

def initialize():
    ProcessId = fetch_roblox_pid()
    Process.update_pid(ProcessId)

    if not Process.process_handle:
        return False, -1
    
    return True, ProcessId

def send_key_input(key_code: int):
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", wintypes.WORD), 
                    ("wScan", wintypes.WORD), 
                    ("dwFlags", wintypes.DWORD), 
                    ("time", wintypes.DWORD), 
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    class INPUT(ctypes.Structure):
        _fields_ = [("type", wintypes.DWORD), 
                    ("ki", KEYBDINPUT)]

    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002

    input_event = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(
        wVk=key_code,
        wScan=0,
        dwFlags=0,
        time=0,
        dwExtraInfo=None
    ))

    ctypes.windll.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))

    input_event.ki.dwFlags = KEYEVENTF_KEYUP
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))

def initialize_script_hook():
    Window = win32gui.FindWindow(None, "Roblox")
    ProcessId = win32process.GetWindowThreadProcessId(Window)[1]
    Process.update_pid(ProcessId)

    if not Process.process_handle:
        return False, -1

    while True:
        if win32gui.GetForegroundWindow() == Window:
            send_key_input(win32api.MapVirtualKey(win32con.VK_ESCAPE, 0))
            break
