
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from src.adapters.drivers.consulter_api_schema import OpenAPIServiceAdapter

# Create a FastMCP server
mcp = FastMCP("API Structure MCP Server")

# Create API Structure Service instance using the adapter
api_structure_service = OpenAPIServiceAdapter()

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add API documentation tools
@mcp.tool()
def fetch_api_documentation(base_url: str = "http://localhost:8000") -> str:
    """
    Fetches the OpenAPI documentation from an API.
    
    Args:
        base_url: The base URL of the API (e.g. "http://localhost:8000")
        
    Returns:
        The OpenAPI/Swagger documentation as a dictionary
    """
    try:
        result = api_structure_service.fetch_openapi_documentation(base_url)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_api_endpoints(base_url: str = "http://localhost:8000") -> str:
    """
    Lists all available endpoints from the API.
    
    Args:
        base_url: The base URL of the API
        
    Returns:
        A list of endpoints with their details including path, method, summary, and description
    """
    try:
        result = api_structure_service.list_endpoints(base_url)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_endpoint_details(path: str, method: str, base_url: str = "http://localhost:8000") -> str:
    """
    Gets detailed information about a specific endpoint.
    
    Args:
        path: The endpoint path (e.g. "/users/{id}")
        method: The HTTP method (GET, POST, PUT, DELETE, etc.)
        base_url: The base URL of the API
        
    Returns:
        Detailed information about the endpoint including parameters, responses, etc.
    """
    try:
        result = api_structure_service.get_endpoint_details(base_url, path, method)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def analyze_api_structure(base_url: str = "http://localhost:8000") -> str:
    """
    Analyzes the OpenAPI documentation and provides a structured representation of the API.
    
    Args:
        base_url: The base URL of the API
        
    Returns:
        A structured representation of the API including info, endpoints, and schemas
    """
    try:
        docs = api_structure_service.fetch_openapi_documentation(base_url)
        result = api_structure_service.analyze_api_structure(docs)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Add a dynamic greeting resource
@mcp.resource("greeting://demo")
def handle_greeting_resource() -> str:
    """A demonstration greeting resource"""
    return "Hello from MCP Demo Server!"



