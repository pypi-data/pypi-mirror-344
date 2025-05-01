# OpenAI图像生成MCP服务gpt-image-1模型 (v0.1.4)

这是一个基于MCP协议的OpenAI图像生成服务器，允许大语言模型通过MCP协议调用OpenAI的图像生成API，生成图像后自动上传到图床并返回图片链接。

## 安装

```bash
pip install gpt-image-1
```

## 功能

### 工具 (Tools)

- `generate_image`: 根据文本提示生成图像，自动上传到图床，返回图片URL。
  - 参数:
    - `prompt`: 描述想要生成的图像的文本提示
    - `size`: 图像尺寸，可选 `1024x1024`(默认), `1024x1536`, `1536x1024`
    - `quality`: 图像质量，可选 `low`, `medium`(默认), `high`, `auto`
    - `model`: 使用的模型，默认为 `gpt-image-1`
    - `save_locally`: 是否同时保存图像到本地文件，默认为`False`
    - `api_key`: 可选，自定义API密钥，不提供则使用默认值
    - `base_url`: 可选，自定义API基础URL，不提供则使用默认值
    - `image_hosting_token`: 可选，自定义图床API令牌，不提供则使用默认值
    - `image_hosting_url`: 可选，自定义图床API URL，不提供则使用默认值

- `save_image_base64`: 将Base64编码的图像数据保存为文件。
  - 参数:
    - `base64_data`: Base64编码的图像数据
    - `filename`: 要保存的文件名，默认为 `generated_image.png`

- `upload_to_image_hosting`: 将Base64编码的图像数据上传到图床。
  - 参数:
    - `base64_data`: Base64编码的图像数据
    - `filename`: 上传的文件名，默认为 `generated_image.png`
    - `permission`: 图片权限，1=公开，0=私有，默认为1
    - `image_hosting_token`: 可选，自定义图床API令牌，不提供则使用默认值
    - `image_hosting_url`: 可选，自定义图床API URL，不提供则使用默认值

### 资源 (Resources)

- `openai://api/status`: 检查OpenAI API的可用性状态。

## 在阿里云百炼中使用

在阿里云百炼平台的MCP服务配置中，使用以下JSON：

```json
{
  "mcpServers": {
    "openai-image-gen": {  // 服务名称，可自定义
      "command": "uvx",
      "args": ["gpt-image-1"],
      "env": {
        "API_KEY": "你的OpenAI API密钥",
        "API_BASE_URL": "https://api.ssopen.top",
        "IMAGE_HOSTING_TOKEN": "你的图床Token",
        "IMAGE_HOSTING_URL": "https://tu.my/api/v1/upload",
        "DISABLE_LOCAL_SAVE": "true"
      }
    }
  }
}
```

## 环境变量配置

服务支持通过环境变量进行配置：

| 环境变量 | 说明 | 默认值 |
|---------|------|-------|
| `API_KEY` | OpenAI API密钥 | 内置默认值 |
| `API_BASE_URL` | API基础URL | `https://api.ssopen.top` |
| `IMAGE_HOSTING_TOKEN` | 图床访问令牌 | 内置默认值 |
| `IMAGE_HOSTING_URL` | 图床上传接口URL | `https://tu.my/api/v1/upload` |
| `DISABLE_LOCAL_SAVE` | 是否禁用本地保存 | `false` |

## 获取API密钥

如果您没有API密钥，可以访问 [https://api.ssopen.top](https://api.ssopen.top) 申请获取。该服务提供OpenAI API的代理访问，支持各种OpenAI模型，包括图像生成模型。

## 本地运行

安装后，您可以在本地通过以下方式运行：

```bash
# 使用uvx
uvx gpt-image-1

# 使用包提供的命令
gpt-image-1

# 使用Python -m
python -m mcp_image_gen
```

按 `Ctrl+C` 停止服务器。

## 配置

默认情况下，服务器使用内置的API密钥、代理URL和图床配置，但您可以：
1. 通过环境变量设置全局默认值
2. 在调用各工具时通过参数覆盖默认值

这使得大语言模型可以灵活地传入自定义凭证和配置。

### 错误处理

服务器会将所有错误信息返回给调用方，格式为 `"Error: 具体错误信息"`，方便大语言模型理解错误原因并做出相应处理。

## 图床功能

本服务使用 `tu.my` 图床服务来托管生成的图像，确保图像生成后能够立即获得可访问的URL。

## 许可证

MIT License 