# Notion MCP Server

A Model Context Protocol (MCP) server for Notion integration. This server provides tools for interacting with Notion, including querying pages, databases, and blocks.

## Features

- **Page Management**: Get, create, and update Notion pages
- **Database Operations**: Query, filter, and sort Notion databases
- **Block Operations**: Get and append blocks to pages
- **Search**: Query for Notion content
- **Resources**: Access metadata about Notion objects
- **Prompts**: Templates for common Notion workflows

## Installation

```bash
pip install mcp-notion
```

## Configuration

Set the following environment variables:

```bash
export NOTION_API_KEY="your_notion_integration_token"
export NOTION_VERSION="2022-06-28"  # Optional, will use default if not specified
```

You can get your Notion API key by creating an integration at https://www.notion.so/my-integrations

## Usage

### Starting the server directly

```bash
mcp-notion
```

### Using with uvx

```bash
uvx mcp-notion
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-notion": {
  "command": "uvx",
  "args": [
    "mcp-notion"
  ],
  "env": {
    "NOTION_API_KEY": "your_notion_integration_token",
    "NOTION_VERSION": "2022-06-28"
  }
}
```

Replace the environment variables with your actual Notion credentials.

## Available Tools

* **search_notion**: Search Notion content with optional filters
* **get_page**: Get details of a specific Notion page
* **get_block_children**: Get children blocks of a block or page
* **get_database**: Get details of a specific Notion database
* **query_database**: Query a Notion database with optional filters and sorting
* **create_page**: Create a new page in a database or as a child of another page
* **update_page**: Update properties of an existing Notion page
* **append_blocks**: Append new blocks to an existing block or page

## Available Resources

* **notion://search**: Search all Notion content
* **notion://databases**: List of all Notion databases the user has access to
* **notion://users**: List of all users in the workspace

## Available Prompts

* **create_database_entry**: Template for creating a new entry in a database
* **search_and_summarize**: Template for searching and summarizing Notion content
* **database_query_builder**: Template for building Notion database queries

## Notes on Authentication

1. You need to create a Notion integration at https://www.notion.so/my-integrations
2. You must share specific pages/databases with your integration
3. Make sure your integration has the appropriate capabilities (Read, Update, etc.)

## Version

0.0.1
