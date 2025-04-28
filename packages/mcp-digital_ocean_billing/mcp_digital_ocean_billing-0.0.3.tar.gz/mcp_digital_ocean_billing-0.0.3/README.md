# Digital Ocean Billing MCP Server

A Model Context Protocol (MCP) server for Digital Ocean Billing integration. This server provides read-only tools for interacting with Digital Ocean's Billing API, allowing you to view account balances, billing history, and invoices.

## Features

- **Account Balance**: View your current Digital Ocean account balance
- **Billing History**: Access detailed billing history and transactions
- **Invoices**: Retrieve and analyze your Digital Ocean invoices
- **Resources**: Access raw billing data for integration with other tools
- **Prompts**: Templates for common billing analysis workflows

## Installation

```bash
pip install mcp-digital_ocean_billing
```

## Configuration

This MCP server requires a Digital Ocean Personal Access Token with read access to your billing information.

### Obtaining Digital Ocean API Credentials

1. Login to your Digital Ocean account at https://cloud.digitalocean.com/
2. Navigate to API → Tokens/Keys
3. Click "Generate New Token"
4. Name your token (e.g., "MCP Billing Access")
5. Ensure "Read" scope is selected
6. Click "Generate Token"
7. Copy and securely store the generated token - it will only be shown once!

### Environment Variables

Set the following environment variables:

```bash
export DIGITAL_OCEAN_BILLING_API_KEY="your_personal_access_token"
```

Optionally, you can customize the API base URL (default is https://api.digitalocean.com/v2):

```bash
export DIGITAL_OCEAN_BILLING_BASE_URL="https://api.digitalocean.com/v2"
```

## Usage

### Starting the server directly

```bash
mcp-digital_ocean_billing
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "digital-ocean-billing": {
      "command": "uvx",
      "args": [
        "mcp-digital_ocean_billing"
      ],
      "env": {
        "DIGITAL_OCEAN_BILLING_API_KEY": "your_personal_access_token"
      }
    }
  }
}
```

Replace the environment variables with your actual Digital Ocean credentials.

### Using uvx directly

You can also run the server using `uvx` directly:

```bash
uvx mcp-digital_ocean_billing
```

With environment variables:

```bash
DIGITAL_OCEAN_BILLING_API_KEY="your_token" uvx mcp-digital_ocean_billing
```

## Available Tools

* **get_account_balance**: Get your current Digital Ocean account balance
* **get_billing_history**: View detailed billing history with pagination support
* **get_invoice_list**: List all invoices for your account
* **get_invoice_detail**: Get detailed information about a specific invoice

## Available Resources

* **digital_ocean_billing://balance**: Current account balance data
* **digital_ocean_billing://billing_history**: Complete billing history in raw JSON format
* **digital_ocean_billing://invoices**: Raw invoice data for your account

## Available Prompts

* **check_billing_summary**: Template for checking overall billing status
* **analyze_invoice**: Template for analyzing a specific invoice
* **cost_optimization**: Template for getting cost optimization recommendations

## Security Considerations

This MCP server is designed to be read-only and does not implement any methods that modify your Digital Ocean account. However, your API token does grant access to billing information, so:

1. Use a token with read-only permissions
2. Store your API token securely
3. Do not share your `claude_desktop_config.json` file with others
4. Regularly rotate your API tokens

## Version

0.0.1
