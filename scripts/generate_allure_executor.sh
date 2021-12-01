#!bin/sh
# allure 执行者

executor="{ \n
    \"name\": \"$CI_PROJECT_NAME\",\n
    \"type\": \"gitlab\", \n
    \"url\": \"$CI_PIPELINE_URL\", \n
    \"buildName\": \"$CI_JOB_NAME #$CI_JOB_ID\", \n
    \"buildUrl\": \"$CI_JOB_URL\", \n
    \"reportUrl\": \"\", \n
    \"reportName\": \"\" \n
}
"

echo $executor
