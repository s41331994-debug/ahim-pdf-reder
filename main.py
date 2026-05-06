import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ahim PDF Reader")
    
    window = MainWindow()
    
    # Check if a file was passed as an argument (e.g., from "Open With")
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if file_path.lower().endswith(".pdf"):
            window.open_file_from_path(file_path)
            
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
