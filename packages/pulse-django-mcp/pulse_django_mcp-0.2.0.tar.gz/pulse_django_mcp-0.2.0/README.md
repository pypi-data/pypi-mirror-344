# Django-MCP

<h1 align="center">Django-MCP</h1>
<p align="center">Seamlessly integrate your Django application with the Model Context Protocol (MCP) using the official Python SDK.</p>
<div align="center">

![Django](https://img.shields.io/badge/Django-%3E%3D3.2-092E20.svg?logo=django&logoColor=white)
![Python Versions](https://img.shields.io/badge/Python-%3E%3D3.10-blue)
![MCP Version](https://img.shields.io/badge/MCP-1.6.0-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

## Overview

`django-mcp` allows you to easily expose parts of your Django application (views, functions) as **Tools**, **Resources**, and **Prompts** compatible with the [Model Context Protocol (MCP) specification (v1.6.0)](https://github.com/modelcontextprotocol/mcp-spec).

This enables AI agents and LLMs (like Gemini, Claude, etc.) that understand MCP to interact with your Django application in a standardized way.

_**Note:** This project was significantly developed with the assistance of an AI pair programmer (Gemini, Claude and Cursor Agent). While thoroughly tested, this collaborative approach shaped its implementation._

This library acts as a **thin wrapper** around the official [`mcp` Python SDK](https://github.com/modelcontextprotocol/python-sdk), providing:

-   **Simplified Setup:** An easy way to initialize and integrate the MCP server within your Django project (`FastMCP` class).
-   **Auto-Discovery:** Automatically discover Django views and register them as MCP tools.
-   **SSE Transport:** Exposes the MCP server via a Server-Sent Events (SSE) endpoint compatible with MCP clients.

## Key Features

-   **Uses Official MCP SDK:** Leverages the standard `mcp` package for core protocol logic.
-   **`FastMCP`-style API:** Provides a familiar decorator-based API (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`).
-   **Django View Auto-Discovery:** Automatically exposes Django views as MCP tools (configurable).
-   **SSE Endpoint Integration:** Easily integrates the MCP SSE transport into your Django `urls.py`.

## Installation

```bash
# Make sure you have Python 3.10+
pip install django-mcp
```

This will also install the required `mcp` SDK and Django if you don't have them.

Add `django_mcp` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_mcp',
    # ...
]
```

## Quick Start & Documentation

For detailed setup instructions, usage examples (registering tools, resources, prompts), auto-discovery configuration, and more, please refer to the detailed documentation:

➡️ **[README_MCP.md](README_MCP.md)**

## Contributing

Contributions are welcome! Please check the [contribution guidelines](CONTRIBUTING.md) (if available) or open an issue/pull request.

## License

Django-MCP is licensed under the MIT License.
