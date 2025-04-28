# chinese_matplotlib

自动设置Matplotlib支持中文字体的小工具。

## 功能特点
- 自动检测当前系统可用的中文字体
- 如果本地缺少中文字体，自动下载并安装思源黑体 (Source Han Sans SC)
- 缓存检测结果，避免每次重复扫描
- 支持跨平台（Windows, macOS, Linux）

## 安装方法
```bash
pip install chinese-matplotlib
```
## 使用
```python
from chinese_matplotlib import set_chinese_font
```
## 测试
```python
from chinese_matplotlib import test_plot
```
