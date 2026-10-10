#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selection.json 读写与初始化工具。

首次配置时由 skill 调用：把用户用大白话选定、并经麦当劳 MCP 核对后的组合与门店写入磁盘。
电脑小白无需懂 JSON —— 这一步由 AI 在你确认后自动完成。

用法：
  python selection_store.py                 # 查看当前配置
  python selection_store.py '{"dine_mode":"takeaway",...}'   # 保存配置
"""
import json
import sys
import os
from datetime import datetime, timezone, timedelta

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "selection.json")


def save(selection: dict, path=DEFAULT_PATH):
    selection["version"] = 1
    selection["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(selection, f, ensure_ascii=False, indent=2)
    return path


def read(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f"[FAIL] JSON 解析失败：{e}")
            sys.exit(2)
        p = save(data)
        print(f"[OK] 已保存配置到 {p}")
    else:
        cur = read()
        print(json.dumps(cur, ensure_ascii=False, indent=2) if cur else "尚未配置（请先完成首次设置）")
