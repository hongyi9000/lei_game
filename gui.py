# gui.py
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextBrowser, QSpacerItem, QSizePolicy
import logging
import os

# 配置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建日志格式
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 创建 FileHandler（将日志保存到文件）和 StreamHandler（显示日志到控制台）
file_handler = logging.FileHandler('app_log.txt')
console_handler = logging.StreamHandler()

file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

class QTextBrowserHandler(logging.Handler):
    def __init__(self, text_browser):
        super().__init__()
        self.text_browser = text_browser

    def emit(self, record):
        msg = self.format(record)
        self.text_browser.append(msg)  # 将日志追加到 QTextBrowser

class LogWindow(QWidget):
    def __init__(self, click_button_func, ocr_func):
        super().__init__()
        self.setWindowTitle("挂机助手")
        self.setGeometry(100, 100, 800, 400)

        layout = QHBoxLayout()

        # 创建一个垂直布局器，用于布局按钮和日志显示区
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 创建“挂机”按钮
        self.hang_button = QPushButton("挂机", self)
        self.hang_button.setStyleSheet(
            "QPushButton {"
            "    font-size: 18px;"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    padding: 15px;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #45a049;"
            "}"
        )
        self.hang_button.clicked.connect(self.on_click)  # 按钮点击事件

        # 创建 QTextBrowser 来显示日志
        self.text_browser = QTextBrowser(self)
        self.text_browser.setStyleSheet(
            "QTextBrowser {"
            "    font-size: 14px;"
            "    background-color: #f4f4f4;"
            "    color: #333;"
            "    padding: 10px;"
            "    border: 2px solid #ddd;"
            "    border-radius: 10px;"
            "}"
        )  
        self.text_browser.setVerticalScrollBarPolicy(1)  # 显示垂直滚动条

        # 添加按钮和日志窗口到布局
        left_layout.addWidget(self.hang_button)
        right_layout.addWidget(self.text_browser)

        # 使用间隔填充让布局更加灵活
        left_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        right_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        left_layout.addItem(left_spacer)
        right_layout.addItem(right_spacer)

        # 添加到水平布局
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 3)  # 设置日志窗口占用更多空间

        # 设置主布局
        self.setLayout(layout)

        # 将自定义的日志处理器添加到 logger
        console_handler = QTextBrowserHandler(self.text_browser)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        self.click_button_func = click_button_func
        self.ocr_func = ocr_func

    def on_click(self):
        # 获取挂机按钮的图片
        template_file = "img_templates/guaji.png"  # 假设模板文件在 img_templates 文件夹内
        
        
        # 检查模板文件是否存在
        if not os.path.exists(template_file):
            logger.error(f"模板文件 {template_file} 不存在！")
            return
        
        logger.info(f"使用模板文件 {template_file} 开始匹配...")
        success = self.click_button_func(template_file)  # 图像匹配
        if success:
            logger.info("任务执行成功！")
        else:
            logger.error("任务执行失败！")
