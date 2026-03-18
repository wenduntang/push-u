#!/bin/bash
# 用法: ./push.sh
# 或: ./push.sh 你的token
cd "$(dirname "$0")"
if [ -n "$1" ]; then
  token="$1"
else
  echo "请粘贴 Token（或运行: ./push.sh 你的token）"
  read -s token
fi
[ -z "$token" ] && { echo "未输入 Token"; exit 1; }
git remote remove origin 2>/dev/null
git remote add origin https://github.com/wenduntang/sandbox-security.git 2>/dev/null
git push https://wenduntang:${token}@github.com/wenduntang/sandbox-security.git main
echo "完成"
