# server.py
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from src.adapters.drivers.consulter_api_schema import OpenAPIServiceAdapter

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Create API Structure Service instance using the adapter
api_structure_service = OpenAPIServiceAdapter()

# Add API documentation tools
@mcp.tool()
def fetch_api_documentation(base_url: str = "http://localhost:8000") -> Dict[Any, Any]:
    """
    Fetches the OpenAPI documentation from an API.
    
    Args:
        base_url: The base URL of the API (e.g. "http://localhost:8000")
        
    Returns:
        The OpenAPI/Swagger documentation as a dictionary
    """
    return api_structure_service.fetch_openapi_documentation(base_url)

@mcp.tool()
def list_api_endpoints(base_url: str = "http://localhost:8000") -> List[Dict[str, Any]]:
    """
    Lists all available endpoints from the API.
    
    Args:
        base_url: The base URL of the API
        
    Returns:
        A list of endpoints with their details including path, method, summary, and description
    """
    return api_structure_service.list_endpoints(base_url)

@mcp.tool()
def get_endpoint_details(path: str, method: str, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Gets detailed information about a specific endpoint.
    
    Args:
        path: The endpoint path (e.g. "/users/{id}")
        method: The HTTP method (GET, POST, PUT, DELETE, etc.)
        base_url: The base URL of the API
        
    Returns:
        Detailed information about the endpoint including parameters, responses, etc.
    """
    return api_structure_service.get_endpoint_details(base_url, path, method)

@mcp.tool()
def analyze_api_structure(base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Analyzes the OpenAPI documentation and provides a structured representation of the API.
    
    Args:
        base_url: The base URL of the API
        
    Returns:
        A structured representation of the API including info, endpoints, and schemas
    """
    docs = api_structure_service.fetch_openapi_documentation(base_url)
    return api_structure_service.analyze_api_structure(docs)
    


