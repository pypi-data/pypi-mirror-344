# InVideo AI MCP Server

![Invideo AI Logo](invideo-ai.svg)

The InVideo AI MCP server enables any MCP Client like Claude Desktop or Agents to use the InVideo AI API to generate AI videos.

**License**: MIT

**Note**: This project is in early development. While we welcome community feedback and contributions, please be aware that official support is limited.

## Installation

### Prerequisites

- Python 3.13 or higher

### Installing uv

`uv` is a fast Python package installer and resolver that we recommend for installing this package.

**macOS or Linux**:

```bash
# Install with the official installer script
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew (macOS)
brew install uv
```

**Windows**:

```powershell
# Install with the official installer script in PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Or via Scoop
scoop install uv
```

For other installation methods, see the [uv documentation](https://github.com/astral-sh/uv).

## Usage

### Quickstart with Claude Desktop

1. Install uv package manager (see Installing uv section above).
2. Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```json
{
  "mcpServers": {
    "InVideoAI": {
      "command": "uvx",
      "args": ["invideo-ai-mcp"]
    }
  }
}
```

If you're using Windows, you'll need to enable "Developer Mode" in Claude Desktop to use the MCP server. Click "Help" in the hamburger menu at the top left and select "Enable Developer Mode".

## Available MCP Tools

The server provides the following tools to Claude:

- **generate_content_ideas**: Generate content ideas for a specific platform with topic, vibe, and target audience suggestions.
- **generate_script**: Generate a video script based on topic, vibe, and target audience.
- **generate_video_from_script**: Generate a video using a script and additional context (topic, vibe, target audience).

## Roadmap

- [ ] Video editing capabilities
