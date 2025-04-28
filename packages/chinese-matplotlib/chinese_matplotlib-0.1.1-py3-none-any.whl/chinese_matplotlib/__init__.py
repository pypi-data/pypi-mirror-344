# chinese_matplotlib/__init__.py

from .font_manager import set_chinese_font, test_plot
import os

_AUTO_EXECUTE = os.getenv('CHINESE_MATPLOTLIB_AUTO', '1')  # 默认开启

if _AUTO_EXECUTE == '1':
    set_chinese_font()
