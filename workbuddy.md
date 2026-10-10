# workbuddy.md — 使用 WorkBuddy 开发本项目的对话上下文（节选）

> 说明：本文件用于核验本项目真实使用腾讯 WorkBuddy 智能体开发，符合「麦当劳程序员创意开发大赛」WorkBuddy 专项联动奖励条件。以下为开发过程中的关键上下文节选（已脱敏，不含任何真实 Token / 个人信息）。

## 开发背景与目标
- 用户希望参加「麦当劳程序员创意开发大赛」，参赛能力定为：基于 `mcd-mcp` 实现"1+1 随心配一键下单"——首次用大白话选好组合，之后一句话直达支付页。
- 明确约束：**所有要人操作的部分都要从简，电脑小白也能用**。因此把"查菜单、认商品码、选门店"全部下沉到 AI 与 MCP，用户只说人话、做确认。

## 关键决策（WorkBuddy 辅助梳理）
1. **能力边界**：skill 只负责"创建订单并返回支付链接"，不自动扣款；真实支付由用户在支付页完成。既满足"一键直达付款页"，又规避越权支付风险。
2. **一次配置持久化**：用 `selection.json` 保存组合 + 默认就餐方式/门店，使"后续任意一句话"都能零输入重建订单。
3. **真实 MCP 工具链**：`query-meals` → `query-nearby-stores` / `delivery-query-addresses` → `calculate-price` → `create-order`（返回支付链接）。
4. **口语化交互**：首次配置不抛菜单、不列 JSON，用户用大白话描述，AI 模糊匹配 + 回显确认；降低电脑小白门槛。
5. **合规**：`CONTEST_DECLARATION.md` 原文不动；配置仅用环境变量占位符，绝不落真实 Token。

## 产出文件
- `skill/SKILL.md`（两套运行逻辑，全程口语化）
- `skill/scripts/order_builder.py`、`skill/scripts/selection_store.py`（可运行校验）
- `skill/references/oneplus1-menu.md`（1+1 组合参考）
- `README.md` / `MCP_INTEGRATION.md` / `mcp-config.example.json` / `CONTEST_DECLARATION.md`（赛事要求）
- 本 `workbuddy.md`

## 验证
- 在 WorkBuddy 中对 `skill/scripts/order_builder.py` 做本地校验：`python order_builder.py` 可正确读取 `selection.json`、校验结构并构造下单骨架（dry-run）。
- 安装说明已写入 `README.md`，可在 WorkBuddy 中实测 `mcd-mcp` 工具调用与一键下单闭环。
