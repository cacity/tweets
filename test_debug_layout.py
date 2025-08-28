#!/usr/bin/env python3
"""
布局调试测试脚本
"""

import requests
import time

def test_debug_layout():
    """测试调试布局功能"""
    print("=" * 60)
    print("布局调试功能测试")
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
            
            # 检查调试功能
            print("\\n2. 检查调试功能...")
            
            # 检查调试按钮
            debug_checks = [
                'testLayout',  # 测试函数
                'showDebugInfo',  # 调试信息函数
                'debug-controls',  # 调试控制器
                '测试单列',  # 调试按钮文本
                '测试紧凑',
                '测试双列',
                '显示信息'
            ]
            
            debug_found = []
            for check in debug_checks:
                if check in html_content:
                    debug_found.append(check)
            
            if len(debug_found) >= 6:
                print(f"✓ 调试功能已添加 ({len(debug_found)}/{len(debug_checks)})")
            else:
                print(f"⚠ 部分调试功能缺失 ({len(debug_found)}/{len(debug_checks)})")
            
            # 检查直接样式操作
            style_checks = [
                'item.style.flex',  # 直接样式操作
                'container.style.maxWidth',  # 容器样式
                'backgroundColor',  # 调试背景色
                '60%',  # 紧凑布局宽度
                '50%'   # 双列布局宽度
            ]
            
            style_found = []
            for check in style_checks:
                if check in html_content:
                    style_found.append(check)
            
            if len(style_found) >= 4:
                print(f"✓ 直接样式操作已实现 ({len(style_found)}/{len(style_checks)})")
            else:
                print(f"⚠ 部分样式操作缺失 ({len(style_found)}/{len(style_checks)})")
            
            # 检查事件绑定
            event_checks = [
                'addEventListener',  # 事件监听
                'change',  # change事件
                'input[name="layout"]',  # 布局选择器
                'getElementById',  # 元素获取
                'querySelectorAll'  # 批量选择
            ]
            
            event_found = []
            for check in event_checks:
                if check in html_content:
                    event_found.append(check)
            
            if len(event_found) >= 4:
                print(f"✓ 事件绑定已实现 ({len(event_found)}/{len(event_checks)})")
            else:
                print(f"⚠ 部分事件绑定缺失 ({len(event_found)}/{len(event_checks)})")
            
            # 总体评估
            print("\\n3. 调试功能评估...")
            total_score = len(debug_found) + len(style_found) + len(event_found)
            max_score = len(debug_checks) + len(style_checks) + len(event_checks)
            
            success_rate = (total_score / max_score) * 100
            print(f"调试功能完整度: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 80:
                print("✅ 调试功能实现良好！")
                print("\\n🔧 调试方法:")
                print("1. 访问页面并打开浏览器开发者工具(F12)")
                print("2. 在控制台输入: showDebugInfo() 查看调试信息")
                print("3. 在控制台输入: testLayout('narrow') 测试紧凑布局")
                print("4. 在控制台输入: testLayout('two-column') 测试双列布局")
                print("5. 观察页面变化和控制台输出")
                
                print("\\n📋 预期效果:")
                print("• 紧凑布局：内容区域变为60%宽度，居中显示")
                print("• 双列布局：每个条目变为50%宽度，两列并排")
                print("• 调试模式会添加不同颜色的背景便于识别")
                return True
            else:
                print(f"⚠ 调试功能需要完善 (完整度: {success_rate:.1f}%)")
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
    print("🔍 Twitter RSS订阅管理器 - 布局调试测试")
    print("本测试将验证调试功能是否正确实现\\n")
    
    success = test_debug_layout()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 调试功能测试通过！")
        print("\\n🌟 调试工具:")
        print("• 直接样式操作，绕过CSS选择器问题")
        print("• 控制台调试函数，便于手动测试")
        print("• 可视化背景色，快速识别布局变化")
        print("• 详细的调试信息输出")
        
        print("\\n💡 排查步骤:")
        print("1. 访问页面，打开开发者工具")
        print("2. 执行 showDebugInfo() 查看当前状态")
        print("3. 执行 testLayout('narrow') 测试紧凑布局")
        print("4. 观察页面是否发生变化")
        print("5. 如果调试功能正常，说明是CSS选择器问题")
        print("6. 如果调试功能也不行，说明是JavaScript执行问题")
    else:
        print("❌ 调试功能测试失败")
        print("\\n🔍 建议检查:")
        print("• JavaScript是否正确加载")
        print("• 控制台是否有错误信息")
        print("• HTML结构是否正确")
    
    print("=" * 60)

if __name__ == "__main__":
    main()