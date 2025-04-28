# chinese_matplotlib/font_manager.py

import os
import platform
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import json
import urllib.request
import zipfile

# 定义默认字体列表
DEFAULT_FONT_CANDIDATES = [
    # Windows
    'Microsoft YaHei', 'SimHei', 'FangSong', 'KaiTi', 'YouYuan',
    # macOS
    'PingFang SC', 'Heiti SC', 'Hiragino Sans GB',
    # Google开源字体
    'Noto Sans CJK SC', 'Noto Serif CJK SC',
    # Adobe开源字体
    'Source Han Sans SC', 'Source Han Serif SC',
    # Linux常见字体
    'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'AR PL UKai CN', 'AR PL UMing CN'
]

# 缓存文件路径
CACHE_DIR = os.path.expanduser('~/.cache/chinese_matplotlib')
CACHE_FILE = os.path.join(CACHE_DIR, 'font_cache.json')

# 思源黑体下载地址
SOURCE_HAN_SANS_SC_URL = "https://github.com/adobe-fonts/source-han-sans/releases/download/2.004R/SourceHanSansSC.zip"

# 本地临时字体存放目录
LOCAL_FONT_DIR = os.path.join(CACHE_DIR, "fonts")


def load_font_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_font_cache(font_name):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"font": font_name}, f)


def download_and_install_source_han_sans_sc():
    os.makedirs(LOCAL_FONT_DIR, exist_ok=True)
    local_zip = os.path.join(LOCAL_FONT_DIR, 'SourceHanSansSC.zip')

    if not os.path.exists(local_zip):
        print("[Info] 正在下载思源黑体 Source Han Sans SC 字体...")
        urllib.request.urlretrieve(SOURCE_HAN_SANS_SC_URL, local_zip)

    with zipfile.ZipFile(local_zip, 'r') as zip_ref:
        zip_ref.extractall(LOCAL_FONT_DIR)
    
    # 查找所有OTF字体文件
    otf_files = []
    for root, dirs, files in os.walk(LOCAL_FONT_DIR):
        for file in files:
            if file.lower().endswith('.otf'):
                otf_files.append(os.path.join(root, file))
    
    # 将字体添加到matplotlib
    for otf in otf_files:
        font_manager.fontManager.addfont(otf)
    
    # 通知matplotlib重新加载字体
    font_manager._rebuild()

    print(f"[Info] 思源黑体字体安装完成，共安装{len(otf_files)}个字体文件。")


def set_chinese_font(preferred_fonts=None, verbose=True):
    """
    自动检测并设置可用的中文字体用于Matplotlib。
    如果没有可用字体，会自动下载思源黑体并注册。
    """
    if preferred_fonts is None:
        preferred_fonts = DEFAULT_FONT_CANDIDATES

    # Step 1: 先查看缓存
    cache = load_font_cache()
    if "font" in cache:
        matplotlib.rcParams['font.family'] = cache["font"]
        matplotlib.rcParams['axes.unicode_minus'] = False
        if verbose:
            print(f"[Info] 使用缓存字体：{cache['font']}")
        return cache["font"]

    # Step 2: 扫描系统字体
    available_fonts = set(f.name for f in font_manager.fontManager.ttflist)

    for font in preferred_fonts:
        if font in available_fonts:
            matplotlib.rcParams['font.family'] = font
            matplotlib.rcParams['axes.unicode_minus'] = False
            save_font_cache(font)
            if verbose:
                print(f"[Info] 成功设置Matplotlib中文字体：{font}")
            return font

    # Step 3: 没找到 → 自动下载思源黑体
    download_and_install_source_han_sans_sc()

    # 重新扫描字体
    available_fonts = set(f.name for f in font_manager.fontManager.ttflist)
    for font in preferred_fonts:
        if font in available_fonts:
            matplotlib.rcParams['font.family'] = font
            matplotlib.rcParams['axes.unicode_minus'] = False
            save_font_cache(font)
            if verbose:
                print(f"[Info] 成功设置（通过自动下载）Matplotlib中文字体：{font}")
            return font

    # Step 4: 如果还失败
    if verbose:
        print('[Warning] 未找到可用的中文字体，中文字符可能无法正常显示。')
    return None


def test_plot():
    """
    测试函数，绘制一个简单中文图。
    """
    set_chinese_font()
    plt.figure()
    plt.title("测试中文字体显示")
    plt.plot([0, 1], [0, 1])
    plt.xlabel("横轴")
    plt.ylabel("纵轴")
    plt.show()
