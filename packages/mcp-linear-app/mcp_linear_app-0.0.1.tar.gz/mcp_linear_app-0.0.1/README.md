# Linear MCP Server

A Model Context Protocol (MCP) server for Linear integration. This server provides tools for interacting with Linear, including managing issues, teams, projects, and more.

## Features

- **Issue Management**: Create, read, update, and search issues
- **Team Management**: List teams and their states
- **Project Management**: List projects and their details
- **Resources**: Access metadata about Linear objects
- **Prompts**: Templates for common Linear workflows

## Installation

```bash
pip install mcp-linear
```

## Configuration

Set the following environment variable:

```bash
export LINEAR_API_KEY="your_api_token"
```

You can optionally set the base URL if you need to use a different endpoint:

```bash
export LINEAR_BASE_URL="https://api.linear.app/graphql"
```

## Usage

### Starting the server directly

```bash
mcp-linear
```

### Using with uvx

```bash
uvx mcp-linear
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-linear": {
  "command": "uvx",
  "args": [
    "mcp-linear"
  ],
  "env": {
    "LINEAR_API_KEY": "your_api_token"
  }
}
```

Replace the environment variables with your actual Linear credentials.

## Available Tools

* **get_issue**: Get details of a specific Linear issue
* **create_issue**: Create a new issue in Linear
* **update_issue**: Update an existing issue in Linear
* **add_comment**: Add a comment to an issue in Linear
* **search_issues**: Search for issues in Linear
* **list_teams**: List all teams in Linear
* **list_projects**: List projects in Linear
* **list_issue_states**: List all issue states for a team in Linear

## Available Resources

* **linear://issues**: List of all issues in Linear
* **linear://teams**: List of all teams in Linear
* **linear://projects**: List of all projects in Linear
* **linear://user**: Information about the authenticated user

## Available Prompts

* **create_issue_prompt**: Template for creating a new issue
* **search_issues_prompt**: Template for searching issues
* **update_issue_prompt**: Template for updating an issue

## Version

0.0.1
