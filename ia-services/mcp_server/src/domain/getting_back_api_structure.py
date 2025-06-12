
from typing import Dict, Any, List
import requests
from src.ports.drivers.for_consult_api_schema import OpenAPIServicePort

class OpenAPIService:
    """
    Domain service for retrieving and analyzing API structure.
    All the logic is implemented here.
    """
    
    def __init__(self):
        pass
    
    def fetch_openapi_documentation(self, base_url: str='http://localhost:8000') -> Dict[Any, Any]:
        """
        Fetches the OpenAPI documentation from the API.
        
        Args:
            base_url (str): The base URL of the API (e.g. "http://localhost:8000")
            
        Returns:
            Dict[Any, Any]: The OpenAPI/Swagger documentation as a dictionary
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        try:
            # Get the OpenAPI documentation from the API
            openapi_url = f"{base_url.rstrip('/')}/openapi.json"
            response = requests.get(openapi_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Try alternative URL format for Swagger
            try:
                swagger_url = f"{base_url.rstrip('/')}/swagger.json"
                response = requests.get(swagger_url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException:
                # If both attempts fail, raise the original exception
                raise e

    def analyze_api_structure(self, openapi_docs: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Analyzes the OpenAPI documentation and extracts relevant information about the API structure.
        
        Args:
            openapi_docs (Dict[Any, Any]): The OpenAPI documentation
            
        Returns:
            Dict[str, Any]: A structured representation of the API
        """
        # Extract API information
        api_info = {
            "info": {
                "title": openapi_docs.get("info", {}).get("title", ""),
                "version": openapi_docs.get("info", {}).get("version", ""),
                "description": openapi_docs.get("info", {}).get("description", "")
            },
            "endpoints": {},
            "schemas": {}
        }

        # Process paths and endpoints
        paths = openapi_docs.get("paths", {})
        for path, path_info in paths.items():
            api_info["endpoints"][path] = {}
            for method, method_info in path_info.items():
                if method.lower() in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    api_info["endpoints"][path][method.lower()] = {
                        "summary": method_info.get("summary", ""),
                        "description": method_info.get("description", ""),
                        "parameters": method_info.get("parameters", []),
                        "responses": method_info.get("responses", {}),
                        "requestBody": method_info.get("requestBody", None)
                    }
        
        # Process components/schemas (if available)
        schemas = openapi_docs.get("components", {}).get("schemas", {})
        for schema_name, schema in schemas.items():
            api_info["schemas"][schema_name] = schema
            
        return api_info

    def list_endpoints(self, base_url: str='http://localhost:8000') -> List[Dict[str, Any]]:
        """
        Lists all available endpoints from the API.
        
        Args:
            base_url (str): The base URL of the API
            
        Returns:
            List[Dict[str, Any]]: A list of endpoints with their details
        """
        openapi_docs = self.fetch_openapi_documentation(base_url)
        api_structure = self.analyze_api_structure(openapi_docs)
        
        endpoints = []
        for path, methods in api_structure["endpoints"].items():
            for method, details in methods.items():
                endpoints.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": details["summary"],
                    "description": details["description"]
                })
        
        return endpoints

    def get_endpoint_details(self, base_url: str='http://localhost:8000', path: str='', method: str='') -> Dict[str, Any]:
        """
        Gets detailed information about a specific endpoint.
        
        Args:
            base_url (str): The base URL of the API
            path (str): The endpoint path
            method (str): The HTTP method (GET, POST, etc.)
            
        Returns:
            Dict[str, Any]: Detailed information about the endpoint
        """
        openapi_docs = self.fetch_openapi_documentation(base_url)
        api_structure = self.analyze_api_structure(openapi_docs)
        
        if path in api_structure["endpoints"] and method.lower() in api_structure["endpoints"][path]:
            return api_structure["endpoints"][path][method.lower()]
        
        return {}
