"""
简单的应用程序测试脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 全局导入所有模块
models_imported = False
feed_manager_imported = False
gui_components_imported = False

try:
    from models import Feed, FeedItem, FeedStore
    models_imported = True
except Exception as e:
    print(f"数据模型导入失败: {e}")

try:
    from feed_manager import FeedManager
    feed_manager_imported = True
except Exception as e:
    print(f"RSS管理器导入失败: {e}")

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from feed_dialog import AddFeedDialog
    from feed_viewer import FeedViewer
    from main_window import MainWindow
    gui_components_imported = True
except Exception as e:
    print(f"GUI组件导入失赅: {e}")

def test_imports():
    """测试所有导入是否正常"""
    success_count = 0
    total_count = 3
    
    if models_imported:
        print("✓ 数据模型导入成功")
        success_count += 1
    else:
        print("✗ 数据模型导入失败")
    
    if feed_manager_imported:
        print("✓ RSS管理器导入成功")
        success_count += 1
    else:
        print("✗ RSS管理器导入失败")
    
    if gui_components_imported:
        print("✓ GUI组件导入成功")
        success_count += 1
    else:
        print("✗ GUI组件导入失败")
    
    return success_count == total_count

def test_basic_functionality():
    """测试基本功能"""
    if not models_imported:
        print("✗ 由于数据模型导入失败，跳过基本功能测试")
        return False
        
    try:
        # 测试数据模型
        feed = Feed("测试订阅源", "http://example.com/rss")
        item = FeedItem("测试标题", "http://example.com/item1", "测试描述")
        feed.items.append(item)
        
        # 测试存储
        store = FeedStore()
        result = store.add_feed(feed)
        
        if result and len(store.get_all_feeds()) == 1:
            print("✓ 基本数据模型功能正常")
            return True
        else:
            print("✗ 数据模型功能异常")
            return False
            
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_gui_creation():
    """测试GUI创建"""
    if not gui_components_imported:
        print("✗ 由于GUI组件导入失败，跳过GUI测试")
        return False
        
    try:
        # 设置高DPI属性
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        
        # 创建应用程序实例
        app = QApplication(sys.argv)
        
        # 创建主窗口（但不显示）
        window = MainWindow()
        
        print("✓ GUI界面创建成功")
        
        # 清理资源
        window.close()
        app.quit()
        
        return True
    except Exception as e:
        print(f"✗ GUI创建失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试Twitter RSS订阅管理器...")
    print("=" * 40)
    
    all_passed = True
    
    # 运行测试
    if not test_imports():
        all_passed = False
    
    if not test_basic_functionality():
        all_passed = False
    
    if not test_gui_creation():
        all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("✓ 所有测试通过！应用程序可以正常运行。")
        print("\n启动应用程序: python main.py")
    else:
        print("✗ 有测试失败，请检查错误信息。")
    
    print("测试完成。")