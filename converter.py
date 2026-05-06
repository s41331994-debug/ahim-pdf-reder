from pdf2docx import Converter as PDFtoDocx
from docx2pdf import convert as DocxtoPDF
from PIL import Image
import os

class PDFConverter:
    @staticmethod
    def pdf_to_word(pdf_path, word_path=None):
        """Convert PDF file to Word with high fidelity for formulas, images, and non-Latin text."""
        if not word_path:
            word_path = pdf_path.replace(".pdf", ".docx")
        
        try:
            cv = PDFtoDocx(pdf_path)
            cv.convert(word_path, start=0, end=None, multi_processing=True)
            cv.close()
            return word_path
        except Exception as e:
            raise Exception(f"PDF to Word Error: {str(e)}")

    @staticmethod
    def word_to_pdf(word_path, pdf_path=None):
        """Convert Word (.docx) to PDF."""
        try:
            DocxtoPDF(word_path, pdf_path)
            if not pdf_path:
                pdf_path = word_path.replace(".docx", ".pdf")
            return pdf_path
        except Exception as e:
            raise Exception(f"Word to PDF Error: {str(e)}")

    @staticmethod
    def image_to_ico(image_path, ico_path=None):
        """Convert PNG/JPG to Windows ICO with multiple sizes."""
        if not ico_path:
            ico_path = os.path.splitext(image_path)[0] + ".ico"
        
        try:
            img = Image.open(image_path)
            # Define standard Windows icon sizes
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save(ico_path, format='ICO', sizes=icon_sizes)
            return ico_path
        except Exception as e:
            raise Exception(f"Image to ICO Error: {str(e)}")
