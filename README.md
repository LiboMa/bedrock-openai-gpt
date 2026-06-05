# Amazon Bedrock OpenAI GPT 模型使用指南

## 概述

Amazon Bedrock 现已支持 OpenAI GPT-5.5 和 GPT-5.4 模型，通过 `bedrock-mantle` 端点使用 OpenAI Responses API 进行调用。

| 模型 | Model ID | 可用区域 | 特点 |
|------|----------|----------|------|
| GPT-5.5 | `openai.gpt-5.5` | us-east-2 (Ohio) | 最强能力，适合复杂推理和代理任务 |
| GPT-5.4 | `openai.gpt-5.4` | us-east-2 (Ohio), us-west-2 (Oregon) | 最佳性价比，适合生产工作流 |

## 前提条件

- 有效的 AWS 账号
- Python 3.8+
- 已安装 OpenAI SDK

## 第一步：获取 Bedrock API Key

1. 登录 AWS 控制台
2. 访问 [Amazon Bedrock API Keys 页面](https://console.aws.amazon.com/bedrock/home#/api-keys/long-term/create)
3. 点击创建长期 API Key
4. **保存好生成的 Key**（仅显示一次）

## 第二步：安装依赖

```bash
pip install -r requirements.txt
```

## 第三步：配置环境变量

```bash
# Bedrock API Key（必须）
export OPENAI_API_KEY="<你的 Bedrock API Key>"

# 端点 URL（根据区域选择）
# Ohio (us-east-2) - GPT-5.5 和 GPT-5.4 均可用
export OPENAI_BASE_URL="https://bedrock-mantle.us-east-2.api.aws/openai/v1"

# Oregon (us-west-2) - 仅 GPT-5.4 可用
# export OPENAI_BASE_URL="https://bedrock-mantle.us-west-2.api.aws/openai/v1"
```

> **注意**：端点路径为 `openai/v1`，与其他模型使用的 `v1` 路径不同。

## 第四步：运行测试

### 基础调用（GPT-5.5）

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="openai.gpt-5.5",
    input="请解释 Amazon Bedrock 的主要功能。",
)

print(response.output_text)
```

### 基础调用（GPT-5.4）

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="openai.gpt-5.4",
    input="请解释 Amazon Bedrock 的主要功能。",
)

print(response.output_text)
```

### 多轮对话 + 推理控制

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="openai.gpt-5.5",
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

### 流式输出

```python
from openai import OpenAI

client = OpenAI()

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

### 工具调用（Function Calling）

```python
from openai import OpenAI

client = OpenAI()

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
https://bedrock-mantle.{region}.api.aws/openai/v1/responses
```

| 区域 | 端点 URL |
|------|----------|
| us-east-2 (Ohio) | `https://bedrock-mantle.us-east-2.api.aws/openai/v1/responses` |
| us-west-2 (Oregon) | `https://bedrock-mantle.us-west-2.api.aws/openai/v1/responses` |

> SDK 的 `base_url` 设置到 `/openai/v1` 即可，SDK 会自动拼接 `/responses` 路径。

## 支持的功能

| 功能 | 支持情况 |
|------|----------|
| Responses API | ✅ |
| 流式输出 (Streaming) | ✅ |
| 服务端工具调用 | ✅ |
| 客户端工具调用 | ✅ |
| 图片输入 | ✅ |
| Chat Completions API | ❌ |
| Converse API | ❌ |
| bedrock-runtime 端点 | ❌ |

## 模型参数

| 参数 | 说明 |
|------|------|
| 上下文窗口 | 272K tokens |
| 最大输出 | 无硬性限制 |
| `reasoning.effort` | `low` / `medium` / `high`（控制推理深度） |

## 常见问题

**Q: 为什么环境变量叫 `OPENAI_API_KEY` 但用的是 AWS 的 Key？**

A: 因为使用的是 OpenAI SDK，它读取 `OPENAI_API_KEY` 环境变量，但实际的凭证是从 Amazon Bedrock 控制台生成的。

**Q: 能否使用 AWS IAM 凭证代替 API Key？**

A: 可以。如果不设置 Bedrock API Key，SDK 会回退到 AWS 标准凭证链（`~/.aws/credentials` 或环境变量 `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`）。

**Q: GPT-5.5 和 GPT-5.4 怎么选？**

A: GPT-5.5 能力最强，适合最复杂的任务；GPT-5.4 性价比更好，适合常规生产工作负载。建议先用 GPT-5.4 测试，需要更强推理能力时升级到 GPT-5.5。

**Q: 数据安全如何保障？**

A: 所有处理都在你选择的 Bedrock Region 内完成，数据不会跨区域传输。按 token 计费，无席位许可费用。

## 参考链接

- [GPT-5.5 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-55.html)
- [GPT-5.4 模型卡](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html)
- [Amazon Bedrock 定价](https://aws.amazon.com/bedrock/pricing/)
- [OpenAI on Amazon Bedrock](https://aws.amazon.com/bedrock/openai/)
- [OpenAI Codex on Amazon Bedrock](https://developers.openai.com/codex/amazon-bedrock)（在 Bedrock 上使用 Codex）
- [Bedrock API Key 管理](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html)
- [区域可用性](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html)
