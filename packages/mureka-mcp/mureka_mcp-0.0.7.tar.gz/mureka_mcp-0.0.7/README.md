

<div class="title-block" style="text-align: center;" align="center">

![export](mureka_mcp.svg)

[![Discord Community](discord_mureka.svg)](https://discord.com/invite/nwu9ANqAf5)
[![Twitter](x_mureka.svg)](https://x.com/Mureka_AI)
[![PyPI](pypi_mureka.svg)](https://pypi.org/project/mureka-mcp)

</div>
<p align="center">
  Official Mureka Model Context Protocol (MCP) server that enables interaction with powerful lyrics, song and bgm generating APIs. This server allows MCP clients like <a href="https://www.anthropic.com/claude">Claude Desktop</a>, <a href="https://github.com/openai/openai-agents-python">OpenAI Agents</a> and others to generate lyrics, song and background music(instrumental).
</p>

## Quickstart with Claude Desktop

1. Get your API key from [Mureka](https://platform.mureka.ai/apiKeys).
2. Install `uv` (Python package manager), install with `curl -LsSf https://astral.sh/uv/install.sh | sh` or see the `uv` [repo](https://github.com/astral-sh/uv) for additional install methods.
3. Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```
{
    "mcpServers": {
        "Mureka": {
            "command": "uvx",
            "args": [
                "mureka-mcp"
            ],
            "env": {
                "MUREKA_API_KEY": "<insert-your-api-key-here>",
                "MUREKA_API_URL": "https://api.mureka.ai",
                "TIME_OUT_SECONDS":"300"
            }
        }
    }
}
```

Then restart the Claude app and see 4 MCP tools available in the window, indicating successful loading
<div class="title-block" style="text-align: center;" align="center">

![img.png](img.png)

</div>
## Optional features
You can add the `TIME_OUT_SECONDS` environment variable to the `claude_desktop_config.json` to set the timeout period for song or bgm generation waiting(Default 60s).

## Troubleshooting

Logs when running with Claude Desktop can be found at:

- **Windows**: `%APPDATA%\Claude\logs\mcp-server-Mureka.log`
- **macOS**: `~/Library/Logs/Claude/mcp-server-Mureka.log`
