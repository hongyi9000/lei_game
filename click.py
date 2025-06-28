import subprocess
import cv2
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

# 定义文件夹路径
TEMPLATE_DIR = 'img_templates'  # 模板图片保存的文件夹
SCREENSHOT_DIR = 'img_screenshoot'  # 截图保存的文件夹

# 确保文件夹存在，不存在则创建
if not os.path.exists(TEMPLATE_DIR):
    os.makedirs(TEMPLATE_DIR)

if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# 保存模板到文件夹
def save_template_image(template_path):
    template_name = os.path.basename(template_path)
    save_path = os.path.join(TEMPLATE_DIR, template_name)
    
    # 调试：打印保存路径，确认是否正确
    logger.info(f"保存模板图像到：{save_path}")
    
    # 检查模板路径是否有效
    if not os.path.exists(template_path):
        logger.error(f"模板文件 {template_path} 不存在！")
        return None
    
    template = cv2.imread(template_path)
    if template is None:
        logger.error(f"无法读取模板图像：{template_path}")
        return None
    
    # 打印读取模板图像的尺寸和信息
    logger.info(f"读取模板图像成功，尺寸：{template.shape}")
    
    # 保存模板图像
    cv2.imwrite(save_path, template)
    return save_path

# 截屏并保存为文件
def screenshot(screenshot_name="screen.png"):
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
    result = subprocess.run(f"adb exec-out screencap -p > {screenshot_path}", shell=True)
    if result.returncode != 0:
        logger.error("截图失败！")
        return False
    logger.info(f"截图成功，保存在：{screenshot_path}")
    return screenshot_path

# 使用 OpenCV 的模板匹配查找并点击按钮
def click_button(template_path, screenshot_name="screen.png", threshold=0.6):
    if not screenshot():  # 如果截图失败
        return False

    # 保存模板图片
    template_save_path = save_template_image(template_path)
    if not template_save_path:
        return False  # 如果模板保存失败，则返回 False

    # 读取屏幕截图和模板图像
    screen = cv2.imread(os.path.join(SCREENSHOT_DIR, screenshot_name))
    template = cv2.imread(template_save_path)

    if screen is None or template is None:
        logger.error("无法读取图像文件")
        return False

    # 转为灰度图像进行匹配
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    logger.info(f"匹配度: {max_val}")

    if max_val > threshold:  # 如果匹配度大于阈值
        x, y = max_loc
        x_center = x + template.shape[1] // 2
        y_center = y + template.shape[0] // 2
        logger.info(f"按钮找到，点击位置：({x_center}, {y_center})")
        subprocess.run(f"adb shell input tap {x_center} {y_center}", shell=True)
        return True
    else:
        logger.error(f"未找到匹配按钮，匹配度较低：{max_val}")
        return False
