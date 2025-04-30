# Health MCP Server

This project provides an MCP server for accessing Azure Cloud Health information using custom health tools.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Azure credentials set up for `DefaultAzureCredential` (e.g., via `az login` or environment variables)
- The following Python packages:
  - `requests`
  - `azure-identity`
  - `mcp` (ensure this is installed or available in your environment)


## Installation (from PyPI)

To install the package from PyPI:

```pwsh
pip install health-mcp-server
```

This will install all required dependencies.

## Running the MCP Server (after installation)

After installing, you can run the MCP server with:

```pwsh
python -m health_tools.HealthToolsMcpServer
```

Or, if you have set up a console script entry point, simply:

```pwsh
health-mcp-server
```

**Note:** Ensure your Azure credentials are set up (e.g., run `az login` or set environment variables for a service principal) before starting the server.

## Installation (from source)

1. Clone this repository.
2. Install dependencies:

   ```pwsh
   pip install requests azure-identity
   ```

   If `mcp` is not available on PyPI, ensure it is installed or accessible in your environment.

## Running the MCP Server

From the root directory, run:

```pwsh
mcp run src/HealthToolsMcpServer.py
```

The server will start and register the health tools.

### Use VS Code
Add the MCP server to VS code.

## Usage

The server exposes two main tools:

- **GetEntityHealthPy**: Get the health of an entity.
- **GetHealthModelPy**: Get the health model.

Refer to the code in `src/HealthToolsMcpServer.py` for details on tool parameters.

### Prompts
Typical prompts:

"Give me the health of the health model `{health_model_name}` in subscription `{subscription_id}` and resource group `{resource_group}`".

Once you have setup the context - health model, subscription id and resource group - you can query freely. For example:

* "Summarize the health for my health model"
* "Do you see any patterns in the health model"
* "Give me more details on the health of `{entity_name}`"

## Logging

Logs are written to `c:\temp\McpServerPy.txt`.

## Troubleshooting

- Ensure your Azure credentials are correctly configured.
- Check the log file for error details if something goes wrong.
