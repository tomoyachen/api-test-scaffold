# API TEST SCAFFOLD

基于 PyTest + Requests + Allure 实现快速搭建 API 自动化测试项目的脚手架。

# Usage
## 安装依赖
本地无 Poetry 包管理工具，需先安装 Poetry
```bash
# Python 全局环境
pip install poetry
```

使用 Poetry 安装依赖
```bash
# Python 全局环境
poetry install
```

## 执行用例
```bash
# Python 全局环境
poetry run pytest testcase

# Poetry 虚拟环境
poetry shell
pytest testcase
```

# Allure Report
## 安装 Allure
下载地址：https://github.com/allure-framework/allure2/releases
1. 下载最新 Release 版，例：`allure-2.16.1.zip`

2. 下载后解压到你本地目录

3. 配置环境变量，例：ALLURE_HOME: D:\Software\allure-2.13.9

## 生成报告
```bash
# 命令行执行（默认增量报告）
pytest testcase -s -v --alluredir=outputs/report

# 命令行执行（清除上一次报告）（基于 pytest.ini 默认参数）
pytest testcase -s -v --alluredir=outputs/report --clean-alluredir

# 启动报告服务（仅启服务，适合本地浏览）
allure serve outputs/report

# 生成 html 报告（生成报告，适合 CI）
allure generate outputs/report -o outputs/report-html --clean
```