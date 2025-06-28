# ocr.py
import subprocess
from PIL import Image
import pytesseract
import logging
import time
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

# 定义文件夹路径
SCREENSHOT_DIR = 'img_screenshoot'  # 截图保存的文件夹

# 确保文件夹存在，不存在则创建
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# 截屏并保存为文件
def screenshot(screenshot_name="screen.png"):
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
    result = subprocess.run(f"adb exec-out screencap -p > {screenshot_path}", shell=True)
    if result.returncode != 0:
        logger.error("截图失败！")
        return False
    logger.info(f"截图成功，保存在：{screenshot_path}")
    return screenshot_path

# 使用 pytesseract 对截屏进行 OCR 识别
def ocr_image(image_path):
    img = Image.open(image_path)
    
    # 使用 Tesseract 识别图像中的中文文字
    text = pytesseract.image_to_string(img, lang='chi_sim')  # 使用简体中文语言包
    logger.info(f"识别到的文字：\n{text}")
    return text
