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
poetry run pytest tests

# 进入虚拟环境后执行（方式 2）
poetry shell
pytest tests
```

# Allure Report
## 安装 JDK
JDK 下载地址：https://www.oracle.com/java/technologies/downloads/#java11-windows


## 安装 Allure
下载地址：https://github.com/allure-framework/allure2/releases
1. 下载最新 Release 版，例：`allure-2.16.1.zip`

2. 下载后解压到你本地目录

3. 配置环境变量，例：ALLURE_HOME: D:\Software\allure-2.13.9

## 生成报告
```bash
# 执行用例时，生成结果（默认增量数据）
pytest tests -s -v --alluredir=outputs/allure-results

# 执行用例时，生成结果（清除上一次数据）（基于 pytest.ini 默认参数）
pytest tests -s -v --alluredir=outputs/allure-results --clean-alluredir
```
```bash
# 根据结果，启动报告 web 服务（仅启服务，适合本地浏览）
allure serve outputs/allure-results
```

```bash
# 根据结果，生成 html 报告文件（生成报告，适合 CI）
allure generate outputs/allure-results -o outputs/allure-report --clean
```

## 额外信息
- environment、executors 数据，通过脚本生成
- trend 趋势图，通过 GitLab CI 处理数据

## 报告美化
- 报告 logo 需要修改 allure 客户端里的插件（这个等我更新自己打包 allure 镜像的时候演示）
- 报告网页 title、报告标题、favicon，通过脚本生成

# CI/ CD
## 镜像说明
工作中一般使用公司仓库比较定制化的镜像，本项目使用的是完全免登录的第三方 docker 镜像

python:3.8 镜像，用于执行 pytest 测试

frankescobar/allure-docker-service:latest 镜像，用于 allure 生成报告

ref: https://github.com/fescobar/allure-docker-service

ref: https://tech-en.netlify.app/articles/en513432/index.html

## 仅执行最近一次 merge 改动范围的用例（默认关闭）
如果有这个需求，可以将 .gitlab-ci.yml 中的 TESTCASE_DIR 默认值设为 ""。


## GitLab Pages
### 单次执行报告
allure-report job 会生成单次报告（allure-report 目录）和增量聚合报告（allure-report-global 目录）存放于 artifacts。
具体地址可以在 job 输出中找到。

### 增量聚合报告
pages job 会把增量聚合报告移至 public 目录，部署成 pages 页面。
具体地址可以在 job 输出中找到。


## 通知
### 飞书通知
需要在 GitLab CI 环境变量中配置 FEISHU_NOTY_TOKEN
如果需要@某人，请查阅官方文档，自定义机器人仅支持 openId 方式

## 已知问题
1. GitLab CI allure-report job 执行失败，错误信息如下
```bash
Could not generate report
java.nio.file.AccessDeniedException: allure-report-global/history/retry-trend.json
```
这是由于上一次 CI 运行到 allure-report job 时，取消了 job，有残留文件影响。

这种情况，可以在 Pipeline 列表页，点击 `清除 Runner 缓存` 