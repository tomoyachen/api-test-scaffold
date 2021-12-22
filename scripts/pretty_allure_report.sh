#!bin/bash
# allure 美化报告

if [[ -d "allure-report" ]]; then
  # linux 是 sed -i, mac 是 sed -i '' 需要传入一个备份文件名，可为空
  sed -i 's/Allure Report/Project 1 测试报告/g' allure-report/index.html # 留的坑，本地和 CI 报告目录不同
  sed -i 's/Allure Report/Project 1 测试报告/g' allure-report/widgets/summary.json
  sed -i 's/rel="favicon"/rel="shortcut icon"/g' allure-report/index.html
  sed -i 's/favicon.ico?v=2/favicon.ico/g' allure-report/index.html
  cp -f favicon.ico allure-report/favicon.ico || true
fi
if [[ -d "allure-report-global" ]]; then
  sed -i 's/Allure Report/Project 1 测试报告/g' allure-report-global/index.html
  sed -i 's/Allure Report/Project 1 测试报告/g' allure-report-global/widgets/summary.json
  sed -i 's/rel="favicon"/rel="shortcut icon"/g' allure-report-global/index.html
  sed -i 's/favicon.ico?v=2/favicon.ico/g' allure-report-global/index.html
  cp -f favicon.ico allure-report-global/favicon.ico || true
fi