#!/usr/bin/env python3
"""
刷新验证脚本的启动器
"""

import sys
import os

# 添加src目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

# 改变工作目录到src
os.chdir(src_dir)

# 导入并执行刷新验证脚本
if __name__ == "__main__":
    import refresh_and_verify
    refresh_and_verify.main()

