#!/usr/bin/env bash
# 一键发布到 GitHub 并完成大赛报名（需 GitHub Personal Access Token，含 repo 权限）
# 用法（在仓库根目录执行）：
#   bash publish.sh <GitHub用户名> <PAT> [仓库名]
#
# 说明：
#   - 会在你的 GitHub 账号下创建「公开」仓库（活动要求 Public）。
#   - 自动 git init / commit / push 当前目录全部文件。
#   - 自动在官方活动仓库提交报名 Issue（格式固定、≤1000 字、无图）。
#   - 仓库创建时间在本脚本执行当天，符合活动"2025-12-25 ~ 2026-10-25"要求。
set -e

USER="$1"
TOKEN="$2"
REPO="${3:-mcd-1plus1-quick-order}"
API="https://api.github.com"
AUTH="-u $USER:$TOKEN"

if [ -z "$USER" ] || [ -z "$TOKEN" ]; then
  echo "用法: bash publish.sh <GitHub用户名> <PAT> [仓库名]"
  exit 1
fi

echo "==> 1. 创建公开仓库 $REPO"
curl -s $AUTH -X POST "$API/user/repos" \
  -H "Accept: application/vnd.github+json" \
  -d "{\"name\":\"$REPO\",\"description\":\"麦当劳1+1随心配一键下单 Skill（麦当劳程序员创意开发大赛参赛作品）\",\"homepage\":\"https://github.com/M-China/mcd-developer-innovation-challenge\",\"public\":true,\"auto_init\":false}" \
  | head -c 300
echo

echo "==> 2. 初始化并提交"
git init -q
git add -A
git commit -q -m "feat: 麦当劳 1+1 随心配一键下单 Skill 初版"
git branch -M main
git remote add origin "https://$USER:$TOKEN@github.com/$USER/$REPO.git"
git push -u origin main

echo "==> 3. 提交报名 Issue（官方活动仓库）"
ISSUE_TITLE="参赛：麦麦 1+1 一键下单"
ISSUE_BODY="【参赛申请】
项目名称：麦麦 1+1 一键下单
项目地址：https://github.com/$USER/$REPO
项目简介：基于麦当劳 MCP（mcd-mcp）能力开发的 WorkBuddy Skill，专为电脑小白设计。首次用大白话告诉它常吃的「1+1=12元」随心配组合（如「吉士蛋麦满分加小薯条」），AI 自动查菜单、认商品码、记门店；之后对该 Skill 发送任意一句话（如「来」）即可自动调用麦当劳 MCP 重建订单并返回支付链接，直达付款页完成下单，把原本多步点餐压缩成一步。"

# 用 python3 安全构造 JSON（避免换行/引号问题）
PAYLOAD=$(python3 -c "import json,sys; print(json.dumps({'title':sys.argv[1],'body':sys.argv[2]}))" "$ISSUE_TITLE" "$ISSUE_BODY")

curl -s $AUTH -X POST "$API/repos/M-China/mcd-developer-innovation-challenge/issues" \
  -H "Accept: application/vnd.github+json" \
  -d "$PAYLOAD" | head -c 300
echo

echo "==> 完成。请前往该 Issue 查看系统回复的报名成功/失败通知（即你要求的「反馈提醒」）。"
