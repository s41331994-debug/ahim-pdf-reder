import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QToolBar, QFileDialog, 
                             QStatusBar, QVBoxLayout, QWidget, QPushButton, QSplitter, QComboBox)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize
from .pdf_viewer import PDFViewer
from .thumbnail_list import ThumbnailList
from .icons import get_icon
from .dialogs import OCRDialog
from core.pdf_engine import PDFEngine
from core.ocr_engine import OCREngine
from core.converter import PDFConverter
from core.annotator import PDFAnnotator, PDFOrganizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = PDFEngine()
        self.ocr_engine = OCREngine()
        self.converter = PDFConverter()
        self.annotator = PDFAnnotator()
        self.organizer = PDFOrganizer()
        self.current_zoom = 1.5
        self.current_page = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ahim PDF Reader - Professional")
        self.setMinimumSize(1000, 800)
        
        # Set Window Icon
        icon_path = os.path.join("assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Main Layout using Splitter
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        self.sidebar = ThumbnailList()
        self.sidebar.itemClicked.connect(self.on_thumbnail_clicked)
        self.splitter.addWidget(self.sidebar)

        # PDF Viewer
        self.viewer = PDFViewer()
        self.viewer.clicked.connect(self.handle_viewer_click)
        self.splitter.addWidget(self.viewer)

        # Set initial sizes for splitter (sidebar: 200, viewer: rest)
        self.splitter.setSizes([200, 800])
        
        self.main_layout.addWidget(self.splitter)

        # Toolbar
        self.create_toolbar()

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Styling
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QToolBar { background-color: #333333; border-bottom: 1px solid #444444; spacing: 15px; padding: 5px; }
            QToolButton { color: white; background-color: transparent; border-radius: 4px; padding: 8px; font-size: 11px; }
            QToolButton:hover { background-color: #444444; }
            QStatusBar { background-color: #333333; color: white; }
            QLabel { color: white; }
        """)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        # Basic Actions
        open_action = QAction(get_icon("open"), "Open PDF", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction(get_icon("word_to_pdf"), "Save", self)
        save_action.triggered.connect(self.save_document)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        # Navigation
        prev_action = QAction(get_icon("prev"), "Prev", self)
        prev_action.triggered.connect(self.prev_page)
        toolbar.addAction(prev_action)

        next_action = QAction(get_icon("next"), "Next", self)
        next_action.triggered.connect(self.next_page)
        toolbar.addAction(next_action)

        toolbar.addSeparator()

        # Zoom
        toolbar.addAction(QAction(get_icon("zoom_in"), "Zoom +", self, triggered=self.zoom_in))
        toolbar.addAction(QAction(get_icon("zoom_out"), "Zoom -", self, triggered=self.zoom_out))

        toolbar.addSeparator()

        # Converters
        toolbar.addAction(QAction(get_icon("pdf_to_word"), "PDF -> Word", self, triggered=self.convert_pdf_to_word))
        toolbar.addAction(QAction(get_icon("word_to_pdf"), "Word -> PDF", self, triggered=self.convert_word_to_pdf))
        toolbar.addAction(QAction(get_icon("image_to_ico"), "Img -> ICO", self, triggered=self.convert_image_to_ico))

        toolbar.addSeparator()

        # OCR
        self.ocr_action = QAction(get_icon("ocr"), "OCR", self)
        self.ocr_action.triggered.connect(self.run_ocr)
        toolbar.addAction(self.ocr_action)
        
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["eng", "ara", "chi_sim", "jpn", "kor", "ind"])
        self.lang_selector.setStyleSheet("color: white; background-color: #444444; border: none;")
        toolbar.addWidget(self.lang_selector)

        toolbar.addSeparator()

        # File Ops
        toolbar.addAction(QAction(get_icon("merge"), "Merge PDF", self, triggered=self.merge_pdfs))
        toolbar.addAction(QAction(get_icon("split"), "Split PDF", self, triggered=self.split_pdf))

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path: self.open_file_from_path(file_path)

    def open_file_from_path(self, file_path):
        try:
            self.engine.open_document(file_path)
            self.current_page = 0
            self.sidebar.load_thumbnails(self.engine)
            self.update_viewer()
            self.setWindowTitle(f"Ahim PDF Reader - {file_path}")
            self.status_bar.showMessage(f"Loaded: {file_path}")
        except Exception as e: self.status_bar.showMessage(f"Error: {str(e)}")

    def update_viewer(self):
        img_data = self.engine.render_page(self.current_page, self.current_zoom)
        self.viewer.display_page(img_data)
        self.status_bar.showMessage(f"Page {self.current_page + 1} of {self.engine.get_page_count()}")
        self.sidebar.setCurrentRow(self.current_page)

    def on_thumbnail_clicked(self, item):
        self.current_page = self.sidebar.row(item)
        self.update_viewer()

    def next_page(self):
        if self.current_page < self.engine.get_page_count() - 1:
            self.current_page += 1
            self.update_viewer()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_viewer()

    def zoom_in(self):
        self.current_zoom += 0.2
        self.update_viewer()

    def zoom_out(self):
        if self.current_zoom > 0.4:
            self.current_zoom -= 0.2
            self.update_viewer()

    def run_ocr(self):
        if not self.engine.doc: return
        img_data = self.engine.render_page(self.current_page, zoom=2.0)
        if img_data:
            lang = self.lang_selector.currentText()
            text = self.ocr_engine.extract_text(img_data, lang=lang)
            OCRDialog(text, self).exec()
            self.status_bar.showMessage(f"OCR Completed ({lang})")

    def convert_pdf_to_word(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if file_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Word", file_path.replace(".pdf", ".docx"), "Word (*.docx)")
            if save_path:
                try:
                    self.converter.pdf_to_word(file_path, save_path)
                    self.status_bar.showMessage("Conversion complete.")
                except Exception as e: self.status_bar.showMessage(f"Error: {e}")

    def convert_word_to_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Word", "", "Word (*.docx)")
        if file_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", file_path.replace(".docx", ".pdf"), "PDF (*.pdf)")
            if save_path:
                try:
                    self.converter.word_to_pdf(file_path, save_path)
                    self.status_bar.showMessage("Conversion complete.")
                except Exception as e: self.status_bar.showMessage(f"Error: {e}")

    def convert_image_to_ico(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save ICO", file_path.replace(os.path.splitext(file_path)[1], ".ico"), "ICO (*.ico)")
            if save_path:
                try:
                    self.converter.image_to_ico(file_path, save_path)
                    self.status_bar.showMessage("ICO created successfully.")
                except Exception as e: self.status_bar.showMessage(f"Error: {e}")

    def merge_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")
        if files:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged", "merged.pdf", "PDF (*.pdf)")
            if save_path:
                try:
                    self.organizer.merge_pdfs(files, save_path)
                    self.status_bar.showMessage("Merge complete.")
                except Exception as e: self.status_bar.showMessage(f"Error: {e}")

    def split_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if file_path:
            out_dir = QFileDialog.getExistingDirectory(self, "Output Folder")
            if out_dir:
                try:
                    self.organizer.split_pdf(file_path, out_dir)
                    self.status_bar.showMessage("Split complete.")
                except Exception as e: self.status_bar.showMessage(f"Error: {e}")

    def handle_viewer_click(self, pos): pass
    def save_document(self):
        if not self.engine.doc: return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF (*.pdf)")
        if file_path:
            try:
                self.engine.doc.save(file_path)
                self.status_bar.showMessage("Document saved.")
            except Exception as e: self.status_bar.showMessage(f"Error: {e}")
