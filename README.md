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
# 全局环境下执行（方式 1）
poetry run pytest testcase

# 进入虚拟环境后执行（方式 2）
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
# 执行用例时，生成结果（默认增量数据）
pytest testcase -s -v --alluredir=outputs/allure-results

# 执行用例时，生成结果（清除上一次数据）（基于 pytest.ini 默认参数）
pytest testcase -s -v --alluredir=outputs/allure-results --clean-alluredir
```
```bash
# 根据结果，启动报告 web 服务（仅启服务，适合本地浏览）
allure serve outputs/allure-results
```

```bash
# 根据结果，生成 html 报告文件（生成报告，适合 CI）
allure generate outputs/allure-results -o outputs/allure-report --clean
```

# CI/ CD
## 支持 GitLab CI
工作中一般使用公司仓库比较定制化的镜像，本项目使用的是完全免登录的第三方 docker 镜像

python:3.8 镜像，用于执行 pytest 测试

frankescobar/allure-docker-service:latest 镜像，用于 allure 生成报告

ref: https://github.com/fescobar/allure-docker-service

ref: https://tech-en.netlify.app/articles/en513432/index.html

## GitLab Pages
保持最新的测试报告，历史报告可以在 Pipleine allure-report Job 中访问。
