# Amazon Bedrock OpenAI GPT 模型使用指南

## 概述

Amazon Bedrock 已提供一整套 OpenAI GPT 模型。你可以通过**两种端点**（`bedrock-mantle` 与 `bedrock-runtime`）调用它们，并且**所有模型同时支持 Responses API 与 Chat Completions API**。

> 本文档依据 AWS 官方文档 [OpenAI models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-openai.html) 及各模型卡（截至 2026-10-16 核实）整理。模型阵容、可用区域与定价以官方文档为准。

## 支持的模型

| 模型 | Model ID（基础） | 说明 |
|------|------------------|------|
| GPT-6 Astra | `openai.gpt-6-astra` | OpenAI 能力最强的模型，面向复杂推理、编码、computer use、研究与文档创作 |
| GPT-6.1 Sol | `openai.gpt-6.1-sol` | 在多项高难度评测上接近 GPT-6 Astra，Sol 定价；兼顾能力与成本 |
| GPT-6 Sol | `openai.gpt-6-sol` | 面向复杂编码与 agentic 工作流 |
| GPT-6 Luna | `openai.gpt-6-luna` | 面向聚焦、高吞吐任务 |
| GPT-5.6 Sol | `openai.gpt-5.6-sol` | 前沿推理与 state-of-the-art agentic 能力，覆盖编码、网络安全与科研 |
| GPT-5.6 Terra | `openai.gpt-5.6-terra` | 性能对标 GPT-5.5、成本减半，面向大规模日常生产负载 |
| GPT-5.6 Luna | `openai.gpt-5.6-luna` | 以 OpenAI 最低成本提供快速推理，面向高吞吐任务 |
| Daybreak Red: GPT-5.6 Cyber | `openai.gpt-5.6-cyber` | 面向漏洞研究、exploit 复现与缓解开发的高度专用模型；**需申请 Trusted Access for Cyber**；仅 `bedrock-mantle` |
| Daybreak Blue: GPT-5.6 Sol | `openai.gpt-daybreak-blue-5.6-sol` | 面向经核验的防守方开展授权网络安全工作的专用模型；**需申请 Trusted Access for Cyber**；仅 `bedrock-mantle` |
| GPT-5.5 | `openai.gpt-5.5` | 面向复杂专业工作，适合高级编码、研究、分析与长时 agentic 任务 |
| GPT-5.4 | `openai.gpt-5.4` | 前沿推理、编码、computer use 与长上下文工作流；**支持 GovCloud (US-West)** |
| GPT OSS Safeguard 120B | `openai.gpt-oss-safeguard-120b` | 1200 亿参数开源安全模型，用于内容审核与护栏执行 |
| GPT OSS Safeguard 20B | `openai.gpt-oss-safeguard-20b` | 200 亿参数紧凑版开源安全模型，用于轻量内容审核 |
| gpt-oss-120b | `openai.gpt-oss-120b`（`bedrock-runtime` 上为 `openai.gpt-oss-120b-1:0`） | 1200 亿参数开源通用模型，用于文本生成、编码与推理 |
| gpt-oss-20b | `openai.gpt-oss-20b`（`bedrock-runtime` 上为 `openai.gpt-oss-20b-1:0`） | 200 亿参数开源模型，面向低算力下的高效文本生成与编码 |

> 完整、最新的模型清单见官方 [OpenAI - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-openai.html) 页面。

## 两种 API 对接方式（重点）

GPT 系列模型（GPT-6 / 6.1 / 5.6 / 5.5 / 5.4）可通过两个端点访问，并且在两个端点上都**同时支持 Responses API 与 Chat Completions API**，基础路径都是 `/openai/v1`（注意不是 `/v1`）。

> 官方模型卡中的例外（2026-10-16 核实）：
> - **Daybreak Red / Blue** 仅支持 `bedrock-mantle`，不支持 `bedrock-runtime`。
> - **GPT OSS 系列**（gpt-oss-120b/20b、GPT OSS Safeguard 120B/20B）：在 `bedrock-mantle` 上 base path 是 **`/v1`**（不是 `/openai/v1`），支持 Responses 与 Chat Completions；在 `bedrock-runtime` 上**不支持 Responses API**，只支持 Chat Completions / Converse / Invoke，且使用 In-Region 的基础 ID（非 CRIS ID）。

