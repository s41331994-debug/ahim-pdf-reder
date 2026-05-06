from PyQt6.QtWidgets import QScrollArea, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal, QPoint

class PDFViewer(QScrollArea):
    clicked = pyqtSignal(QPoint)
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setMouseTracking(True)
        self.container_layout.addWidget(self.page_label)
        
        self.setWidget(self.container)
        self.setStyleSheet("background-color: #1e1e1e; border: none;")

    def display_page(self, img_data):
        if img_data:
            image = QImage.fromData(img_data)
            pixmap = QPixmap.fromImage(image)
            self.page_label.setPixmap(pixmap)
            self.page_label.setFixedSize(pixmap.size())
        else:
            self.page_label.clear()
            self.page_label.setText("No document loaded")
            self.page_label.setFixedSize(400, 600)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Calculate position relative to the page_label
            # We use viewport coordinates and map them to the label
            label_pos = self.page_label.mapFrom(self.viewport(), event.pos())
            
            # Ensure the click is within the page bounds
            if self.page_label.rect().contains(label_pos):
                self.clicked.emit(label_pos)
        super().mousePressEvent(event)
