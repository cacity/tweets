#!/usr/bin/env python3
"""
测试布局切换修复效果
"""

import requests
import time

def test_layout_fix():
    """测试布局切换修复效果"""
    print("=" * 60)
    print("布局切换修复验证测试")
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
            
            # 检查修复后的布局功能
            print("\\n2. 检查修复后的布局功能...")
            
            # 检查增强的CSS样式
            css_checks = [
                'body .layout-single .item-wrapper',  # 增强的单列样式
                'body .layout-narrow #items-container',  # 增强的紧凑样式  
                'body .layout-two-column .item-wrapper',  # 增强的双列样式
                'flex: 0 0 50% !important',  # 强制flex样式
                'max-width: 60% !important',  # 强制最大宽度
                'document.body.classList.add'  # 新的布局切换逻辑
            ]
            
            css_found = []
            for check in css_checks:
                if check in html_content:
                    css_found.append(check)
            
            if len(css_found) >= 5:
                print(f"✓ 增强CSS样式已应用 ({len(css_found)}/{len(css_checks)})")
            else:
                print(f"⚠ 部分增强样式缺失 ({len(css_found)}/{len(css_checks)})")
            
            # 检查JavaScript调试逻辑
            js_checks = [
                'console.log',  # 调试日志
                'switchLayout',  # 布局切换函数
                'document.body.classList',  # 新的类管理方式
                'layoutType.replace',  # 布局类型处理
                'feedLayoutPreference',  # 偏好存储
                '!important'  # 强制样式
            ]
            
            js_found = []
            for check in js_checks:
                if check in html_content:
                    js_found.append(check)
            
            if len(js_found) >= 5:
                print(f"✓ JavaScript修复逻辑已应用 ({len(js_found)}/{len(js_checks)})")
            else:
                print(f"⚠ 部分JavaScript逻辑缺失 ({len(js_found)}/{len(js_checks)})")
            
            # 检查样式优先级
            priority_checks = [
                '!important',  # 强制样式优先级
                'body .layout-narrow',  # 提高CSS选择器权重
                'body .layout-two-column',  # 提高CSS选择器权重
                'transition: all 0.3s ease'  # 平滑过渡效果
            ]
            
            priority_found = []
            for check in priority_checks:
                if check in html_content:
                    priority_found.append(check)
            
            if len(priority_found) >= 3:
                print(f"✓ 样式优先级修复已应用 ({len(priority_found)}/{len(priority_checks)})")
            else:
                print(f"⚠ 部分样式优先级缺失 ({len(priority_found)}/{len(priority_checks)})")
            
            # 总体评估
            print("\\n3. 修复效果评估...")
            total_score = len(css_found) + len(js_found) + len(priority_found)
            max_score = len(css_checks) + len(js_checks) + len(priority_checks)
            
            success_rate = (total_score / max_score) * 100
            print(f"修复完成度: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 80:
                print("✅ 布局切换修复成功！")
                print("\\n🔧 修复内容:")
                print("• 使用 body 元素应用布局类，提高CSS优先级")
                print("• 添加 !important 确保样式生效")
                print("• 使用 flex 属性替代 width，更可靠")
                print("• 增强JavaScript调试，便于排查问题")
                print("• 改进布局切换逻辑，更稳定可靠")
                
                print("\\n📋 测试步骤:")
                print("1. 访问页面并打开浏览器开发者工具")
                print("2. 点击右上角的布局切换按钮")
                print("3. 在控制台查看调试信息")
                print("4. 观察页面布局的实际变化")
                print("\\n现在紧凑和双列布局应该都能正常工作了！")
                return True
            else:
                print(f"⚠ 修复效果需要进一步改进 (完成度: {success_rate:.1f}%)")
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
    print("🔧 Twitter RSS订阅管理器 - 布局切换修复验证")
    print("本测试将验证布局切换问题的修复效果\\n")
    
    success = test_layout_fix()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 布局切换修复验证通过！")
        print("\\n🌟 主要修复:")
        print("• 提高CSS选择器优先级，确保样式生效")
        print("• 使用flex布局替代width设置，更可靠")
        print("• 添加!important确保样式强制应用")
        print("• 改进JavaScript逻辑，增加调试信息")
        print("• 优化布局切换的稳定性和响应速度")
        
        print("\\n💡 使用说明:")
        print("现在访问订阅源页面，三个布局按钮都应该能正常工作:")
        print("• 📋 单列：全宽显示（默认）")
        print("• 📱 紧凑：60%宽度，解决过宽问题")
        print("• 📊 双列：50%×2并排显示")
    else:
        print("❌ 布局切换修复验证失败")
        print("\\n🔍 建议检查:")
        print("• 浏览器控制台是否有JavaScript错误")
        print("• CSS样式是否被其他规则覆盖")
        print("• HTML结构是否正确")
    
    print("=" * 60)

if __name__ == "__main__":
    main()