### 1. Metal API —— `bedrock-mantle` 端点（OpenAI 兼容）

- **基础 URL**：`https://bedrock-mantle.{region}.api.aws/openai/v1`
  - 例：region 为 `us-east-1` 时，URL 为 `https://bedrock-mantle.us-east-1.api.aws/openai/v1`
- **模型标识**：使用**基础 Model ID**，如 `openai.gpt-5.5`
- **推理端点（base path 固定为 `/openai/v1`）**：
  - Responses API：`/openai/v1/responses`
  - Chat Completions API：`/openai/v1/chat/completions`
- **模型发现**：走 `/v1/models`（不是 `/openai/v1/models`；对后者请求会返回 404）
- 适合希望以 OpenAI SDK/OpenAI 兼容方式直接接入的场景。

### 2. Runtime API —— `bedrock-runtime` 端点（标准 Bedrock Runtime）

- **基础 URL**：`https://bedrock-runtime.{region}.amazonaws.com/openai/v1`
- **模型标识**：GPT 系列在此端点**不支持 In-Region 调用**，必须使用**跨区域推理（CRIS）ID**：
  - Geo（US 地理）：`us.openai.gpt-5.5`
  - Global：`global.openai.gpt-5.5`
  - GPT-5.6 Terra / Luna 在印度区域（ap-south-1/2）另有 Geo ID：`in.openai.gpt-5.6-terra` / `in.openai.gpt-5.6-luna`
  - 例外：GPT OSS 系列在此端点使用 In-Region 基础 ID（如 `openai.gpt-oss-120b-1:0`、`openai.gpt-oss-safeguard-120b`），gpt-oss-120b/20b 在 GovCloud 另有 `us-gov.` Geo ID
- 除 OpenAI 兼容的 Responses / Chat Completions 外，`bedrock-runtime` 还支持 Bedrock 原生的 **Converse**（所有 GPT 模型）与 **Invoke**（GPT-6.1 Sol、GPT-6 Sol、GPT-6 Luna、GPT OSS 系列）。官方模型卡中 OpenAI 模型均**不支持 Messages API**。
- **AWS 建议新应用优先使用 `bedrock-runtime`**（与 Bedrock 其余能力、CRIS、服务层级等一致）。

| 对比项 | `bedrock-mantle`（Metal API） | `bedrock-runtime`（Runtime API） |
|--------|------------------------------|----------------------------------|
| 基础 URL | `https://bedrock-mantle.{region}.api.aws/openai/v1` | `https://bedrock-runtime.{region}.amazonaws.com/openai/v1` |
| base path | `/openai/v1` | `/openai/v1` |
| Responses API | ✅ `/openai/v1/responses` | ✅ |
| Chat Completions API | ✅ `/openai/v1/chat/completions` | ✅ |
| 模型标识 | 基础 ID（如 `openai.gpt-5.5`） | CRIS ID（如 `us.openai.gpt-5.5` / `global.openai.gpt-5.5`）；GPT OSS 例外 |
| 模型发现 | `/v1/models` | 见 Bedrock 模型列表 API |
| 其他 API | — | Converse；部分模型支持 Invoke（不支持 Messages） |
| AWS 建议 | OpenAI 兼容直连 | **新应用优先** |

## 前提条件

- 有效的 AWS 账号
- Python 3.8+
- 已安装 OpenAI SDK（见 `requirements.txt`，`openai>=1.78.0`）

## 第一步：获取 Bedrock API Key

