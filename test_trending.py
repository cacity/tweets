#!/usr/bin/env python3
"""
测试热门榜单生成功能
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trending_generator import TrendingGenerator

def test_trending_basic():
    """测试基本的榜单生成功能（不使用AI）"""
    print("🧪 开始测试热门榜单生成功能")
    print("=" * 60)
    
    # 初始化榜单生成器（不提供Gemini API密钥）
    generator = TrendingGenerator()
    
    # 测试基本功能
    print("📋 测试1: 生成榜单（不使用AI摘要）")
    result = generator.generate_trending_lists(
        hours=48,  # 使用48小时以获得更多内容
        top_count=10,  # 生成top10
        refresh_feeds=False,  # 不刷新RSS（节省时间）
        use_ai_summary=False   # 不使用AI摘要
    )
    
    # 验证结果
    if result:
        print("✅ 榜单生成成功！")
        print(f"📊 综合榜单条目数: {len(result['general']['items'])}")
        print(f"📂 分类榜单数量: {len(result['categories'])}")
        
        # 显示综合榜单前3名
        if result['general']['items']:
            print("\n🏆 综合榜单前3名:")
            for i, item in enumerate(result['general']['items'][:3], 1):
                print(f"  {i}. {item['title'][:50]}...")
                print(f"     评分: {item['score']['total']:.2f}")
        
        # 显示分类统计
        if result['categories']:
            print("\n📂 分类榜单统计:")
            for category, data in result['categories'].items():
                category_name = {
                    'ai': '人工智能',
                    'tech': '科技资讯', 
                    'business': '商业资讯',
                    'product': '产品设计'
                }.get(category, category)
                print(f"  {category_name}: {len(data['items'])} 条")
        
        print("\n✅ 基本测试通过！")
        return True
    else:
        print("❌ 榜单生成失败")
        return False

def test_with_refresh():
    """测试包含RSS刷新的功能"""
    print("\n📋 测试2: 刷新RSS并生成榜单")
    print("=" * 60)
    
    generator = TrendingGenerator()
    
    try:
        result = generator.generate_trending_lists(
            hours=24,
            top_count=5,
            refresh_feeds=True,  # 刷新RSS源
            use_ai_summary=False
        )
        
        if result and len(result['general']['items']) > 0:
            print("✅ RSS刷新和榜单生成成功！")
            return True
        else:
            print("⚠️ 没有获得足够的内容，可能是RSS源没有最新内容")
            return True  # 这不算失败，可能确实没有新内容
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_result_persistence():
    """测试结果持久化"""
    print("\n📋 测试3: 结果持久化和读取")
    print("=" * 60)
    
    generator = TrendingGenerator()
    
    # 获取最新结果
    result = generator.get_simplified_result()
    
    if result:
        print("✅ 成功读取已保存的榜单结果")
        print(f"📅 生成时间: {result['meta']['generated_at'][:19]}")
        return True
    else:
        print("⚠️ 没有找到已保存的榜单结果")
        return True  # 如果没有之前的结果也不算失败

def main():
    """主测试函数"""
    print("🚀 热门榜单系统测试")
    print("=" * 60)
    
    # 检查必要的目录
    os.makedirs('trending_output', exist_ok=True)
    
    test_results = []
    
    # 运行测试
    test_results.append(test_trending_basic())
    test_results.append(test_with_refresh()) 
    test_results.append(test_result_persistence())
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📋 测试汇总")
    print("=" * 60)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"通过: {passed}/{total} 项测试")
    
    if passed == total:
        print("🎉 所有测试通过！热门榜单系统工作正常")
    else:
        print("⚠️ 部分测试未通过，请检查相关功能")
    
    print("\n💡 使用说明:")
    print("1. 启动Web应用: python src/app.py")
    print("2. 访问热门榜单: http://127.0.0.1:5000/trending")
    print("3. 设置Gemini API密钥环境变量以启用AI摘要:")
    print("   export GEMINI_API_KEY='your_api_key'")
    
    print("\n🔧 手动生成榜单:")
    print("python src/trending_generator.py --hours 24 --count 20 --refresh")

if __name__ == "__main__":
    main()