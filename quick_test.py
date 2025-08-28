"""
快速启动测试脚本
"""

import sys
import os

def check_dependencies():
    """检查依赖"""
    print("检查依赖...")
    missing = []
    
    try:
        import PyQt5
        print("✓ PyQt5 已安装")
    except ImportError:
        missing.append("PyQt5")
        
    try:
        import requests
        print("✓ requests 已安装")
    except ImportError:
        missing.append("requests")
        
    try:
        import feedparser
        print("✓ feedparser 已安装")
    except ImportError:
        missing.append("feedparser")
        
    try:
        import dateutil
        print("✓ python-dateutil 已安装")
    except ImportError:
        missing.append("python-dateutil")
    
    if missing:
        print(f"\n缺少依赖: {', '.join(missing)}")
        print("请运行: pip install " + " ".join(missing))
        return False
    
    return True

def test_app_startup():
    """测试应用程序启动"""
    print("\n测试应用程序组件...")
    
    try:
        # 设置Qt属性避免警告
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        # 必须在创建QApplication之前设置
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        
        # 测试导入
        from main_window import MainWindow
        print("✓ 主窗口类导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 应用程序测试失败: {e}")
        return False

def main():
    print("Twitter RSS订阅管理器 - 启动检查")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 测试应用组件
    if not test_app_startup():
        return
    
    print("\n" + "=" * 40)
    print("✓ 所有检查通过！")
    print("\n现在可以启动应用程序:")
    print("python main.py")
    print("=" * 40)

if __name__ == "__main__":
    main()