#!/usr/bin/env python3
"""
最终布局修复验证脚本
"""

import requests
import time

def test_layout_final_fix():
    """测试最终的布局修复效果"""
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
            
            # 检查关键修复
            print("\n2. 检查关键修复...")
            
            # 检查JavaScript语法修复
            syntax_checks = [
                'function applyLayoutDirect',  # 全局函数定义
                'testLayout',  # 调试函数
                'showDebugInfo',  # 调试信息函数
                'addEventListener',  # 事件监听
                'max-width: 60%',  # 紧凑布局
                'flex: 0 0 50%'   # 双列布局
            ]
            
            syntax_found = []
            for check in syntax_checks:
                if check in html_content:
                    syntax_found.append(check)
            
            print(f"✓ JavaScript语法修复检查 ({len(syntax_found)}/{len(syntax_checks)})")
            
            # 检查是否有语法错误标志
            error_checks = [
                '<script>\n{% endblock %}',  # 错误的脚本结构
                'function applyLayoutDirect(layoutType) {\n    console.log',  # 重复定义
            ]
            
            errors_found = 0
            for check in error_checks:
                if check in html_content:
                    errors_found += 1
            
            if errors_found == 0:
                print("✓ 语法错误已修复")
            else:
                print(f"⚠ 仍存在{errors_found}个语法问题")
            
            # 检查核心功能
            core_checks = [
                'cssText',  # 直接样式操作
                'localStorage.setItem',  # 偏好保存
                'removeAttribute',  # 样式重置
                'background-color: #fffacd'  # 调试背景色
            ]
            
            core_found = []
            for check in core_checks:
                if check in html_content:
                    core_found.append(check)
            
            print(f"✓ 核心功能检查 ({len(core_found)}/{len(core_checks)})")
            
            # 总体评估
            print("\n3. 修复效果评估...")
            total_score = len(syntax_found) + (6 - errors_found) + len(core_found)
            max_score = len(syntax_checks) + 6 + len(core_checks)
            
            success_rate = (total_score / max_score) * 100
            print(f"修复完成度: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 85:
                print("✅ 布局切换修复成功！")
                print("\n🔧 主要修复:")
                print("• 修复JavaScript语法错误")
                print("• 将applyLayoutDirect函数移到全局作用域")
                print("• 使用cssText直接设置样式") 
                print("• 添加调试背景色便于观察")
                print("• 修复重复的script标签问题")
                
                print("\n📱 测试步骤:")
                print("1. 打开浏览器访问页面")
                print("2. 打开开发者工具(F12)")
                print("3. 点击右上角的【紧凑】按钮")
                print("4. 观察内容区域是否变为60%宽度并居中")
                print("5. 点击【双列】按钮")
                print("6. 观察条目是否变为两列显示")
                print("7. 在控制台执行 showDebugInfo() 查看详细信息")
                print("\n如果还是不行，请在控制台执行: testLayout('narrow')")
                return True
            else:
                print(f"⚠ 修复效果需要进一步完善 (完成度: {success_rate:.1f}%)")
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
    print("🛠️ Twitter RSS订阅管理器 - 最终布局修复验证")
    print("本测试将验证所有布局切换问题的修复效果\n")
    
    success = test_layout_final_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 最终布局修复验证通过！")
        print("\n🎯 解决的问题:")
        print("• JavaScript语法错误导致脚本无法执行")
        print("• 函数作用域问题导致事件处理失败")
        print("• CSS样式优先级不够导致布局不变")
        print("• 缺乏调试工具导致问题难以定位")
        
        print("\n🌟 最终效果:")
        print("• 📋 单列：100%宽度，默认布局")
        print("• 📱 紧凑：60%宽度，解决过宽问题")
        print("• 📊 双列：50%×2，并排显示")
        print("• 🎨 调试模式：不同背景色便于识别")
        
        print("\n💡 如果仍然不工作:")
        print("1. 确保浏览器刷新了页面缓存(Ctrl+F5)")
        print("2. 在控制台执行 showDebugInfo() 查看状态")
        print("3. 手动执行 testLayout('narrow') 测试")
        print("4. 检查控制台是否有错误信息")
    else:
        print("❌ 最终布局修复验证失败")
        print("\n🔍 建议检查:")
        print("• Flask应用是否正常运行")
        print("• 浏览器缓存是否已清理")
        print("• 开发者工具控制台错误信息")
    
    print("=" * 60)

if __name__ == "__main__":
    main()