1. 登录 AWS 控制台
2. 访问 [Amazon Bedrock API Keys 页面](https://console.aws.amazon.com/bedrock/home#/api-keys/long-term/create)
3. 点击创建长期 API Key
4. **保存好生成的 Key**（仅显示一次）

> 也可以不使用 API Key，改用 AWS 标准凭证链（SigV4）。见下方常见问题。

## 第二步：安装依赖

```bash
pip install -r requirements.txt
```

## 第三步：配置环境变量

根据你选择的端点（二选一）配置 `OPENAI_BASE_URL`。AWS 建议新应用优先使用 `bedrock-runtime`。

```bash
# Bedrock API Key（必须）
export OPENAI_API_KEY="<你的 Bedrock API Key>"

# 方式 A（推荐）：bedrock-runtime（Runtime API）
#   模型需使用 CRIS ID，如 us.openai.gpt-5.5 / global.openai.gpt-5.5
export OPENAI_BASE_URL="https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1"

# 方式 B：bedrock-mantle（Metal API，OpenAI 兼容）
#   模型使用基础 ID，如 openai.gpt-5.5
# export OPENAI_BASE_URL="https://bedrock-mantle.us-east-1.api.aws/openai/v1"
```

> **注意**：两种端点的基础路径都是 `openai/v1`，与其他模型使用的 `v1` 路径不同。SDK 的 `base_url` 设置到 `/openai/v1` 即可，SDK 会自动拼接 `/responses` 或 `/chat/completions`。
>
> **端点与模型 ID 必须配对**：`bedrock-mantle` 配基础 ID（`openai.gpt-5.5`），`bedrock-runtime` 配 CRIS ID（`us.openai.gpt-5.5` / `global.openai.gpt-5.5`），混用会调用失败。为了照抄即可运行，下面每个示例都**在代码里显式传入 `base_url`**，不依赖上面导出的 `OPENAI_BASE_URL`；每个标题都标明了所用端点。

## 第四步：运行测试

### Responses API 基础调用（bedrock-mantle，使用基础 ID）

```python
from openai import OpenAI

# bedrock-mantle（Metal API）+ 基础 ID
client = OpenAI(base_url="https://bedrock-mantle.us-east-1.api.aws/openai/v1")

response = client.responses.create(
    model="openai.gpt-5.5",
    input="请解释 Amazon Bedrock 的主要功能。",
)

print(response.output_text)
```

### Responses API 基础调用（bedrock-runtime，使用 CRIS ID）

```python
from openai import OpenAI

# bedrock-runtime（Runtime API）+ CRIS ID（不能用基础 ID）
client = OpenAI(base_url="https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1")

response = client.responses.create(
    model="us.openai.gpt-5.5",  # 或 global.openai.gpt-5.5
    input="请解释 Amazon Bedrock 的主要功能。",
)

print(response.output_text)
```

### Chat Completions API 调用（bedrock-mantle，使用基础 ID；两种端点均支持）

```python
from openai import OpenAI

# bedrock-mantle（Metal API）+ 基础 ID。
# 改用 bedrock-runtime 时须同时改两处：
#   base_url="https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1"
#   model="us.openai.gpt-5.6-sol"（或 global.openai.gpt-5.6-sol）
client = OpenAI(base_url="https://bedrock-mantle.us-east-1.api.aws/openai/v1")

completion = client.chat.completions.create(
    model="openai.gpt-5.6-sol",
    messages=[
        {"role": "system", "content": "你是一名资深 AWS 架构师，回答要简洁实用。"},
        {"role": "user", "content": "列出三条 Serverless 架构最佳实践。"},
    ],
)

print(completion.choices[0].message.content)
```

### 多轮对话 + 推理控制（bedrock-mantle，使用基础 ID）

```python
from openai import OpenAI

# bedrock-mantle（Metal API）+ 基础 ID；
# 走 bedrock-runtime 时改用 runtime base_url 与 us.openai.gpt-6-astra
client = OpenAI(base_url="https://bedrock-mantle.us-east-1.api.aws/openai/v1")

response = client.responses.create(
    model="openai.gpt-6-astra",
    input=[
        {
            "role": "developer",
            "content": "你是一名资深 AWS 架构师，回答要简洁实用。",
        },
        {
            "role": "user",
            "content": "设计一个支持 5 万并发用户的无服务器聊天架构。",
        },
    ],
    reasoning={"effort": "medium"},  # 可选: low / medium / high
)

print(response.output_text)
```

### 流式输出（bedrock-mantle，使用基础 ID）

```python
from openai import OpenAI

# bedrock-mantle（Metal API）+ 基础 ID
client = OpenAI(base_url="https://bedrock-mantle.us-east-1.api.aws/openai/v1")

stream = client.responses.create(
    model="openai.gpt-5.5",
    input="用 Python 实现一个二分搜索函数。",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
print()
```

### 工具调用（Function Calling，bedrock-mantle，使用基础 ID）

```python
from openai import OpenAI

# bedrock-mantle（Metal API）+ 基础 ID
client = OpenAI(base_url="https://bedrock-mantle.us-east-1.api.aws/openai/v1")

# Responses API 使用扁平结构：name/description/parameters 与 type 同级
# （不要嵌套在 "function" 下，否则会报 missing field `name`）
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名称"},
            },
            "required": ["location"],
        },
    }
]

response = client.responses.create(
    model="openai.gpt-5.5",
    input="北京今天天气怎么样？",
    tools=tools,
)

for item in response.output:
    if item.type == "function_call":
        print(f"调用函数: {item.name}")
        print(f"参数: {item.arguments}")
```

## 端点格式说明

```
# bedrock-mantle（Metal API）
https://bedrock-mantle.{region}.api.aws/openai/v1/responses
https://bedrock-mantle.{region}.api.aws/openai/v1/chat/completions

# bedrock-runtime（Runtime API）
https://bedrock-runtime.{region}.amazonaws.com/openai/v1/responses
https://bedrock-runtime.{region}.amazonaws.com/openai/v1/chat/completions
```

| 端点 | 示例 URL |
|------|----------|
| bedrock-mantle (us-east-1) | `https://bedrock-mantle.us-east-1.api.aws/openai/v1` |
| bedrock-runtime (us-east-1) | `https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1` |

> `base_url` 设置到 `/openai/v1` 即可，SDK 会自动拼接 `/responses` 或 `/chat/completions`。模型发现在 `bedrock-mantle` 上走 `/v1/models`。

## 支持的功能

| 功能 | 支持情况 |
|------|----------|
| Responses API | ✅（两种端点均支持；GPT OSS 系列仅 `bedrock-mantle`） |
| Chat Completions API | ✅（两种端点均支持） |
| Converse API | ✅（`bedrock-runtime`） |
| Invoke API | 部分模型（`bedrock-runtime`：GPT-6.1 Sol、GPT-6 Sol、GPT-6 Luna、GPT OSS 系列） |
| Messages API | ❌（官方模型卡中 OpenAI 模型均不支持） |
| 流式输出 (Streaming) | ✅ |
| 服务端工具调用 | ✅（`bedrock-mantle`；GPT 系列在 `bedrock-runtime` 上不支持） |
| 客户端工具调用 | ✅ |
| 图片输入 | ✅（GPT 系列；GPT OSS 系列仅文本） |
| `bedrock-mantle` 端点（Metal API） | ✅ |
| `bedrock-runtime` 端点（Runtime API） | ✅（AWS 建议新应用优先；Daybreak 不支持） |

## 可用区域（重点）

可用区域**按模型与端点而不同**，不再固定于 us-east-2 / us-west-2。Amazon Bedrock 提供三种推理方式：

- **In-Region**：请求保持在单个区域内，满足严格合规要求
- **Geo Cross-Region（Geo CRIS）**：在同一地理范围（US / EU / APAC）内跨区域路由，同时遵守数据驻留
- **Global Cross-Region（Global CRIS）**：在无数据驻留限制时可路由到全球任意区域

> 使用 `bedrock-runtime` 调用 GPT 系列时请用 CRIS ID：Geo 用 `us.openai.<model>`（GPT-5.6 Terra/Luna 在印度区域另有 `in.`），Global 用 `global.openai.<model>`。官方模型卡中 GPT 系列**没有** `eu.` / `apac.` Geo ID，欧洲、亚太等区域只能走 Global CRIS。

### 各模型可用区域（按模型列出）

下表依据 2026-10-16 抓取的各模型卡「Regional availability」整理。`bedrock-mantle` 一列都是 In-Region（基础 ID 直连）；`bedrock-runtime` 一列写的是**源区域**（发起请求的区域），GPT 系列在这些区域只能通过 CRIS 调用。

| 模型 | `bedrock-mantle`（Metal API，In-Region） | `bedrock-runtime`（Runtime API）源区域 | Geo CRIS | Global CRIS |
|------|------------------------------------------|----------------------------------------|----------|-------------|
| GPT-6 Astra | us-east-1、us-west-2（us-west-2 仅 Standard；Ultrafast 仅 us-east-1） | Geo+Global：us-east-1/2、us-west-1/2、ca-central-1、ca-west-1；仅 Global：eu-central-1、eu-north-1、eu-west-1/2/3、ap-northeast-1/2/3、ap-south-1、ap-southeast-1/2、sa-east-1 | `us.` | `global.` |
| GPT-6.1 Sol | us-east-1 | US 地理范围（源区域 us-east-1/2、us-west-1/2、ca-central-1、ca-west-1） | `us.` | `global.` |
| GPT-6 Sol | us-east-1 | Geo+Global：us-east-1/2、us-west-1/2、ca-central-1、ca-west-1；仅 Global：eu-central-1/2、eu-north-1、eu-south-1/2、eu-west-1/2/3、ap-east-2、ap-northeast-1/2/3、ap-south-1/2、ap-southeast-1~7、il-central-1、af-south-1、sa-east-1、mx-central-1 | `us.` | `global.` |
| GPT-6 Luna | us-east-1 | 同 GPT-6 Sol | `us.` | `global.` |
| GPT-5.6 Sol | us-east-1、us-east-2 | Geo+Global：us-east-1/2、us-west-1/2、ca-central-1、ca-west-1；仅 Global：eu-central-1/2、eu-north-1、eu-south-1/2、eu-west-1/2/3、ap-east-2、ap-northeast-1/2/3、ap-south-1/2、ap-southeast-1~7、il-central-1、me-central-1、me-south-1、af-south-1、sa-east-1 | `us.` | `global.` |
| GPT-5.6 Terra | us-east-1、us-east-2、us-west-2，**us-gov-west-1、us-gov-east-1（GovCloud）** | 同 GPT-5.6 Sol；另 ap-south-1/2 支持印度 Geo（`in.`） | `us.` / `in.` | `global.` |
| GPT-5.6 Luna | us-east-1、us-east-2、us-west-2，**us-gov-west-1、us-gov-east-1（GovCloud）** | 同 GPT-5.6 Terra | `us.` / `in.` | `global.` |
| Daybreak Red: GPT-5.6 Cyber | us-east-2 | 不支持 | — | — |
| Daybreak Blue: GPT-5.6 Sol | us-east-2 | 不支持 | — | — |
| GPT-5.5 | us-east-1、us-east-2 | Geo+Global：us-east-1/2、us-west-1/2、ca-central-1、ca-west-1；仅 Global：mx-central-1、eu-central-1/2、eu-north-1、eu-south-1/2、eu-west-1/2/3、ap-east-2、ap-northeast-1/2/3、ap-south-1/2、ap-southeast-1~7、il-central-1、me-central-1、me-south-1、af-south-1、sa-east-1 | `us.` | `global.` |
| GPT-5.4 | us-east-1、us-east-2、us-west-2，**us-gov-west-1（GovCloud US-West）** | 同 GPT-5.5 | `us.` | `global.` |
| gpt-oss-120b / gpt-oss-20b | 模型卡只给出一张合并的 In-Region 表：us-east-1/2、us-west-2、eu-central-1、eu-north-1、eu-south-1、eu-west-1/2、ap-northeast-1/2、ap-south-1、ap-southeast-1/2/3/4、sa-east-1、**us-gov-west-1（GovCloud）** | In-Region（基础 ID `openai.gpt-oss-*-1:0`），区域同左 | GovCloud 内 `us-gov.` | 不支持 |
| GPT OSS Safeguard 120B / 20B | 模型卡只给出一张合并的 In-Region 表：us-east-1/2、us-west-2、eu-central-1、eu-north-1、eu-south-1、eu-west-1/2、ap-northeast-1/2、ap-south-1、ap-southeast-1/2/3/4、sa-east-1 | In-Region，区域同左 | 不支持 | 不支持 |

> Geo CRIS 的目的区域取决于源区域。以 `us.` 为例：源区域 us-east-1/us-east-2/us-west-2 路由到 us-east-1、us-east-2、us-west-2；us-west-1 另含自身；ca-central-1 / ca-west-1 另含自身。准确路由可在源区域调用 [GetInferenceProfile](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetInferenceProfile.html) 查询。
>
> Daybreak 网络安全专用模型需申请 **Trusted Access for Cyber**。
>
> 区域会随官方更新而变化，请以官方页面为准：
> - [OpenAI 模型卡总览](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-openai.html)（每张卡含「Regional availability」）
> - [Regional availability by models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html)

## 模型参数

| 参数 | 说明 |
|------|------|
| 上下文窗口 | **1,050,000 tokens**（GPT-6 Astra / 6 Sol / 6 Luna、GPT-5.6 Sol / Terra / Luna、GPT-5.5、GPT-5.4）。其中 272K 为短/长上下文的计费阈值：输入 ≤272K 走短上下文计费，超过则整个请求按长上下文计费。例外：GPT-6.1 Sol 与 Daybreak Blue 标注 1M，Daybreak Red 标注 272K，GPT OSS 系列 128K |
| 最大输出 | **128,000 tokens**（同上 GPT 系列）；例外：GPT-6.1 Sol 为 131,072，GPT OSS 系列为 16K |
| `reasoning.effort` | `low` / `medium` / `high`（控制推理深度） |
| 服务层级（service_tier） | GPT 系列只支持 Standard（`"service_tier": "default"` 或省略）；GPT-6 Astra 与 GPT-6.1 Sol 另支持 `ultrafast`；GPT OSS 系列支持 Standard / Priority / Flex。所有 OpenAI 模型都不支持 Reserved |

## 定价

定价按 token 计费、按模型与服务层级而不同，且区分短/长上下文。本文不写死数字，请以官方页面为准：

- [Amazon Bedrock 定价](https://aws.amazon.com/bedrock/pricing/)
- 各模型卡中的 Pricing 部分

## 常见问题

**Q: `bedrock-mantle` 和 `bedrock-runtime` 有什么区别，该用哪个？**

A: 两者都支持 Responses API 与 Chat Completions API，base path 都是 `/openai/v1`。区别在于：`bedrock-mantle`（Metal API）是 OpenAI 兼容端点，使用基础 Model ID；`bedrock-runtime`（Runtime API）调用 GPT 系列时使用跨区域推理 ID（`us.` / `global.` 前缀），并额外支持 Converse（部分模型还支持 Invoke）。**AWS 建议新应用优先使用 `bedrock-runtime`**。

**Q: 为什么环境变量叫 `OPENAI_API_KEY` 但用的是 AWS 的 Key？**

A: 因为使用的是 OpenAI SDK，它读取 `OPENAI_API_KEY` 环境变量，但实际的凭证是从 Amazon Bedrock 控制台生成的。

**Q: 能否使用 AWS IAM 凭证代替 API Key？**

A: 可以。如果不设置 Bedrock API Key，SDK 会回退到 AWS 标准凭证链（`~/.aws/credentials` 或环境变量 `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`），以 SigV4 签名请求。

**Q: 这么多模型怎么选？**

A: 追求最强能力选 GPT-6 Astra / GPT-6.1 Sol；复杂编码与 agentic 工作流选 GPT-6 Sol / GPT-5.6 Sol / GPT-5.5；大规模日常生产负载选 GPT-5.6 Terra（对标 GPT-5.5、成本减半）；高吞吐、低成本选 GPT-6 Luna / GPT-5.6 Luna；内容审核与护栏选 GPT OSS Safeguard 系列；需要开源通用模型选 gpt-oss-120b / 20b。网络安全专用的 Daybreak（GPT-5.6 Cyber / Sol）需申请 **Trusted Access for Cyber**。

**Q: 上下文窗口到底多大？**

A: GPT 系列（GPT-6 Astra / 6 Sol / 6 Luna、GPT-5.6 Sol / Terra / Luna、GPT-5.5、GPT-5.4）为 1,050,000 tokens，最大输出 128,000 tokens（GPT-6.1 Sol、Daybreak、GPT OSS 例外，见「模型参数」）。文档中的 272K 是短/长上下文的**计费阈值**（输入 ≤272K tokens 按短上下文计费），不是上下文窗口上限。

**Q: 数据安全如何保障？**

A: 可按需选择 In-Region（单区域，满足严格数据驻留）、Geo CRIS（同一地理范围内跨区域）或 Global CRIS（全球）。按 token 计费，无席位许可费用。

## 参考链接

- [OpenAI - Amazon Bedrock（模型卡总览）](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-openai.html)
- [GPT-6 Astra 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-6-astra.html)
- [GPT-6.1 Sol 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-6-1-sol.html)
- [GPT-5.6 Sol 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html)
- [GPT-5.5 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-55.html)
- [GPT-5.4 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html)
- [区域可用性（Regional availability by models）](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html)
- [Amazon Bedrock 定价](https://aws.amazon.com/bedrock/pricing/)
- [OpenAI on Amazon Bedrock](https://aws.amazon.com/bedrock/openai/)
- [OpenAI Codex on Amazon Bedrock](https://developers.openai.com/codex/amazon-bedrock)（在 Bedrock 上使用 Codex）
- [Bedrock API Key 管理](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html)
