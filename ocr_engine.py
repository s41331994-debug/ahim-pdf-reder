import pytesseract
from PIL import Image
import io
import os

class OCREngine:
    def __init__(self):
        # Common Tesseract paths on Windows
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(os.getlogin()),
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break

    def extract_text(self, img_data, lang='eng'):
        """Extract text from raw image data (PPM/bytes) with language support."""
        try:
            image = Image.open(io.BytesIO(img_data))
            # Combine languages if needed, e.g., 'eng+ara'
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            return f"OCR Error: {str(e)}"

    def get_available_languages(self):
        """Get list of installed Tesseract languages."""
        try:
            return pytesseract.get_languages(config='')
        except:
            return ['eng']
