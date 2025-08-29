#!/usr/bin/env python3
"""
快速测试热门榜单核心功能
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_components():
    """测试基本组件"""
    print("🔧 测试基本组件...")
    
    try:
        # 测试内容评分器
        from content_ranker import ContentRanker
        ranker = ContentRanker()
        print("✅ ContentRanker 初始化成功")
        
        # 测试Gemini服务
        from gemini_service import GeminiService
        gemini = GeminiService()
        print(f"✅ GeminiService 初始化: {'启用' if gemini.enabled else '未启用'}")
        
        # 测试Feed管理器
        from feed_manager import FeedManager
        feed_manager = FeedManager()
        feeds = feed_manager.get_all_feeds()
        print(f"✅ FeedManager 初始化成功，当前有 {len(feeds)} 个RSS源")
        
        # 获取内容项
        all_items = feed_manager.get_all_content_items()
        recent_items = feed_manager.get_recent_content(72)  # 72小时内容
        print(f"✅ 总内容项: {len(all_items)}, 最近72小时: {len(recent_items)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 组件测试失败: {e}")
        return False

def test_ranking_system():
    """测试评分系统"""
    print("\n🎯 测试评分系统...")
    
    try:
        from feed_manager import FeedManager
        from content_ranker import ContentRanker
        
        feed_manager = FeedManager()
        ranker = ContentRanker()
        
        # 获取最近内容
        recent_items = feed_manager.get_recent_content(72)
        
        if not recent_items:
            print("⚠️ 没有最近的内容可供测试")
            return True
        
        # 测试内容排序
        rankings = ranker.rank_content(recent_items[:10], 5)  # 只测试前10个内容的前5名
        
        if rankings:
            print(f"✅ 成功生成 {len(rankings)} 条排序结果")
            for i, item in enumerate(rankings[:3], 1):
                score = item['score']
                print(f"  {i}. {item['item'].title[:40]}...")
                print(f"     总分: {score.total_score:.2f}, 分类: {score.category}")
        
        # 测试分类排序
        category_rankings = ranker.get_category_rankings(recent_items[:20], 3)
        print(f"✅ 生成 {len(category_rankings)} 个分类排序")
        
        return True
        
    except Exception as e:
        print(f"❌ 评分系统测试失败: {e}")
        return False

def test_ai_summary():
    """测试AI摘要功能"""
    print("\n🤖 测试AI摘要功能...")
    
    try:
        from gemini_service import GeminiService
        
        gemini = GeminiService()
        
        if not gemini.enabled:
            print("⚠️ Gemini API未启用，跳过AI摘要测试")
            return True
        
        # 测试摘要生成
        test_content = """
        人工智能技术正在快速发展，最新的大语言模型在各个领域都展现出了惊人的能力。
        从文本生成到代码编写，从数据分析到创意设计，AI正在改变我们的工作方式。
        这些技术的应用前景广阔，但也带来了一些挑战和思考。
        """
        
        summary = gemini.generate_summary(test_content, 100)
        
        if summary:
            print(f"✅ AI摘要生成成功:")
            print(f"   原文长度: {len(test_content)} 字符")
            print(f"   摘要长度: {len(summary)} 字符") 
            print(f"   摘要内容: {summary}")
        else:
            print("⚠️ AI摘要生成失败")
        
        return True
        
    except Exception as e:
        print(f"❌ AI摘要测试失败: {e}")
        return False

def test_trending_generator():
    """测试榜单生成器"""
    print("\n📊 测试榜单生成器...")
    
    try:
        from trending_generator import TrendingGenerator
        
        generator = TrendingGenerator()
        
        # 检查是否有现有结果
        existing_result = generator.get_simplified_result()
        
        if existing_result:
            print("✅ 发现现有榜单结果:")
            print(f"   生成时间: {existing_result['meta']['generated_at'][:19]}")
            print(f"   综合榜单: {len(existing_result['general']['items'])} 条")
            print(f"   分类榜单: {len(existing_result['categories'])} 个")
        else:
            print("⚠️ 没有找到现有的榜单结果")
        
        # 测试快速生成（不刷新RSS，不使用AI）
        print("🚀 测试快速榜单生成（不刷新RSS，不使用AI）...")
        
        result = generator.generate_trending_lists(
            hours=48,  # 48小时
            top_count=5,  # 只生成Top5
            refresh_feeds=False,  # 不刷新RSS
            use_ai_summary=False  # 不使用AI
        )
        
        if result:
            print("✅ 榜单生成成功!")
            print(f"   综合榜单: {len(result['general']['items'])} 条")
            print(f"   分类榜单: {len(result['categories'])} 个")
            
            # 显示前3名
            if result['general']['items']:
                print("🏆 综合榜单前3名:")
                for i, item in enumerate(result['general']['items'][:3], 1):
                    print(f"  {i}. {item['title'][:50]}...")
                    print(f"     评分: {item['score']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 榜单生成器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 热门榜单系统快速测试")
    print("=" * 60)
    
    # 确保输出目录存在
    os.makedirs('trending_output', exist_ok=True)
    
    tests = [
        ("基本组件", test_basic_components),
        ("评分系统", test_ranking_system),
        ("AI摘要", test_ai_summary),
        ("榜单生成器", test_trending_generator)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append(False)
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📋 测试汇总")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ 通过" if results[i] else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统工作正常")
        print("\n🌐 现在可以启动Web应用测试:")
        print("python src/app.py")
        print("然后访问: http://127.0.0.1:5000/trending")
    else:
        print("⚠️ 部分测试未通过，请检查相关功能")

if __name__ == "__main__":
    main()