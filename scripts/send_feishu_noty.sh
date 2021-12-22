#!/bin/bash
# 发送飞书消息，数据来源基于 allure

# FEISHU_NOTY_TOKEN='' # 需要在 gitlab CI 设置中添加环境变量

title='API 自动化测试报告'
project='Project 1'
type='API'

summary=`cat allure-report/widgets/summary.json` || summary=`cat outputs/allure-report/widgets/summary.json` # 留的坑，本地和 CI 报告目录不同
passed=`echo $summary | grep -Eo '"passed" : [0-9]+?,' | grep -Eo '[0-9]+'`
failed=`echo $summary | grep -Eo '"failed" : [0-9]+?,' | grep -Eo '[0-9]+'`
broken=`echo $summary | grep -Eo '"broken" : [0-9]+?,' | grep -Eo '[0-9]+'`
skipped=`echo $summary | grep -Eo '"skipped" : [0-9]+?,' | grep -Eo '[0-9]+'`
unknown=`echo $summary | grep -Eo '"unknown" : [0-9]+?,' | grep -Eo '[0-9]+'`
total=`echo $summary | grep -Eo '"total" : [0-9]+' | grep -Eo '[0-9]+'`
rate=`awk 'BEGIN{printf "%0.1f", '$passed'/'$total'*100}'`
rate_without_skipped=`awk 'BEGIN{printf "%0.1f", ('$passed' + '$unknown' + '$skipped')/'$total'*100}'`

# 根据通过率 更换 header 颜色
headerColor='turquoise'
if [ `echo "$rate_without_skipped < 95" | bc` -eq 1 ];then
  headerColor='red'
elif [ `echo "$rate_without_skipped < 100" | bc` -eq 1 ];then
  headerColor='orange'
fi

start_timestamp=`echo $summary | grep -Eo '"start" : [0-9]+?,' | grep -Eo '[0-9]+'`
# linux 是 date -d, mac 是 date -r
start_datetime=`date -d @$(expr $start_timestamp / 1000) "+%Y-%m-%d %H:%M:%S"`

DING_URL="https://open.feishu.cn/open-apis/bot/v2/hook/${FEISHU_NOTY_TOKEN}"

curl $DING_URL -H "Content-Type: application/json" \
  -d "{
    \"msg_type\": \"interactive\",
    \"card\": {
      \"config\": {
        \"wide_screen_mode\": true
      },
      \"header\": {
        \"template\": \"${headerColor}\",
        \"title\": {
          \"content\": \"${title}\",
          \"tag\": \"plain_text\"
        }
      },
      \"elements\": [
        {
          \"fields\": [
            {
              \"is_short\": true,
              \"text\": {
                \"content\": \"**模块：**${project}\",
                \"tag\": \"lark_md\"
              }
            },
            {
              \"is_short\": true,
              \"text\": {
                \"content\": \"**平台：**${type}\",
                \"tag\": \"lark_md\"
              }
            },
            {
              \"is_short\": true,
              \"text\": {
                \"content\": \"**时间：**${start_datetime}\",
                \"tag\": \"lark_md\"
              }
            },
            {
              \"is_short\": true,
              \"text\": {
                \"content\": \"**负责人：**<at id=1>${GITLAB_USER_NAME}</at>\",
                \"tag\": \"lark_md\"
              }
            },
            {
              \"is_short\": true,
              \"text\": {
                \"content\": \"**通过率：**${rate}%\",
                \"tag\": \"lark_md\"
              }
            },
            {
              \"is_short\": false,
              \"text\": {
                \"content\": \"\",
                \"tag\": \"lark_md\"
              }
            },
            {
              \"is_short\": true,
              \"text\": {
                \"content\": \"📊  **总用例数：**${total}\n✅  **通过用例：**${passed}\n❌  **失败用例：**${failed}\n⛔  **错误用例：**${broken}\n🚧  **跳过用例：**${skipped}\n\",
                \"tag\": \"lark_md\"
              }
            }
          ],
          \"tag\": \"div\"
        },
        {
          \"tag\": \"hr\"
        },
        {
          \"tag\": \"div\",
          \"text\": {
            \"tag\": \"lark_md\",
            \"content\": \"🙋️  <a href='https://github.com/tomoyachen/api-test-scaffold'>我要反馈误报</a> ｜ 📝  <a href='${CI_JOB_URL}'>查看触发流程</a>\"
          },
          \"extra\": {
            \"tag\": \"button\",
            \"text\": {
              \"tag\": \"lark_md\",
              \"content\": \"查看报告\"
            },
            \"type\": \"primary\",
            \"url\": \"$CI_PAGES_URL\"
          }
        }
      ]
    }
}"