#!bin/sh
# 动态获取最近一次 merge 到本次提交的全部改动用例

COMMIT_BEFORE_SHA=$(git rev-list --merges -n 1 master || git rev-parse HEAD~1)
# echo $COMMIT_BEFORE_SHA
COMMIT_SHA=$(git rev-parse HEAD~0)
# echo $COMMIT_SHA
# echo $(git log -n 1 master --merges --pretty=format:"%H") # 获取最近一次 merge 的另一种写法
if [ "$COMMIT_BEFORE_SHA" = "$COMMIT_SHA" ];then
  TESTCASE_CHANGES=$(git diff --name-only --diff-filter=ACRM $(git rev-list --merges -n 2 master | nl | sort -nr | cut -f2) | grep -E '/test_[A-Za-z0-9_-]+?\.py$|/[A-Za-z0-9_-]+?_test\.py$' || echo '--collect-only')
else
  TESTCASE_CHANGES=$(git diff --name-only --diff-filter=ACRM $COMMIT_BEFORE_SHA $COMMIT_SHA | grep -E '/test_[A-Za-z0-9_-]+?\.py$|/[A-Za-z0-9_-]+?_test\.py$' || echo '--collect-only')
fi
echo $TESTCASE_CHANGES
