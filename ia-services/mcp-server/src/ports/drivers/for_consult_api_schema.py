from typing import Dict, Any, Protocol, List

class OpenAPIServicePort(Protocol):
    """
    Port defining the interface for OpenAPI service.
    This is the interface that domain services must implement.
    """
    
    def fetch_openapi_documentation(self, base_url: str) -> Dict[Any, Any]:
        """
        Fetches the OpenAPI documentation from the API.
        
        Args:
            base_url (str): The base URL of the API
            
        Returns:
            Dict[Any, Any]: The OpenAPI/Swagger documentation
        """
        ...
    
    def analyze_api_structure(self, openapi_docs: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Analyzes the OpenAPI documentation and extracts relevant information.
        
        Args:
            openapi_docs (Dict[Any, Any]): The OpenAPI documentation
            
        Returns:
            Dict[str, Any]: A structured representation of the API
        """
        ...
    
    def list_endpoints(self, base_url: str) -> List[Dict[str, Any]]:
        """
        Lists all available endpoints from the API.
        
        Args:
            base_url (str): The base URL of the API
            
        Returns:
            List[Dict[str, Any]]: A list of endpoints with their details
        """
        ...
    
    def get_endpoint_details(self, base_url: str, path: str, method: str) -> Dict[str, Any]:
        """
        Gets detailed information about a specific endpoint.
        
        Args:
            base_url (str): The base URL of the API
            path (str): The endpoint path
            method (str): The HTTP method (GET, POST, etc.)
            
        Returns:
            Dict[str, Any]: Detailed information about the endpoint
        """
        ...
