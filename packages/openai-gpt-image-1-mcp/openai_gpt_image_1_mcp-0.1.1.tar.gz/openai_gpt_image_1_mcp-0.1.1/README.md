# OpenAI Image Generation MCP

Model Context Protocol (MCP) server for AI assistants to generate and edit images using OpenAI's GPT-image-1 model.

## Features

- Generate images from text prompts
- Edit images with reference images and optional masks
- Save generated/edited images to local storage
- Handle errors gracefully

## Installation

Install from PyPI:

```bash
pip install openai-gpt-image-1-mcp
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)

## Usage

### Starting the MCP Server

After installation, you can start the MCP server using the following command:

```bash
openai-gpt-image-1-mcp
```

Or run it directly as a module:

```bash
python -m openai_gpt_image_1_server
```

### Configuring with Claude Desktop

To use this MCP with Claude Desktop or similar tools, add the following configuration to your `mcp_config.json` file:

#### For PyPI installation (recommended)

```json
"openai-gpt-image-1-mcp": {
  "autoApprove": [
    "generate_image",
    "edit_image"
  ],
  "disabled": false,
  "timeout": 180,
  "command": "openai-gpt-image-1-mcp",
  "env": {
    "OPENAI_API_KEY": "your_openai_api_key_here"
  },
  "transportType": "stdio"
}
```

#### For UV package manager

```json
"openai-gpt-image-1-mcp": {
  "autoApprove": [
    "generate_image",
    "edit_image"
  ],
  "disabled": false,
  "timeout": 180,
  "command": "uv",
  "args": [
    "run",
    "openai-gpt-image-1-mcp"
  ],
  "env": {
    "OPENAI_API_KEY": "your_openai_api_key_here"
  },
  "transportType": "stdio"
}
```

#### For direct execution (without PyPI)

If you cloned the repository and want to run it directly:

```json
"openai-gpt-image-1-mcp": {
  "autoApprove": [
    "generate_image",
    "edit_image"
  ],
  "disabled": false,
  "timeout": 180,
  "command": "python",
  "args": [
    "/absolute/path/to/your/cloned/repo/openai_gpt_image_1_mcp/openai_gpt_image_1_server/__init__.py"
  ],
  "env": {
    "OPENAI_API_KEY": "your_openai_api_key_here"
  },
  "transportType": "stdio"
}
```

**Configuration parameters explained:**

- `autoApprove`: List of tool methods that can be called without user confirmation
- `disabled`: Set to `true` to disable this MCP
- `timeout`: Maximum time (in seconds) allowed for image generation operations
- `command` & `args`: The command to start the MCP server
- `env`: Environment variables needed by the MCP (requires your OpenAI API key)
- `transportType`: Communication protocol used (keep as "stdio")

### API Tools

#### generate_image

Generate an image from a text prompt.

Parameters:
- `prompt` (string, required): Text description of the desired image
- `model` (string, optional): Model to use, default is "gpt-image-1"
- `n` (integer, optional): Number of images to generate, default is 1
- `size` (string, optional): Image dimensions, options: "1024x1024", "1536x1024", "1024x1536", "auto"
- `quality` (string, optional): Rendering quality, options: "low", "medium", "high", "auto"
- `user` (string, optional): Unique identifier for the end-user
- `save_filename` (string, optional): Custom filename without extension

Returns:
- Success: `{"status": "success", "saved_path": "/path/to/image.png"}`
- Error: `{"status": "error", "message": "Error details"}`

#### edit_image

Edit an image or create variations based on reference images and an optional mask.

Parameters:
- `prompt` (string, required): Text description of the desired final image
- `image_paths` (array of strings, required): List of paths to input images
- `mask_path` (string, optional): Path to mask image for inpainting
- `model` (string, optional): Model to use, default is "gpt-image-1"
- `n` (integer, optional): Number of images to generate, default is 1
- `size` (string, optional): Image dimensions, options: "1024x1024", "1536x1024", "1024x1536", "auto"
- `quality` (string, optional): Rendering quality, options: "low", "medium", "high", "auto"
- `user` (string, optional): Unique identifier for the end-user
- `save_filename` (string, optional): Custom filename without extension

Returns:
- Success: `{"status": "success", "saved_path": "/path/to/image.png"}`
- Error: `{"status": "error", "message": "Error details"}`

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.