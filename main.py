"""
Twitter RSS订阅管理器 - 主程序入口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

from main_window import MainWindow


def check_dependencies():
    """检查依赖库是否安装"""
    missing_deps = []
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    try:
        import feedparser
    except ImportError:
        missing_deps.append("feedparser")
    
    try:
        from dateutil.parser import parse
    except ImportError:
        missing_deps.append("python-dateutil")
    
    if missing_deps:
        return False, missing_deps
    
    return True, []


def main():
    """主函数"""
    # 设置应用程序属性（必须在创建QApplication之前）
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # 创建应用程序
    app = QApplication(sys.argv)
    app.setApplicationName("Twitter RSS订阅管理器")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("RSS Manager")
    
    # 检查依赖
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("缺少依赖")
        msg.setText("应用程序缺少必要的依赖库")
        msg.setDetailedText(
            f"缺少以下库：\n" + "\n".join(missing) + 
            "\n\n请运行以下命令安装：\npip install " + " ".join(missing)
        )
        msg.exec_()
        sys.exit(1)
    
    try:
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec_())
        
    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("应用程序错误")
        msg.setText("应用程序启动失败")
        msg.setDetailedText(f"错误信息：{str(e)}")
        msg.exec_()
        sys.exit(1)


if __name__ == "__main__":
    main()