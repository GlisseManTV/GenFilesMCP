
# GenFilesMCP 🧩

GenFilesMCP is a Model Context Protocol (MCP) server that generates PowerPoint, Excel, Word, or Markdown files from user requests and chat context. This MCP executes Python templates to produce files and uploads them to an Open Web UI (OWUI) endpoint. Additionally, it supports analyzing and reviewing existing Word documents by extracting their structure and adding comments for corrections, grammar suggestions, or idea enhancements.

## Table of Contents

- [Features](#features)
- [Status](#status)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Option 1: Using Pre-built Docker Image (Recommended)](#option-1-using-pre-built-docker-image-recommended)
  - [Option 2: Building from Source](#option-2-building-from-source)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [MCP Configuration in Open Web UI](#mcp-configuration-in-open-web-ui)
  - [Getting Your JWT Token](#getting-your-jwt-token)
- [Setup for Document Review Feature](#setup-for-document-review-feature)
- [Usage Examples](#usage-examples)
  - [Example 1: Generating a DOCX file](#example-1-generating-a-docx-file)
  - [Example 2: Reviewing a DOCX file with comments](#example-2-reviewing-a-docx-file-with-comments)
- [Star History](#star-history)

## Features

- **File Generation**: Creates files in multiple formats (PowerPoint, Excel, Word, Markdown) from user requests.
- **FastMCP Server**: Receives and processes generation requests via a FastMCP server.
- **Python Templates**: Uses customizable Python templates to generate files with specific structures.
- **OWUI Integration**: Automatically uploads generated files to Open Web UI's file API (`/api/v1/files/`).
- **Document Review (Experimental)**: Analyzes existing Word documents and adds structured comments for corrections, grammar suggestions, or idea enhancements.

## Status

This is a **Minimal Viable Product (MVP)**. It works for generating and uploading files but still needs improvements in:
- Security and input sanitization
- Template validation
- Logging and error handling

**Use with caution**: This MCP executes code and should be run in a controlled environment (Docker recommended). Avoid exposing it on public networks.

## Prerequisites

- **Docker** installed on your system
- **Open Web UI** instance running (v0.6.31 or later recommended for native MCP support)
- **JWT Token** from your Open Web UI admin settings

## Installation

### Option 1: Using Pre-built Docker Image (Recommended)

Pull the pre-built Docker image from GitHub Container Registry:

```bash
docker pull ghcr.io/baronco/genfilesmcp:v0.1.0
```

Run the container:

```bash
docker run -d --restart unless-stopped -p YOUR_PORT:YOUR_PORT -e OWUI_URL="http://host.docker.internal:3000" -e JWT_SECRET="YOUR_JWT_SECRET" -e PORT=YOUR_PORT --name gen_files_mcp gen_files_mcp ghcr.io/baronco/genfilesmcp:v0.1.0
```

Alternatively, use the `:latest` tag for the most recent version:

```bash
docker run -d --restart unless-stopped -p YOUR_PORT:YOUR_PORT -e OWUI_URL="http://host.docker.internal:3000" -e JWT_SECRET="YOUR_JWT_SECRET" -e PORT=YOUR_PORT --name gen_files_mcp gen_files_mcp ghcr.io/baronco/genfilesmcp:latest
```

### Option 2: Building from Source

If you need to build the image yourself:

1. Clone the repository:

```bash
git clone https://github.com/Baronco/GenFilesMCP.git
cd GenFilesMCP
```

2. Build the Docker image:

```bash
docker build -t genfilesmcp .
```

3. Run the container:

```bash
docker run -d --restart unless-stopped \
  -p YOUR_PORT:YOUR_PORT \
  -e OWUI_URL="http://host.docker.internal:3000" \
  -e JWT_SECRET="YOUR_JWT_SECRET" \
  -e PORT=YOUR_PORT \
  --name gen_files_mcp \
  genfilesmcp
```

## Configuration

### Environment Variables

The MCP server requires the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `OWUI_URL` | URL of your Open Web UI instance | `http://host.docker.internal:3000` |
| `JWT_SECRET` | JWT token from OWUI for authentication | See [Getting Your JWT Token](#getting-your-jwt-token) |
| `PORT` | Port where the MCP server will listen | `8015` |

### MCP Configuration in Open Web UI

**Important:** From **Open Web UI version v0.6.31** onwards, the platform natively supports `http streamable` type MCPs. This means you **do not need MCPO** to use this server.

**For Open Web UI v0.6.31+:**
Configure the MCP directly in your Open Web UI "External Tools" settings. Change the type “OpenApi” to “MCP Streamable HTTP”

**For earlier versions or if using MCPO:**
Add this configuration to your MCPO config file:

```json
{
  "mcpServers": {
    "GenFilesMCP": {
      "type": "streamable_http",
      "url": "http://host.docker.internal:YOUR_PORT/mcp/"
    }
  }
}
```

Replace `YOUR_PORT` with the port you configured (e.g., `8015`).

### Getting Your JWT Token

The JWT token can be found in your Open Web UI Admin settings:
1. Go to **Admin Panel**
2. Navigate to **Settings**
3. Open the **Account** module
4. Copy your JWT token

## Setup for Document Review Feature

The document review feature is **experimental** and requires additional setup:

### Prerequisites
1. Upload a `.docx` file to your Open Web UI chat context
2. Create a custom tool in Open Web UI to retrieve file metadata

### Creating the File Metadata Tool

1. In Open Web UI, go to **Workspace > Tools > (+) Create**
2. Paste the following code:

```python
import os
import requests
from datetime import datetime
from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        pass

    def get_files_metadata(self, __files__: dict = {}) -> dict:
        """
        Get files metadata
        """
        chat_current_files = {"files": []}

        if __files__ is not None:
            for f in __files__:
                chat_current_files["files"].append({"id": f["id"], "name": f["name"]})
            return chat_current_files
        else:
            message = {
                "message": "There are no documents uploaded in the current chat."
            }
            return message
```

3. Save the tool

<div style="text-align: center;">

  ![File Metadata Tool](img/filestool.png)

</div>

### System Prompt for FileGenAgent

For optimal results, create a custom agent in Open Web UI:
1. Copy the system prompt from `example/systemprompt.md`
2. Create a new agent called **FileGenAgent**
3. Use this system prompt for the agent
4. Tested successfully with **GPT-5 Thinking mini**

## Usage Examples

### Example 1: Generating a DOCX file

<div style="text-align: center;">

  ![Generating DOCX Example](img/example2.png)

</div>

> **Example files**: You can find the prompt and generated result in the `example` folder: `History_of_Neural_Nets_Summary_69d1751b-577b-4329-beca-ac16db7acdbd.docx`

> This file was generated using the GenFiles MCP server and GPT-5 mini

### Example 2: Reviewing a DOCX file with comments

The review feature allows the agent to analyze uploaded documents and add structured comments for improvements.

<div style="text-align: center;">

  ![Review Example 1](img/reviewer1.png)

</div>

<div style="text-align: center;">

  ![Review Example 2](img/reviewer2.png)

</div>

<div style="text-align: center;">

  ![Review Example 3](img/reviewer3.png)

</div>

**Workflow:**
1. User uploads `History_of_Neural_Nets_Summary.docx` to the chat
2. User requests a review with comments for corrections, grammar suggestions, and idea enhancements
3. Agent calls the `get_files_metadata` custom tool to retrieve file ID and name
4. Agent uses the `full_context_docx` MCP function to analyze the document structure
5. Agent calls the `review_docx` MCP function to add comments to specific elements

**Result:**

<div style="text-align: center;">

  ![DOCX Comments](img/docxcomments.png)

</div>

> **Example files**: Find the reviewed document in the `example` folder: `History_of_Neural_Nets_Summary_reviewed_a35adcc5-e338-47c6-a0b0-2c21602b0777.docx`

> Generated using the GenFiles MCP server and GPT-5 mini

> The review functionality preserves the original formatting while adding structured comments

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Baronco/GenFilesMCP&type=date&legend=top-left)](https://www.star-history.com/#Baronco/GenFilesMCP&type=date&legend=top-left)
