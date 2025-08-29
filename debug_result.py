#!/usr/bin/env python3
"""
调试result数据结构
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trending_generator import TrendingGenerator

def debug_result():
    """调试result数据结构"""
    print("🔍 调试result数据结构")
    print("=" * 50)
    
    try:
        generator = TrendingGenerator()
        
        # 获取简化结果
        result = generator.get_simplified_result()
        
        print(f"result is None: {result is None}")
        print(f"result type: {type(result)}")
        
        if result:
            print(f"result keys: {list(result.keys())}")
            
            if 'general' in result:
                print(f"result['general'] type: {type(result['general'])}")
                print(f"result['general'] keys: {list(result['general'].keys()) if isinstance(result['general'], dict) else 'not dict'}")
                
                if isinstance(result['general'], dict) and 'items' in result['general']:
                    items = result['general']['items']
                    print(f"result['general']['items'] type: {type(items)}")
                    print(f"items length: {len(items) if hasattr(items, '__len__') else 'no len'}")
                    
                    if hasattr(items, '__iter__') and not isinstance(items, str):
                        print("Items is iterable")
                        try:
                            for i, item in enumerate(items[:2]):  # 只看前2个
                                print(f"  item {i} type: {type(item)}")
                                break
                        except Exception as e:
                            print(f"  Error iterating items: {e}")
                    else:
                        print("Items is NOT iterable")
                        print(f"Items value: {items}")
        else:
            print("No result found")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_result()