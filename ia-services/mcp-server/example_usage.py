# Example usage of the API Structure Service

from src.domain.getting_back_api_structure import APIStructureService

def main():
    # Create the service
    api_service = APIStructureService()
    
    # Define the base URL of the API
    base_url = "http://localhost:8000"  # Replace with your actual API base URL
    
    try:
        # Get the OpenAPI documentation
        print("Fetching OpenAPI documentation...")
        openapi_docs = api_service.fetch_openapi_documentation(base_url)
        
        # Analyze the API structure
        print("Analyzing API structure...")
        api_structure = api_service.analyze_api_structure(openapi_docs)
        
        # Print API information
        print("\nAPI Information:")
        print(f"Title: {api_structure['info'].get('title')}")
        print(f"Version: {api_structure['info'].get('version')}")
        
        # List endpoints
        print("\nListing all endpoints:")
        endpoints = api_service.list_endpoints(base_url)
        for endpoint in endpoints:
            print(f"{endpoint['method']} {endpoint['path']} - {endpoint['summary']}")
        
        # Get details of a specific endpoint (example)
        if endpoints:
            example = endpoints[0]
            print(f"\nDetails for {example['method']} {example['path']}:")
            details = api_service.get_endpoint_details(base_url, example['path'], example['method'])
            print(f"Summary: {details.get('summary')}")
            print(f"Description: {details.get('description')}")
            print(f"Parameters: {len(details.get('parameters', []))}")
            print(f"Responses: {list(details.get('responses', {}).keys())}")
        
        print(f"\nTotal endpoints: {len(endpoints)}")
        print(f"Total schemas: {len(api_structure['schemas'])}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
