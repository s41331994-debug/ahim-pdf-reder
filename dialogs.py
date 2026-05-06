from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

class OCRDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.extracted_text = text
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OCR Results")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        label = QLabel("Extracted Text:")
        label.setStyleSheet("font-weight: bold; color: white;")
        layout.addWidget(label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.extracted_text)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #dcdcdc;
                border: 1px solid #444444;
                font-family: 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.text_edit)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #006abc;
            }
        """)
        layout.addWidget(close_btn)
        
        self.setStyleSheet("background-color: #2b2b2b;")
