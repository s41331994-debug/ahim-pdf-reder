import winreg
import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def register_as_default(exe_path):
    if not is_admin():
        print("ERROR: Please run this script as Administrator.")
        return False

    try:
        # 1. Register the application class
        key_path = r"Software\Classes\AhimPDF.Document"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Ahim PDF Document")
            
        # 2. Set the open command
        command_path = rf"{key_path}\shell\open\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')

        # 3. Associate .pdf extension (Current User)
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pdf") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "AhimPDF.Document")

        print("SUCCESS: Ahim PDF Reader has been registered in the system.")
        print("Now you can right-click a PDF -> Open With -> Choose Ahim PDF Reader.")
        return True
    except Exception as e:
        print(f"Failed to register: {e}")
        return False

if __name__ == "__main__":
    # Assuming the EXE is built in dist/AhimPDFReader.exe
    exe_location = os.path.abspath("dist/AhimPDFReader.exe")
    if os.path.exists(exe_location):
        register_as_default(exe_location)
    else:
        print(f"EXE not found at {exe_location}. Please run build.py first.")
