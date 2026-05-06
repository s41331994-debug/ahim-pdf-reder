import shutil
import os
from PIL import Image

def setup_assets():
    source_img = r"C:\Users\liyaz\.gemini\antigravity\brain\30a7438e-1d3e-4503-86c8-85ba35354606\ahim_pdf_logo_1778045139114.png"
    target_png = r"d:\Ahim-PDF-Reader\assets\icon.png"
    target_ico = r"d:\Ahim-PDF-Reader\assets\icon.ico"
    
    if os.path.exists(source_img):
        # Create assets folder if not exists
        os.makedirs(r"d:\Ahim-PDF-Reader\assets", exist_ok=True)
        
        # Copy PNG
        shutil.copy(source_img, target_png)
        print(f"Copied PNG to {target_png}")
        
        # Convert to ICO
        img = Image.open(target_png)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(target_ico, format='ICO', sizes=icon_sizes)
        print(f"Converted to ICO: {target_ico}")
    else:
        print("Source image not found!")

if __name__ == "__main__":
    setup_assets()
