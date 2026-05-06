from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QListView
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt, QSize

class ThumbnailList(QListWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setIconSize(QSize(150, 200))
        self.setMovement(QListView.Movement.Static)
        self.setSpacing(10)
        self.setFixedWidth(200)
        
        # Dark Theme Styling
        self.setStyleSheet("""
            QListWidget {
                background-color: #252525;
                border-right: 1px solid #444444;
                outline: none;
            }
            QListWidget::item {
                color: white;
                background-color: transparent;
            }
            QListWidget::item:selected {
                background-color: #3d3d3d;
                border: 1px solid #0078d4;
            }
        """)

    def load_thumbnails(self, engine):
        """Generate and load thumbnails for all pages."""
        self.clear()
        page_count = engine.get_page_count()
        
        for i in range(page_count):
            # Render page with low zoom for thumbnail
            img_data = engine.render_page(i, zoom=0.2)
            if img_data:
                image = QImage.fromData(img_data)
                pixmap = QPixmap.fromImage(image)
                
                item = QListWidgetItem(f"Page {i+1}")
                item.setIcon(QIcon(pixmap))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.addItem(item)
