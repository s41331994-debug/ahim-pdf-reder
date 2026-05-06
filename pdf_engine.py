import fitz  # PyMuPDF
import os
from PIL import Image
import io

class PDFEngine:
    def __init__(self):
        self.doc = None
        self.current_page = 0

    def open_document(self, file_path):
        """Open a PDF document."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.doc = fitz.open(file_path)
        self.current_page = 0
        return self.get_metadata()

    def get_metadata(self):
        """Get document metadata."""
        if not self.doc:
            return {}
        return self.doc.metadata

    def get_page_count(self):
        """Get total number of pages."""
        if not self.doc:
            return 0
        return len(self.doc)

    def render_page(self, page_number, zoom=1.0):
        """Render a page to a QPixmap compatible image (PIL/bytes)."""
        if not self.doc:
            return None
        
        if 0 <= page_number < len(self.doc):
            page = self.doc.load_page(page_number)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image for easier handling in some cases, 
            # or we can return bytes directly for PyQt
            img_data = pix.tobytes("ppm")
            return img_data
        return None

    def close_document(self):
        """Close the current document."""
        if self.doc:
            self.doc.close()
            self.doc = None
