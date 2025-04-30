#!/usr/bin/env python
"""
MCP Server main script for DoLMcpServerPy

This script starts an MCP server and registers the health tools.
"""


import asyncio
from mcp.server.fastmcp import FastMCP
from health_tools import get_entity_health_async, get_health_model_async

# Create server
server = FastMCP("HealthMcpServer")

@server.tool(name="GetEntityHealthPy", description="Get the health of an entity")
async def get_entity_health_tool(entity_id: str, health_model_name: str, resource_group_name: str, subscription_id: str, start_time: str = None) -> str:
    try:
        # Capture the response but don't print it to the console
        result = await get_entity_health_async(entity_id, health_model_name, resource_group_name, subscription_id, start_time)
        
        # Ensure the result is in the proper format for the MCP protocol
        return result
    except Exception as e:
        return f"Error retrieving entity health: {str(e)}"
             
@server.tool(name="GetHealthModelPy", description="Get the health model")
async def get_health_model_tool(health_model_name: str, resource_group_name: str, subscription_id: str) -> str:
    try:
        # Capture the response but don't print it to the console
        result = await get_health_model_async(health_model_name, resource_group_name, subscription_id)
        
        # Ensure the result is in the proper format for the MCP protocol
        return result
    except Exception as e:
        return f"Error retrieving health model: {str(e)}"

if __name__ == "__main__":
    server.run()
