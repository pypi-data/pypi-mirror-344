# Mixpanel MCP Server

A Model Context Protocol (MCP) server for Mixpanel integration. This server provides tools for interacting with Mixpanel, including querying events, analyzing funnels, working with user profiles, and managing annotations.

## Features

- **Event Analysis**: Query and analyze Mixpanel event data
- **User Profiles**: Retrieve and examine user profile information
- **Funnels**: Analyze conversion funnels for user journeys
- **Cohorts**: Work with user cohorts
- **Annotations**: Create and manage annotations to mark important events
- **Data Export**: Export raw event data for external analysis

## Installation

```bash
pip install mcp-mixpanel
```

## Configuration

Set the following environment variables:

```bash
export MIXPANEL_API_SECRET="your_api_secret"
export MIXPANEL_PROJECT_ID="your_project_id"  # Optional
export MIXPANEL_SERVICE_ACCOUNT_USERNAME="username"  # Optional alternative auth
export MIXPANEL_SERVICE_ACCOUNT_PASSWORD="password"  # Optional alternative auth
```

## Usage

### Starting the server directly

```bash
mcp-mixpanel
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-mixpanel": {
  "command": "uvx",
  "args": [
    "mcp-mixpanel"
  ],
  "env": {
    "MIXPANEL_API_SECRET": "your_api_secret",
    "MIXPANEL_PROJECT_ID": "your_project_id"
  }
}
```

Replace the environment variables with your actual Mixpanel credentials.

## Available Tools

* **query_events**: Query Mixpanel events by name, date range, and other parameters
* **get_user_profile**: Retrieve detailed profile information for a specific user
* **create_annotation**: Create an annotation to mark important events or changes
* **get_funnel_data**: Analyze conversion data for a specific funnel
* **get_cohorts**: List all cohorts defined in your Mixpanel project
* **export_events**: Export raw event data for external analysis

## Available Resources

* **mixpanel://events**: List of all event names in your Mixpanel project
* **mixpanel://properties**: List of all event properties in your Mixpanel project
* **mixpanel://funnels**: List of all funnels in your Mixpanel project
* **mixpanel://annotations**: List of all annotations in your Mixpanel project

## Available Prompts

* **query_events**: Template for querying and analyzing event data
* **funnel_analysis**: Template for analyzing funnel performance
* **create_annotation**: Template for creating annotations for important events

## Version

0.0.1
