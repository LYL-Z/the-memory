#!/bin/bash
# 知识库每日自动备份推送
# 路径：The Memory/The Memory/scripts/push_vault.sh
# 作用：git add -A +（有变更则提交）+ 推送到 GitHub 私有库 origin/master
# 已内置本机三处坑的绕过：死代理(:11119)、凭据助手绝对路径、LFS。
# 私密层 私人资料/ 被 .gitignore 排除，不会上传。
set -euo pipefail
cd "D:/The Memory/The Memory"

# 仅在有变更时提交
if [ -n "$(git status --porcelain)" ]; then
  TS=$(date +%Y-%m-%dT%H:%M)
  git add -A
  git commit -m "chore: 自动备份推送 $TS"
  echo "已提交：$TS"
else
  echo "无变更，跳过提交。"
fi

# 推送：清空 git 死代理（回退沙箱环境代理），用 PATH 中的 gh 作凭据助手
git -c http.proxy= -c https.proxy= \
    -c "credential.https://github.com.helper=!gh auth git-credential" \
    push origin master
echo "DONE HEAD=$(git rev-parse HEAD)"
