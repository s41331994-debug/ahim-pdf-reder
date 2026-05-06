import fitz

class PDFAnnotator:
    @staticmethod
    def add_highlight(page, rect, color=(1, 1, 0)):
        """Add a highlight annotation to a page."""
        annot = page.add_highlight_annot(rect)
        annot.set_colors(stroke=color)
        annot.update()

    @staticmethod
    def add_sticky_note(page, point, text, color=(1, 1, 0)):
        """Add a text (sticky note) annotation."""
        annot = page.add_text_annot(point, text)
        annot.set_colors(stroke=color)
        annot.update()

    @staticmethod
    def add_text(page, point, text, fontsize=12, color=(0, 0, 0)):
        """Add a new text layer to the PDF."""
        page.insert_text(point, text, fontsize=fontsize, color=color)

class PDFOrganizer:
    @staticmethod
    def merge_pdfs(pdf_list, output_path):
        """Merge multiple PDF files into one."""
        result = fitz.open()
        for pdf_path in pdf_list:
            with fitz.open(pdf_path) as m_pdf:
                result.insert_pdf(m_pdf)
        result.save(output_path)
        result.close()

    @staticmethod
    def split_pdf(pdf_path, output_dir, pages_per_file=1):
        """Split a PDF into multiple files."""
        doc = fitz.open(pdf_path)
        for i in range(0, len(doc), pages_per_file):
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=i, to_page=min(i + pages_per_file - 1, len(doc) - 1))
            new_doc.save(os.path.join(output_dir, f"split_{i+1}.pdf"))
            new_doc.close()
        doc.close()
