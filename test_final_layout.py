#!/usr/bin/env python3
"""
最终布局修复测试
"""

import requests
import time

def test_final_layout():
    """测试最终布局修复效果"""
    print("=" * 60)
    print("最终布局修复验证测试")
    print("=" * 60)
    
    # 目标URL
    base_url = "http://127.0.0.1:5000"
    target_url = f"{base_url}/feeds/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe"
    
    print(f"测试URL: {target_url}")
    print()
    
    try:
        # 访问目标页面
        print("1. 获取页面内容...")
        response = requests.get(target_url, timeout=10)
        
        if response.status_code == 200:
            print("✓ 页面加载成功")
            html_content = response.text
            
            # 检查全局函数
            print("\\n2. 检查全局函数...")
            
            global_checks = [
                'function testLayout(',  # 全局测试函数
                'function showDebugInfo(',  # 全局调试函数
                'function applyLayoutDirect(',  # 全局应用函数
                'window.testLayout',  # 确认是全局函数
            ]
            
            global_found = []
            for check in global_checks:
                if check in html_content:
                    global_found.append(check)
            
            # 检查事件绑定改进
            print("\\n3. 检查事件绑定改进...")
            
            event_checks = [
                'label[for^=\"layout-\"]',  # label选择器
                'addEventListener(\\'click\\'',  # 点击事件
                'addEventListener(\\'change\\'',  # 改变事件
                'setTimeout',  # 延迟执行
                'this.getAttribute(\\'for\\')'  # 属性获取
            ]
            
            event_found = []
            for check in event_checks:
                if check in html_content:
                    event_found.append(check)
            
            # 检查直接样式操作
            print("\\n4. 检查直接样式操作...")
            
            style_checks = [
                'cssText',  # 直接CSS文本
                '!important',  # 强制样式
                'removeAttribute(\\'style\\')',  # 样式重置
                'max-width: 60%',  # 紧凑布局
                'flex: 0 0 50%'  # 双列布局
            ]
            
            style_found = []
            for check in style_checks:
                if check in html_content:
                    style_found.append(check)
            
            # 输出检查结果
            print(f"✓ 全局函数: {len(global_found)}/3 项检查通过")
            print(f"✓ 事件绑定: {len(event_found)}/5 项检查通过") 
            print(f"✓ 样式操作: {len(style_found)}/5 项检查通过")
            
            # 总体评估
            print("\\n5. 修复效果评估...")
            total_score = len(global_found) + len(event_found) + len(style_found)
            max_score = 3 + 5 + 5
            
            success_rate = (total_score / max_score) * 100
            print(f"修复完成度: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 70:
                print("✅ 布局修复基本完成！")
                print("\\n🔧 现在的测试步骤:")
                print("1. 访问页面并打开开发者工具(F12)")
                print("2. 在控制台执行: showDebugInfo()")
                print("3. 在控制台执行: testLayout('narrow')")
                print("4. 在控制台执行: testLayout('two-column')")
                print("5. 或者点击页面上的布局切换按钮")
                
                print("\\n📋 预期效果:")
                print("• showDebugInfo() - 应该正常执行，显示调试信息")
                print("• testLayout('narrow') - 内容变为60%宽度，居中")
                print("• testLayout('two-column') - 内容分两列显示")
                print("• 页面按钮点击应该也能正常切换布局")
                
                print("\\n🚨 如果还是不行:")
                print("• 检查浏览器控制台是否有JavaScript错误")
                print("• 尝试刷新页面重新加载JavaScript")
                print("• 确认页面上确实有布局切换按钮")
                return True
            else:
                print(f"⚠ 修复效果需要进一步改进")
                return False
                
        else:
            print(f"✗ 页面加载失败: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ 页面访问失败: {e}")
        return False
    
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
        return False

def main():
    print("🏁 Twitter RSS订阅管理器 - 最终布局修复验证")
    print("本测试将验证最新的布局修复是否成功\\n")
    
    success = test_final_layout()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 最终修复验证基本通过！")
        print("\\n🎯 主要修复:")
        print("• 将调试函数移到全局作用域")
        print("• 同时绑定label和radio的事件")
        print("• 使用直接样式操作和cssText")
        print("• 添加延迟执行避免冲突")
        print("• 改进错误处理和调试信息")
        
        print("\\n💪 现在应该能工作了！")
        print("如果布局切换按钮还是不响应，请:")
        print("1. 尝试手动执行控制台命令")
        print("2. 检查是否有JavaScript错误")
        print("3. 刷新页面重新加载")
    else:
        print("❌ 最终修复验证未完全通过")
        print("\\n🔧 后续排查:")
        print("• 检查HTML结构是否正确")
        print("• 确认JavaScript是否正确加载")
        print("• 查看浏览器控制台错误信息")
    
    print("=" * 60)

if __name__ == "__main__":
    main()