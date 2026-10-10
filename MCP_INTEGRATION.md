# MCP 接入说明（MCP_INTEGRATION.md）

本作品真实使用**麦当劳 MCP Server（`mcd-mcp`）**能力，服务地址 `https://mcp.mcd.cn`，传输协议 Streamable HTTP，鉴权方式为请求头 `Authorization: Bearer <MCP_TOKEN>`。

## 实际使用的工具（Tools）

| 工具名 | 用途 | 在本作品中的调用环节 |
| --- | --- | --- |
| `query-meals` | 查询当前门店可售餐品列表（含分类、餐品编码、标签） | 首次配置：模糊匹配用户口语菜名 → 真实商品 code；一键下单：复核两件组合品当前在售 code |
| `query-meal-detail` | 查询餐品详情 / 套餐组成 | 核对组合内容、可替换项（可选） |
| `query-nearby-stores` | 查询附近可用门店 | 到店 / 堂食模式：把用户说的店名/地名匹配到门店 code |
| `delivery-query-addresses` | 查询已保存配送地址 | 外送模式：匹配默认配送地址 id |
| `query-store-coupons` / `query-my-coupons` | 查询可用优惠券 | 下单前试算优惠（可选） |
| `calculate-price` | 商品价格计算（含优惠、配送费、应付总额） | 下单前向用户展示"主餐+小食=12 元"及应付金额 |
| `create-order` | 创建订单，**返回订单详情与支付链接（paymentUrl）** | 一键下单核心：生成订单并拿到支付页链接，直达付款 |
| `now-time-info` | 获取当前时间 | 营业时间判断（可选） |

## 调用流程

```
[首次配置]
用户大白话("吉士蛋麦满分加小薯条, 到店")
   └─ query-meals → 模糊匹配 → group_a.code / group_b.code
   └─ query-nearby-stores → 匹配 → store.code
   └─ 写入 selection.json（组合 + 就餐方式 + 门店，持久化）

[一键下单] 用户对 skill 发任意一句话
   └─ 读取 selection.json
   └─ query-meals 复核实时在售 code（停售则提示并退回配置）
   └─ [可选] query-store-coupons / calculate-price 试算
   └─ create-order → 返回 paymentUrl
   └─ 呈现订单摘要 + 支付链接（用户点击直达付款页）
```

## 业务价值
- **把多步操作压缩成一步**：原本"找 1+1 → 选两件 → 结算 → 付款"约 5 步，现在一句话触发。
- **降低决策负担**：固定口味用户无需每次重复选择，组合与门店一次锁定。
- **真实可用**：全程调用麦当劳官方 MCP 工具，订单与支付链接来自官方实时返回，非模拟。
- **普惠设计**：交互全程口语化，电脑小白也能零门槛复购。

## 接入配置（脱敏）
详见仓库根 `mcp-config.example.json`，仅使用环境变量占位符，不含任何真实 Token。
