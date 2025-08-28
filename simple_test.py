"""
简化的测试脚本 - 测试应用程序基本功能
"""

def test_basic_imports():
    """测试基本导入"""
    print("测试基本导入...")
    try:
        # 测试数据模型
        from models import Feed, FeedItem, FeedStore
        print("✓ 数据模型导入成功")
        
        # 测试管理器
        from feed_manager import FeedManager
        print("✓ RSS管理器导入成功")
        
        # 测试GUI组件
        from feed_dialog import AddFeedDialog
        from feed_viewer import FeedViewer  
        from main_window import MainWindow
        print("✓ GUI组件导入成功")
        
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_data_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    try:
        from models import Feed, FeedItem, FeedStore
        
        # 创建测试数据
        feed = Feed("测试RSS", "http://test.com/rss.xml")
        item = FeedItem("测试文章", "http://test.com/article1", "测试内容")
        feed.items.append(item)
        
        # 测试存储
        store = FeedStore()
        result = store.add_feed(feed)
        
        if result and len(store.get_all_feeds()) == 1:
            print("✓ 数据模型功能正常")
            return True
        else:
            print("✗ 数据模型功能异常")
            return False
            
    except Exception as e:
        print(f"✗ 数据模型测试失败: {e}")
        return False

def test_feed_manager():
    """测试RSS管理器"""
    print("\n测试RSS管理器...")
    try:
        from feed_manager import FeedManager
        
        # 创建管理器实例
        manager = FeedManager("test_feeds.json")
        feeds = manager.get_all_feeds()
        
        print(f"✓ RSS管理器初始化成功，当前有 {len(feeds)} 个订阅源")
        return True
        
    except Exception as e:
        print(f"✗ RSS管理器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Twitter RSS订阅管理器 - 简化测试")
    print("=" * 50)
    
    tests = [
        ("基本导入", test_basic_imports),
        ("数据模型", test_data_models), 
        ("RSS管理器", test_feed_manager),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name}测试出现异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有基础测试通过！")
        print("可以尝试运行: python main.py")
    else:
        print("✗ 部分测试失败，请检查错误信息")
    
    print("=" * 50)

if __name__ == "__main__":
    main()