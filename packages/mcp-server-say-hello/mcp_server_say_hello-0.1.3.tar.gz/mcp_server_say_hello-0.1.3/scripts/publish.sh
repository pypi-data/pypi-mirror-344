#!/bin/bash
# 构建并发布包
set -e

# 清理旧构建文件
rm -rf dist

# 安装工具
pip install --upgrade hatch twine

# 使用hatch构建包
hatch build

# 上传到PyPI（需要提前配置token）
twine upload dist/*