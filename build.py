import subprocess
import os
import sys

def build_exe():
    print("Building Ahim PDF Reader Executable...")
    
    # Command to build EXE
    # --noconsole: Don't show terminal
    # --onefile: Pack everything into one EXE
    # --name: The name of the output file
    # --clean: Clean cache before build
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--icon", "assets/icon.ico",
        "--name", "AhimPDFReader",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\nSUCCESS: Executable created in 'dist/AhimPDFReader.exe'")
        print("To set as default, right-click any PDF file, select 'Open with' -> 'Choose another app',")
        print("locate 'AhimPDFReader.exe' in the 'dist' folder, and check 'Always use this app'.")
    except Exception as e:
        print(f"Error during build: {e}")

if __name__ == "__main__":
    build_exe()
