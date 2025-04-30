"""
Health Tools for DoLMcp Server Python implementation

This module provides tools for accessing health information from Azure's Cloud Health service.
"""

import os
import json
import logging
import datetime
import traceback
import requests
from azure.identity import DefaultAzureCredential
from typing import Optional

# Set up logging
LOG_FILE_PATH = r"c:\temp\McpServerPy.txt"
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_this(message: str) -> None:
    """Log a message to the file and console."""
    try:
        logging.info(message)
        print(message)
    except Exception as ex:
        print(f"Failed to write to log file: {str(ex)}")

async def get_azure_token(resource: str) -> str:
    """
    Gets an Azure authentication token for the specified resource.
    
    Args:
        resource: The resource URI for which the token is requested
        
    Returns:
        A bearer token for the specified resource
    """
    log_this(f"Getting token for resource: {resource}")
    
    try:
        # Create a default Azure credential
        credential = DefaultAzureCredential()
        
        # Get token for the specified resource
        token = credential.get_token(f"{resource}/.default")
        
        log_this(f"Token retrieved for resource: {resource}")
        return token.token
    except Exception as ex:
        error_message = f"Error getting Azure token: {str(ex)}"
        log_this(error_message)
        raise Exception(error_message)

async def get_control_plane_token() -> str:
    """Get Azure authentication token for management operations."""
    return await get_azure_token("https://management.azure.com")

async def get_dataplane_token() -> str:
    """Get Azure authentication token for data plane operations."""
    return await get_azure_token("https://data.healthmodels.azure.com")

def parse_dataplane_endpoint(json_response: str) -> str:
    """
    Extract dataplane endpoint from the JSON response.
    
    Args:
        json_response: The JSON response containing the dataplane endpoint
        
    Returns:
        The dataplane endpoint URL
    """
    #log_this(f"Parsing dataplane endpoint from JSON: {json_response}")
    
    try:
        # Parse the JSON response
        json_obj = json.loads(json_response)
        
        # Extract the dataplane endpoint
        dataplane_endpoint = json_obj.get("properties", {}).get("dataplaneEndpoint")
        
        log_this(f"Successfully extracted dataplane endpoint: {dataplane_endpoint}")
        
        if not dataplane_endpoint:
            raise Exception("Dataplane endpoint is null or empty in the response.")
        
        return dataplane_endpoint
    except Exception as ex:
        error_message = f"Error parsing dataplane endpoint: {str(ex)}"
        log_this(error_message)
        raise Exception(error_message)

async def get_dataplane_endpoint_async(subscription_id: str, resource_group_name: str, health_model_name: str) -> str:
    """
    Get the dataplane endpoint for a health model.
    
    Args:
        subscription_id: Azure subscription ID
        resource_group_name: Resource group name
        health_model_name: Health model name
        
    Returns:
        The dataplane endpoint URL
    """
    # Get Azure authentication token for management operations
    token = await get_control_plane_token()
    log_this("Control plane token retrieved successfully")
    
    health_model_url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.CloudHealth/healthmodels/{health_model_name}?api-version=2023-10-01-preview"
    log_this(f"Health model URL: {health_model_url}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    log_this(f"Getting health model from URL: {health_model_url}")
    
    response = requests.get(health_model_url, headers=headers)
    log_this(f"Response status code: {response.status_code}")
    
    response.raise_for_status()
    
    # Read the response content
    response_string = response.text
    #log_this(f"Health model response content: {response_string}")
    
    # Parse the dataplane endpoint
    dataplane_endpoint = parse_dataplane_endpoint(response_string)
    log_this(f"Dataplane endpoint: {dataplane_endpoint}")
    
    return dataplane_endpoint

async def get_dataplane_response_async(url: str) -> str:
    """
    Get response from the dataplane endpoint.
    
    Args:
        url: The endpoint URL to query
        
    Returns:
        The response content as a string
    """
    dataplane_token = await get_dataplane_token()
    log_this("Dataplane token retrieved successfully")
    
    headers = {
        "Authorization": f"Bearer {dataplane_token}"
    }
    
    health_response = requests.get(url, headers=headers)
    log_this(f"Request to {url} returned status code: {health_response.status_code}")
    
    health_response.raise_for_status()
    
    health_response_string = health_response.text
    #log_this(f"Health response content: {health_response_string}")
    
    return health_response_string

async def get_entity_health_async(entity: str, health_model_name: str, resource_group_name: str, subscription_id: str, 
                           start_time: str = None) -> str:
    """
    Get the health of an entity.
    
    Args:
        entity: The entity to get the health of
        health_model_name: The health model name
        resource_group_name: The resource group name
        subscription_id: The subscription ID
        start_time: The start time for health history (optional)
        end_time: The end time for health history (optional)
        
    Returns:
        The health information as a JSON string
    """
    try:
        # Set default times if not provided
        if not start_time:
            # Default to 24 hours ago
            start_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        # Default to current time
        end_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            
        dataplane_endpoint = await get_dataplane_endpoint_async(subscription_id, resource_group_name, health_model_name)
        
        # Get the health of the entity
        entity_health_url = f"{dataplane_endpoint}api/entities/{entity}/history?startTime={start_time}&endTime={end_time}"
        log_this(f"Entity health URL: {entity_health_url}")
        
        health_response_string = await get_dataplane_response_async(entity_health_url)
        return health_response_string
    except Exception as ex:
        error_message = f"Error in get_entity_health_async: {str(ex)}"
        if hasattr(ex, '__cause__') and ex.__cause__:
            error_message += f" Inner exception: {str(ex.__cause__)}"
        log_this(error_message)
        log_this(f"Stack trace: {traceback.format_exc()}")
        raise

async def get_health_model_async(health_model_name: str, resource_group_name: str, subscription_id: str) -> str:
    """
    Get the health model.
    
    Args:
        health_model_name: The health model name
        resource_group_name: The resource group name
        subscription_id: The subscription ID
        
    Returns:
        The health model information as a JSON string
    """
    try:
        dataplane_endpoint = await get_dataplane_endpoint_async(subscription_id, resource_group_name, health_model_name)
        
        # Get the health model
        health_model_url = f"{dataplane_endpoint}api/views/default/v2/query"
        log_this(f"Healthmodel URL: {health_model_url}")
        
        health_response_string = await get_dataplane_response_async(health_model_url)
        return health_response_string
    except Exception as ex:
        error_message = f"Error in get_health_model_async: {str(ex)}"
        if hasattr(ex, '__cause__') and ex.__cause__:
            error_message += f" Inner exception: {str(ex.__cause__)}"
        log_this(error_message)
        log_this(f"Stack trace: {traceback.format_exc()}")
        raise