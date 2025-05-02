# Dog Eye Diagnosis MCP Server

This package provides a Model Context Protocol (MCP) server for analyzing dog's eye images and returning probabilities for 10 different diseases.

## Installation

Install the package from PyPI using UV or pip:

```bash
uv pip install dog-eye-diagnosis-mcp-server
```

or

```bash
pip install dog-eye-diagnosis-mcp-server
```

## Configuration

Configure your MCP server by adding the following entry to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dog_eye_diagnosis": {
      "command": "uvx",
      "args": [
        "dog-eye-diagnosis-mcp-server"
      ]
    }
  }
}
```

## Usage

Ensure the server is properly installed and configured, then run your MCP setup or restart your application to enable the Dog Eye Diagnosis MCP server.

## License

MIT
