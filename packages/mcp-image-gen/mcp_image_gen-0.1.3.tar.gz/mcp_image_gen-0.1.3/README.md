# OpenAI图像生成MCP服务 (v0.1.3)

这是一个基于MCP协议的OpenAI图像生成服务器，允许大语言模型通过MCP协议调用OpenAI的图像生成API，生成图像后自动上传到图床并返回图片链接。

## 安装

```bash
pip install mcp-image-gen
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
      "args": ["mcp-image-gen"]
    }
  }
}
```

## 本地运行

安装后，您可以在本地通过以下方式运行：

```bash
# 使用uvx
uvx mcp-image-gen

# 使用包提供的命令
mcp-image-gen

# 使用Python -m
python -m mcp_image_gen
```

按 `Ctrl+C` 停止服务器。

## 配置

默认情况下，服务器使用内置的API密钥、代理URL和图床配置，但您可以在调用工具时通过参数覆盖它们。这使得大语言模型可以灵活地传入自定义凭证和配置。

### 错误处理

服务器会将所有错误信息返回给调用方，格式为 `"Error: 具体错误信息"`，方便大语言模型理解错误原因并做出相应处理。

## 图床功能

本服务使用 `tu.my` 图床服务来托管生成的图像，确保图像生成后能够立即获得可访问的URL。

## 许可证

MIT License 