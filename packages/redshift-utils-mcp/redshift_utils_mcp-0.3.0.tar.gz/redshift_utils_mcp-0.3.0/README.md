# Redshift Admin MCP Server

![Redshift Admin MCP Server Banner](docs/banner.png)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This project implements a Model Context Protocol (MCP) server designed specifically to interact with Amazon Redshift databases.

It bridges the gap between Large Language Models (LLMs) or AI assistants (like those in Claude, Cursor, or custom applications) and your Redshift data warehouse, enabling secure, standardized data access and interaction. This allows users to query data, understand database structure, and monitoring/diagnostic operations using natural language or AI-driven prompts.

This server is for developers, data analysts, or teams looking to integrate LLM capabilities directly with their Amazon Redshift data environment in a structured and secure manner.

## Table of Contents

- [Redshift Admin MCP Server](#redshift-admin-mcp-server)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage / Quickstart](#usage--quickstart)
  - [MCP Integration](#mcp-integration)
    - [Available MCP Resources](#available-mcp-resources)
    - [Available MCP Tools](#available-mcp-tools)
  - [Development](#development)
  - [TO DO](#to-do)
  - [Contributing](#contributing)
  - [License](#license)
  - [References](#references)

## Features

*   ✨ **Secure Redshift Connection (via Data API):** Connects to your Amazon Redshift cluster using the AWS Redshift Data API via Boto3, leveraging AWS Secrets Manager for credentials managed securely via environment variables.
*   🔍 **Schema Discovery:** Exposes MCP resources for listing schemas and tables within a specified schema.
*   📊 **Metadata & Statistics:** Provides a tool (`handle_inspect_table`) to gather detailed table metadata, statistics (like size, row counts, skew, stats staleness), and maintenance status.
*   📝 **Read-Only Query Execution:** Offers a secure MCP tool (`handle_execute_ad_hoc_query`) to execute arbitrary SELECT queries against the Redshift database, enabling data retrieval based on LLM requests.
*   📈 **Query Performance Analysis:** Includes a tool (`handle_diagnose_query_performance`) to retrieve and analyze the execution plan, metrics, and historical data for a specific query ID.
*   🔍 **Table Inspection:** Provides a tool (`handle_inspect_table`) to perform a comprehensive inspection of a table, including design, storage, health, and usage.
*   🩺 **Cluster Health Check:** Offers a tool (`handle_check_cluster_health`) to perform a basic or full health assessment of the cluster using various diagnostic queries.
*   🔒 **Lock Diagnosis:** Provides a tool (`handle_diagnose_locks`) to identify and report on current lock contention and blocking sessions.
*   📊 **Workload Monitoring:** Includes a tool (`handle_monitor_workload`) to analyze cluster workload patterns over a time window, covering WLM, top queries, and resource usage.
*   📝 **DDL Retrieval:** Offers a tool (`handle_get_table_definition`) to retrieve the `SHOW TABLE` output (DDL) for a specified table.
*   🛡️ **Input Sanitization:** Utilizes parameterized queries via the Boto3 Redshift Data API client where applicable to mitigate SQL injection risks.
*   🧩 **Standardized MCP Interface:** Adheres to the Model Context Protocol specification for seamless integration with compatible clients (e.g., Claude Desktop, Cursor IDE, custom applications).

## Prerequisites

Clearly list all requirements needed before a user can install and run the server. This prevents setup failures and frustration.

Software:

*   Python 3.8+
*   `uv` (recommended package manager)
*   Git (for cloning the repository)

Infrastructure & Access:

*   Access to an Amazon Redshift cluster.
*   An AWS account with permissions to use the Redshift Data API (`redshift-data:*`) and access the specified Secrets Manager secret (`secretsmanager:GetSecretValue`).
*   A Redshift user account whose credentials are stored in AWS Secrets Manager. This user needs the necessary permissions within Redshift to perform the actions enabled by this server (e.g., `CONNECT` to the database, `SELECT` on target tables, `SELECT` on relevant system views like `pg_class`, `pg_namespace`, `svv_all_schemas`, `svv_tables`, `svv_table_info``). Using a role with the principle of least privilege is strongly recommended. See [Security Considerations](#security-considerations).

Credentials:

Your Redshift connection details are managed via AWS Secrets Manager, and the server connects using the Redshift Data API. You need:

*   The Redshift cluster identifier.
*   The database name within the cluster.
*   The ARN of the AWS Secrets Manager secret containing the database credentials (username and password).
*   The AWS region where the cluster and secret reside.
*   Optionally, an AWS profile name if not using default credentials/region.

These details will be configured via environment variables as detailed in the [Configuration](#configuration) section.

## Installation

Provide clear, simple, step-by-step instructions for installation. Prioritize the easiest method for end-users if multiple options exist.

Option 1: From Source

1.  Clone the repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
    cd YOUR_REPO
    ```

2.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```


## Configuration

Explain how to configure the server, focusing on the required Redshift connection details. Using environment variables is the standard and recommended approach for sensitive data like credentials.

Set Environment Variables:
This server requires the following environment variables to connect to your Redshift cluster via the AWS Data API. You can set these directly in your shell, using a systemd service file, a Docker environment file, or by creating a `.env` file in the project's root directory (if using a tool like `uv` or `python-dotenv` that supports loading from `.env`).

Example using shell export:
```bash
export REDSHIFT_CLUSTER_ID="your-cluster-id"
export REDSHIFT_DATABASE="your_database_name"
export REDSHIFT_SECRET_ARN="arn:aws:secretsmanager:us-east-1:123456789012:secret:your-redshift-secret-XXXXXX"
export AWS_REGION="us-east-1" # Or AWS_DEFAULT_REGION
# export AWS_PROFILE="your-aws-profile-name" # Optional
```

Example `.env` file (see `.env.example`):
```dotenv
# .env file for Redshift MCP Server configuration
# Ensure this file is NOT committed to version control if it contains secrets. Add it to .gitignore.

REDSHIFT_CLUSTER_ID="your-cluster-id"
REDSHIFT_DATABASE="your_database_name"
REDSHIFT_SECRET_ARN="arn:aws:secretsmanager:us-east-1:123456789012:secret:your-redshift-secret-XXXXXX"
AWS_REGION="us-east-1" # Or AWS_DEFAULT_REGION
# AWS_PROFILE="your-aws-profile-name" # Optional
```

Required Variables Table:

| Variable Name         | Required | Description                                                      | Example Value                                                          |
| :-------------------- | :------- | :--------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `REDSHIFT_CLUSTER_ID` | Yes      | Your Redshift cluster identifier.                                | `my-redshift-cluster`                                                  |
| `REDSHIFT_DATABASE`   | Yes      | The name of the database to connect to.                          | `mydatabase`                                                           |
| `REDSHIFT_SECRET_ARN` | Yes      | AWS Secrets Manager ARN for Redshift credentials.                | `arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret-abcdef` |
| `AWS_REGION`          | Yes      | AWS region for Data API and Secrets Manager.                     | `us-east-1`                                                            |
| `AWS_DEFAULT_REGION`  | No       | Alternative to `AWS_REGION` for specifying the AWS region.       | `us-west-2`                                                            |
| `AWS_PROFILE`         | No       | AWS profile name to use from your credentials file (~/.aws/...). | `my-redshift-profile`                                                  |

*Note: Ensure the AWS credentials used by Boto3 (via environment, profile, or IAM role) have permissions to access the specified `REDSHIFT_SECRET_ARN` and use the Redshift Data API (`redshift-data:*`).*

## Usage / Quickstart

Provide the command(s) needed to start the server after installation and configuration. Include expected output or a simple test to verify it's running correctly.

Starting the Server:

If installed from source:
```bash
# Ensure environment variables are set or .env file is present and loaded by your shell/uv
python -m redshift_utils_mcp
# Or using uv:
# uv run python -m redshift_utils_mcp
```

Verification:
Upon successful startup, you should see log messages indicating the server is running and validating configuration. If configuration is valid, it will indicate it's ready. Example (actual output will vary):

```
INFO: Configuring Redshift Admin MCP Server...
INFO: Using Cluster ID from argument/env: your-cluster-id
INFO: Using Database from argument/env: your_database_name
INFO: Using Secret ARN from argument/env: arn:aws:secretsmanager:...
INFO: Using AWS Region from argument/env: us-east-1
INFO: Configuration loaded. Starting MCP server...
INFO: Validating Redshift Data API configuration...
INFO: Configuration validated successfully.
INFO: Redshift Utils MCP Server shutting down. # This message appears after validation in lifespan
INFO: MCP server finished. # This appears after the lifespan context exits in __main__
```
*(Note: The lifespan check runs and exits before the server fully starts listening for stdio connections in the current structure, but it validates the config)*

The server runs via standard input/output (stdio) and is designed to be launched by an MCP client.

## MCP Integration

Explain how users can connect this server to their MCP-compatible clients (like Claude Desktop, Cursor IDE, or custom applications). Providing ready-to-use configuration snippets is highly beneficial.

Connecting with Claude Desktop / Anthropic Console:
Add the following configuration block to your `claude_desktop_config.json` file (you can typically find this file in the application support directory for Claude). Adjust `command`, `args`, `env`, and `workingDirectory` based on your installation method and setup.

```json
{
  "mcpServers": {
    "redshift-utils-mcp": {
      "command": "uvx",
      "args": ["run", "redshift_utils_mcp"],
      "env": {
        "REDSHIFT_CLUSTER_ID":"your-cluster-id",
        "REDSHIFT_DATABASE":"your_database_name",
        "REDSHIFT_SECRET_ARN":"arn:aws:secretsmanager:...",
        "AWS_REGION": "us-east-1"
      }
  }
}
```

Connecting with Cursor IDE:
1.  Start the MCP server locally using the instructions in the [Usage / Quickstart](#usage--quickstart) section.
2.  In Cursor, open the Command Palette (Cmd/Ctrl + Shift + P).
3.  Type "Connect to MCP Server" or navigate to the MCP settings.
4.  Add a new server connection.
5.  Choose the `stdio` transport type.
6.  Enter the command and arguments required to start your server (`uvx run redshift_utils_mcp`). Ensure any necessary environment variables are available to the command being run.
7.  Cursor should detect the server and its available tools/resources.

Connecting with Custom Clients (using MCP SDKs):
If you are building your own MCP client application using an official SDK (like `@modelcontextprotocol/sdk` for TypeScript/JavaScript or `mcp` for Python), you will typically connect using the `StdioClientTransport` (or equivalent) by pointing it to the command that starts this server.

Example (Conceptual TypeScript):
```typescript
import { McpClient } from "@modelcontextprotocol/sdk/client";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio";

const transport = new StdioClientTransport({
  command: "python",
  args: ["-m", "redshift_utils_mcp"],
  // env: {... } // Optional environment variables
});

const client = new McpClient(transport);
await client.connect();

// Now you can interact with the server
// const tools = await client.listTools();
// console.log(tools);
```
Refer to the specific MCP SDK documentation for detailed client implementation guides.

### Available MCP Resources

Resources are used by MCP clients to retrieve data or state from the server (analogous to HTTP GET requests). This server exposes the following resources related to your Redshift database:

| Resource URI Pattern                     | Description                                                                               | Example URI                       |
| :--------------------------------------- | :---------------------------------------------------------------------------------------- | :-------------------------------- |
| `/scripts/{script_path}`                 | Retrieves the raw content of a SQL script file from the server's `sql_scripts` directory. | `/scripts/health/disk_usage.sql`  |
| `redshift://schemas`                     | Lists all accessible user-defined schemas in the connected database.                      | `redshift://schemas`              |
| `redshift://wlm/configuration`           | Retrieves the current Workload Management (WLM) configuration details.                    | `redshift://wlm/configuration`    |
| `redshift://schema/{schema_name}/tables` | Lists all accessible tables and views within the specified `{schema_name}`.               | `redshift://schema/public/tables` |

Replace `{script_path}` and `{schema_name}` with the actual values when making requests.
Accessibility of schemas/tables depends on the permissions granted to the Redshift user configured via `REDSHIFT_SECRET_ARN`.

### Available MCP Tools

Tools are used by MCP clients to request actions or computations from the server (analogous to HTTP POST requests). This server provides the following tools for interacting with Redshift:

| Tool Name                           | Description                                                                                                  | Input Parameters (Name, Type, Required, Description)                                                                                                                                                    | Output Description                                                                                                                                                                       | Example Invocation (Conceptual)                                                                                                                     |
| :---------------------------------- | :----------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `handle_check_cluster_health`       | Performs a health assessment of the Redshift cluster using a set of diagnostic SQL scripts.                  | `level` (string, No, 'Level of detail: "basic" or "full"'), `time_window_days` (integer, No, 'Lookback period in days for time-sensitive checks')                                                       | Dictionary mapping script names to results (list of dicts) or Exception objects.                                                                                                         | `use_mcp_tool("redshift-admin", "handle_check_cluster_health", {"level": "full", "time_window_days": 7})`                                           |
| `handle_diagnose_locks`             | Identifies active lock contention and blocking sessions in the cluster.                                      | `target_pid` (integer, No, 'Filter by process ID'), `target_table_name` (string, No, 'Filter by table name'), `min_wait_seconds` (integer, No, 'Minimum seconds a lock must be waiting to be included') | List of dictionaries, where each dictionary represents a row from the lock contention query result.                                                                                      | `use_mcp_tool("redshift-admin", "handle_diagnose_locks", {"min_wait_seconds": 10})`                                                                 |
| `handle_diagnose_query_performance` | Analyzes a specific query's execution performance, including plan, metrics, and historical data.             | `query_id` (integer, Yes, 'The numeric ID of the Redshift query to analyze'), `compare_historical` (boolean, No, 'Fetch performance data for previous runs of the same query text')                     | Dictionary mapping script names to results (list of dicts) or Exception objects.                                                                                                         | `use_mcp_tool("redshift-admin", "handle_diagnose_query_performance", {"query_id": 12345, "compare_historical": true})`                              |
| `handle_execute_ad_hoc_query`       | Executes an arbitrary SQL query provided by the user via Redshift Data API. Designed as an escape hatch.     | `sql_query` (string, Yes, 'The exact SQL query string to execute.')                                                                                                                                     | Dictionary with `status`, `columns`, `rows`, `row_count` on success, or raises an exception on failure.                                                                                  | `use_mcp_tool("redshift-admin", "handle_execute_ad_hoc_query", {"sql_query": "SELECT COUNT(*) FROM users WHERE registration_date > '2023-01-01'"})` |
| `handle_get_table_definition`       | Retrieves the DDL (Data Definition Language) statement (`SHOW TABLE`) for a specific table.                  | `schema_name` (string, Yes, 'The schema name of the table.'), `table_name` (string, Yes, 'The name of the table.')                                                                                      | String containing the CREATE TABLE statement (DDL) or raises an exception if not found or an error occurs.                                                                               | `use_mcp_tool("redshift-admin", "handle_get_table_definition", {"schema_name": "public", "table_name": "products"})`                                |
| `handle_inspect_table`              | Retrieves detailed information about a specific Redshift table, covering design, storage, health, and usage. | `schema_name` (string, Yes, 'The schema name of the table.'), `table_name` (string, Yes, 'The name of the table.')                                                                                      | A dictionary where keys are script names and values are either the raw list of dictionary results, the extracted DDL string, or an Exception object if that specific script failed.      | `use_mcp_tool("redshift-admin", "handle_inspect_table", {"schema_name": "analytics", "table_name": "user_sessions"})`                               |
| `handle_monitor_workload`           | Analyzes cluster workload patterns over a specified time window using various diagnostic scripts.            | `time_window_days` (integer, No, 'Lookback period in days for the workload analysis.'), `top_n_queries` (integer, No, 'Number of top queries (by total execution time) to consider')                    | A dictionary where keys are script names (e.g., 'workload/top_queries.sql') and values are either a list of result rows (as dictionaries) or the Exception object if that script failed. | `use_mcp_tool("redshift-admin", "handle_monitor_workload", {"time_window_days": 7, "top_n_queries": 20})`                                           |

Tool names and parameters must match the server's implementation exactly.
Ensure the Redshift user configured via `REDSHIFT_SECRET_ARN` has the necessary permissions for the tools you intend to use.

## Development

Instructions for developers who want to contribute to or modify this project.

Prerequisites: Ensure you have completed the [Installation](#installation) steps (using the "From Source" method) and have all [Prerequisites](#prerequisites) met.

Install Development Dependencies:
This project uses `uv` and dependencies are managed via `pyproject.toml`. Development dependencies are likely in a `[project.optional-dependencies.dev]` group.
```bash
uv sync --dev
```

Running Tests:
This project uses `pytest` for testing.
```bash
pytest
```

Code Style & Linting:

This project uses `ruff` for code formatting and linting.
Please format your code before committing:
```bash
ruff format .
```
Run the linter using:
```bash
ruff check .
```
(Optional) Consider setting up pre-commit hooks: (Not explicitly configured in provided files)

Refer to the (CODE\_STYLE.md) file for detailed guidelines (if applicable).

Building (if applicable):
This is a Python project and does not require a separate build step before running.

## TO DO
- [ ] Improve Prompt Options
- [ ] Add support for more credential methods
- [ ] Add Support for Redshift Serverless

## Contributing

Contributions are welcome! Please follow these guidelines.

Find/Report Issues: Check the GitHub Issues page for existing bugs or feature requests. Feel free to open a new issue if needed.

Security is critical when providing database access via an MCP server. Please consider the following:

🔒 **Credentials Management:** This server uses AWS Secrets Manager via the Redshift Data API, which is a more secure approach than storing credentials directly in environment variables or configuration files. Ensure your AWS credentials used by Boto3 (via environment, profile, or IAM role) are managed securely and have the minimum necessary permissions. Never commit your AWS credentials or `.env` files containing secrets to version control.

🛡️ **Principle of Least Privilege:** Configure the Redshift user whose credentials are in AWS Secrets Manager with the minimum permissions required for the server's intended functionality. For example, if only read access is needed, grant only `CONNECT` and `SELECT` privileges on the necessary schemas/tables and `SELECT` on the required system views. Avoid using highly privileged users like `admin` or the cluster superuser.


For guidance on creating restricted Redshift users and managing permissions, refer to the official (https://docs.aws.amazon.com/redshift/latest/mgmt/security.html).

## License

This project is licensed under the MIT License. See the (LICENSE) file for details.

## References

*   This project relies heavily on the [Model Context Protocol specification](https://modelcontextprotocol.io/specification/).
*   Built using the official MCP SDK provided by [Model Context Protocol](https://modelcontextprotocol.io/).
*   Utilizes the AWS SDK for Python ([Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)) to interact with the [Amazon Redshift Data API](https://docs.aws.amazon.com/redshift-data/latest/APIReference/Welcome.html).
*   Many of the diagnostic SQL scripts are adapted from the excellent [awslabs/amazon-redshift-utils](https://github.com/awslabs/amazon-redshift-utils) repository.
