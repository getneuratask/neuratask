from typing import Dict, Any, List
from src.domain.getting_back_api_structure import OpenAPIService

class OpenAPIServiceAdapter:
    """
    Adapter for OpenAPI service.
    Simply passes methods to the domain service implementation.
    """
    
    def __init__(self):
        self.service = OpenAPIService()
    
    def fetch_openapi_documentation(self, base_url: str) -> Dict[Any, Any]:
        """
        Passes the fetch_openapi_documentation call to the domain service.
        
        Args:
            base_url (str): The base URL of the API
            
        Returns:
            Dict[Any, Any]: The OpenAPI/Swagger documentation
        """
        return self.service.fetch_openapi_documentation(base_url)
    
    def analyze_api_structure(self, openapi_docs: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Passes the analyze_api_structure call to the domain service.
        
        Args:
            openapi_docs (Dict[Any, Any]): The OpenAPI documentation
            
        Returns:
            Dict[str, Any]: A structured representation of the API
        """
        return self.service.analyze_api_structure(openapi_docs)
    
    def list_endpoints(self, base_url: str) -> List[Dict[str, Any]]:
        """
        Passes the list_endpoints call to the domain service.
        
        Args:
            base_url (str): The base URL of the API
            
        Returns:
            List[Dict[str, Any]]: A list of endpoints with their details
        """
        return self.service.list_endpoints(base_url)
    
    def get_endpoint_details(self, base_url: str, path: str, method: str) -> Dict[str, Any]:
        """
        Passes the get_endpoint_details call to the domain service.
        
        Args:
            base_url (str): The base URL of the API
            path (str): The endpoint path
            method (str): The HTTP method (GET, POST, etc.)
            
        Returns:
            Dict[str, Any]: Detailed information about the endpoint
        """
        return self.service.get_endpoint_details(base_url, path, method)
