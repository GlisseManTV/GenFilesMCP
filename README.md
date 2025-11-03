
# GenFilesMCP 🧩

GenFilesMCP is a Model Context Protocol (MCP) server that generates PowerPoint, Excel, Word, or Markdown files from user requests and chat context. This MCP executes Python templates to produce files, uploads them to an Open Web UI (OWUI) endpoint, and stores them in the user's personal knowledge base. Additionally, it supports analyzing and reviewing existing Word documents by extracting their structure and adding comments for corrections, grammar suggestions, or idea enhancements.

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
- [Setup for Document Generation and Review Features](#setup-for-document-generation-and-review-features)
  - [Knowledge Base and Permissions](#knowledge-base-and-permissions)
- [Usage Examples](#usage-examples)
  - [Example 1: Generating a DOCX file](#example-1-generating-a-docx-file)
  - [Example 2: Reviewing a DOCX file with comments](#example-2-reviewing-a-docx-file-with-comments)
- [Star History](#star-history)

## Features

- **File Generation**: Creates files in multiple formats (PowerPoint, Excel, Word, Markdown) from user requests.
- **FastMCP Server**: Receives and processes generation requests via a FastMCP server.
- **Python Templates**: Uses customizable Python templates to generate files with specific structures.
- **OWUI Integration**: Automatically uploads generated files to Open Web UI's file API (`/api/v1/files/`).
- **Document Review**: Analyzes existing Word documents and adds structured comments for corrections, grammar suggestions, or idea enhancements.
- **Knowledge Base Integration**: Generated and reviewed documents are automatically stored in the user's personal knowledge base, allowing easy access, download, and deletion.
- **Multi-User Support**: Designed for environments with multiple users, with user-specific document collections.

## Status

This is the **first stable version (v0.2.0)** designed for multi-user environments. It includes enhanced security, user-specific knowledge base integration, and improved document management.

## Prerequisites

- **Docker** installed on your system
- **Open Web UI** instance running (v0.6.31 or later for native MCP support)
- Administrators must enable "Knowledge Access" permission in Workspace Permissions for default or group user permissions

## Installation

### Option 1: Using Pre-built Docker Image (Recommended)

Pull the pre-built Docker image from GitHub Container Registry:

```bash
docker pull ghcr.io/baronco/genfilesmcp:v0.2.0
```

Run the container:

```bash
docker run -d --restart unless-stopped -p YOUR_PORT:YOUR_PORT -e OWUI_URL="http://host.docker.internal:3000" -e PORT=YOUR_PORT --name gen_files_mcp gen_files_mcp ghcr.io/baronco/genfilesmcp:v0.2.0
```

Alternatively, use the `:latest` tag for the most recent version:

```bash
docker run -d --restart unless-stopped -p YOUR_PORT:YOUR_PORT -e OWUI_URL="http://host.docker.internal:3000" -e PORT=YOUR_PORT --name gen_files_mcp gen_files_mcp ghcr.io/baronco/genfilesmcp:latest
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
| `PORT` | Port where the MCP server will listen | `8015` |

### MCP Configuration in Open Web UI

**Important:** This version requires **Open Web UI version v0.6.31 or later** for native MCP support. MCPO is no longer supported.

Configure the MCP directly in your Open Web UI "External Tools" settings. Set the type to "MCP Streamable HTTP".



## Setup for Document Generation and Review Features

These features require additional setup in Open Web UI:

### Prerequisites

1. Create a mandatory custom tool called `chat_context` in Open Web UI to retrieve user and file metadata

### Creating the chat_context Tool

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

    # Add your custom tools using pure Python code here, make sure to add type hints and descriptions

    def chat_files(self, __files__: dict = {}) -> dict:
        """
        Get files metadata
        """
        # id and name of current files
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

    def user_data(self, __user__: dict = {}) -> str:
        """
        Get the user Email and user ID from the user object.
        """

        # Do not include a descrption for __user__ as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        user_data = {"user_id": None, "user_email": None}

        if "id" in __user__:
            user_data["user_id"] = __user__["id"]
        if "email" in __user__:
            user_data["user_email"] = __user__["email"]

        if user_data["user_id"] is None:
            user_data = {"error": "User: Unknown"}

        return user_data
```

3. Save the tool as `chat_context`

<div style="text-align: center;">

  ![File Metadata Tool](img/filestool.png)

</div>

**Note:** This tool is mandatory for the correct functioning of document generation and review features, as it provides the necessary user context (user_id) for storing documents in the user's knowledge base.

### Knowledge Base and Permissions

This version integrates with Open Web UI's knowledge base system:

- **Permission Requirement**: Administrators must enable the "Knowledge Access" permission in Workspace Permissions for default or group user permissions.
- **User Collections**: Each user will have two dedicated knowledge collections created automatically:
  - "My Generated Files": Contains all documents generated by the user.
  - "Documents Reviewed by AI": Contains all Word documents reviewed and commented on by the AI.
- **Document Management**: Users can easily review, access, download, and delete their generated or reviewed documents from their knowledge base. Deleting a document from the knowledge base also removes it from the chats where it was generated.

## System Prompt for FileGenAgent

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
