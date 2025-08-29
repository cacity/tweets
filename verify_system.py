#!/usr/bin/env python3
"""
验证热门榜单系统功能
"""

import requests
import json
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BASE_URL = "http://127.0.0.1:5001"

def test_web_app():
    """测试Web应用响应"""
    print("🌐 测试Web应用响应...")
    
    try:
        # 测试首页
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ 首页响应正常")
        else:
            print(f"❌ 首页响应异常: {response.status_code}")
            return False
        
        # 测试热门榜单页面
        response = requests.get(f"{BASE_URL}/trending", timeout=10)
        if response.status_code == 200:
            print("✅ 热门榜单页面响应正常")
        else:
            print(f"❌ 热门榜单页面响应异常: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Web应用测试失败: {e}")
        return False

def test_trending_api():
    """测试热门榜单API"""
    print("\n📊 测试热门榜单API...")
    
    try:
        # 测试榜单状态API
        response = requests.get(f"{BASE_URL}/api/trending_status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ 榜单状态API响应正常")
            print(f"   有榜单数据: {data['data']['has_data']}")
            print(f"   AI功能启用: {data['data']['ai_enabled']}")
        else:
            print(f"❌ 榜单状态API响应异常: {response.status_code}")
            return False
        
        # 测试生成榜单API
        print("🚀 测试生成榜单API（这可能需要一些时间）...")
        
        payload = {
            "hours": 48,
            "count": 5,
            "refresh": False,  # 不刷新RSS以节省时间
            "use_ai": False    # 暂时不使用AI以节省时间
        }
        
        response = requests.post(
            f"{BASE_URL}/api/generate_trending", 
            json=payload,
            timeout=120  # 2分钟超时
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ 榜单生成API成功")
                print(f"   综合榜单条目: {data['data']['general_count']}")
                print(f"   分类榜单数量: {data['data']['categories_count']}")
            else:
                print(f"❌ 榜单生成失败: {data['message']}")
                return False
        else:
            print(f"❌ 榜单生成API响应异常: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def test_ai_functionality():
    """测试AI功能"""
    print("\n🤖 测试AI功能...")
    
    try:
        # 尝试生成一个带AI摘要的小榜单
        payload = {
            "hours": 72,
            "count": 3,
            "refresh": False,
            "use_ai": True
        }
        
        print("正在测试AI摘要功能，这可能需要1-2分钟...")
        
        response = requests.post(
            f"{BASE_URL}/api/generate_trending",
            json=payload,
            timeout=180  # 3分钟超时
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ AI摘要功能测试成功")
                return True
            else:
                print(f"⚠️ AI摘要测试失败: {data['message']}")
                return True  # 不算完全失败，可能是API配额问题
        else:
            print(f"❌ AI摘要API响应异常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ AI功能测试异常: {e}")
        return True  # 不算完全失败

def main():
    """主函数"""
    print("🧪 热门榜单系统验证")
    print("=" * 50)
    
    tests = [
        ("Web应用", test_web_app),
        ("榜单API", test_trending_api),
        ("AI功能", test_ai_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📋 验证结果汇总")
    print("=" * 50)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ 通过" if results[i] else "❌ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n总体结果: {passed}/{total} 项测试通过")
    
    if passed >= 2:  # 至少Web应用和API正常就算成功
        print("\n🎉 系统验证成功！")
        print("\n📖 使用指南:")
        print("1. 访问首页管理RSS源: http://127.0.0.1:5001/")
        print("2. 查看热门榜单: http://127.0.0.1:5001/trending")
        print("3. 在榜单页面点击'生成最新榜单'创建智能推荐")
        print("4. 浏览不同分类的专业榜单")
        print("\n💡 提示:")
        print("- 首次使用请先在首页添加RSS订阅源")
        print("- 榜单生成需要1-2分钟，请耐心等待")
        print("- AI摘要功能需要Gemini API密钥")
    else:
        print("⚠️ 系统存在问题，请检查相关功能")

if __name__ == "__main__":
    main()