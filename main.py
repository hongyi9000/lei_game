# main.py
from gui import LogWindow
from click import click_button
from ocr import ocr_image
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 将其他模块传递给 GUI
    window = LogWindow(click_button, ocr_image)
    window.show()
    
    sys.exit(app.exec_())