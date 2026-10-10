#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦麦 1+1 一键下单 —— 订单构造与校验工具（可独立运行，无需 MCP Token）。

职责：
1. 读取 selection.json（用户一次选定的一组合 + 默认就餐方式/门店）。
2. 校验结构完整性。
3. 构造 create-order 所需的商品列表与订单骨架（dry-run，不发起真实请求）。
4. 供 SKILL.md 在运行时参考调用参数结构。

真实点餐通过 WorkBuddy 的 mcd-mcp 连接器完成，本脚本仅做本地构造与校验，
便于电脑小白在无 Token 环境下也能验证配置是否写对。
"""
import json
import sys
import os

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "selection.json")


def load_selection(path=DEFAULT_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到 selection.json（{path}）。请先完成首次配置。")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_selection(sel):
    errors = []
    if not isinstance(sel, dict):
        errors.append("selection 必须是 JSON 对象")
        return errors
    if sel.get("dine_mode") not in ("takeaway", "delivery", "counter"):
        errors.append("dine_mode 必须是 takeaway / delivery / counter 之一")
    if "combo" not in sel or not isinstance(sel["combo"], dict):
        errors.append("缺少 combo 组合定义")
    else:
        for g in ("group_a", "group_b"):
            item = sel["combo"].get(g)
            if not item or not item.get("code") or not item.get("name"):
                errors.append(f"combo.{g} 缺少 code 或 name")
    if sel.get("dine_mode") in ("takeaway", "counter") and not sel.get("store", {}).get("code"):
        errors.append("到店/堂食模式缺少 store.code")
    if sel.get("dine_mode") == "delivery" and not sel.get("delivery_address", {}).get("id"):
        errors.append("外送模式缺少 delivery_address.id")
    return errors


def build_order_payload(sel):
    """构造 create-order 入参骨架（商品列表 + 就餐方式 + 门店/地址）。
    实际调用时应以 query-meals 复核后的实时 code 覆盖此处 code。"""
    items = [
        {
            "productCode": sel["combo"]["group_a"]["code"],
            "quantity": 1,
            "name": sel["combo"]["group_a"]["name"],
        },
        {
            "productCode": sel["combo"]["group_b"]["code"],
            "quantity": 1,
            "name": sel["combo"]["group_b"]["name"],
        },
    ]
    payload = {
        "dineMode": sel["dine_mode"],
        "items": items,
        "remark": "1+1 随心配 一键下单",
    }
    if sel["dine_mode"] in ("takeaway", "counter"):
        payload["storeCode"] = sel["store"]["code"]
    else:
        payload["addressId"] = sel["delivery_address"]["id"]
    return payload


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    try:
        sel = load_selection(path)
    except FileNotFoundError as e:
        print(f"[FAIL] {e}")
        sys.exit(2)
    errors = validate_selection(sel)
    if errors:
        print("[INVALID] selection.json 存在问题：")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    payload = build_order_payload(sel)
    print("[OK] selection.json 校验通过")
    print("构造的下单骨架（dry-run，未发起真实请求）：")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
