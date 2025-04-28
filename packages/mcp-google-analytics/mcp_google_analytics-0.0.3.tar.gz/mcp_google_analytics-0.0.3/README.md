# Google Analytics MCP Server

A Model Context Protocol (MCP) server for Google Analytics integration. This server provides tools for interacting with Google Analytics, including running reports, querying accounts and properties, and accessing metadata.

## Features

- **Run Reports**: Get analytics data with specified metrics and dimensions
- **Account Management**: List accounts and properties
- **Metadata Access**: Get information about available metrics and dimensions
- **Resources**: Access Google Analytics accounts, properties, and metadata
- **Prompts**: Templates for common Google Analytics workflows

## Installation

```bash
pip install mcp-google-analytics
```

## Configuration

Set the following environment variables:

```bash
export GOOGLE_ANALYTICS_CLIENT_ID="your_client_id"
export GOOGLE_ANALYTICS_CLIENT_SECRET="your_client_secret"
export GOOGLE_ANALYTICS_REFRESH_TOKEN="your_refresh_token"
export GOOGLE_ANALYTICS_PROPERTY_ID="your_property_id"
```

### OAuth Setup

To get the required OAuth credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Analytics Data API and Google Analytics Admin API
4. Create OAuth 2.0 credentials
5. Use the OAuth 2.0 Playground to get a refresh token:
   - Go to https://developers.google.com/oauthplayground/
   - Configure the OAuth 2.0 Playground to use your client ID and secret
   - Select the required Google Analytics scopes
   - Click "Authorize APIs"
   - Exchange the authorization code for tokens
   - Save the refresh token

## Usage

### Starting the server directly

```bash
mcp-google-analytics
```

### Using with Claude Desktop

Add the following to your claude_desktop_config.json file:

```json
"mcp-google-analytics": {
  "command": "uvx",
  "args": [
    "mcp-google-analytics"
  ],
  "env": {
    "GOOGLE_ANALYTICS_CLIENT_ID": "your_client_id",
    "GOOGLE_ANALYTICS_CLIENT_SECRET": "your_client_secret",
    "GOOGLE_ANALYTICS_REFRESH_TOKEN": "your_refresh_token",
    "GOOGLE_ANALYTICS_PROPERTY_ID": "your_property_id"
  }
}
```

Replace the environment variables with your actual Google Analytics credentials.

## Available Tools

* **run_report**: Run a basic report with specified metrics and dimensions
* **get_accounts**: List all Google Analytics accounts
* **get_properties**: List all properties within an account
* **get_metadata**: Get metadata about available metrics and dimensions

## Available Resources

* **google_analytics://accounts**: List of all accounts
* **google_analytics://properties/{account_id}**: List properties for a specific account
* **google_analytics://metadata**: Metadata about available metrics and dimensions

## Available Prompts

* **create_basic_report**: Template for creating a basic report
* **analyze_traffic_sources**: Template for analyzing traffic sources
* **track_conversions**: Template for tracking conversions

## Version

0.0.1
