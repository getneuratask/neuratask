
import requests
import json
import argparse
from pprint import pprint

def call_mcp_tool(tool_name, params=None):
    """
    Makes a call to an MCP tool.
    
    Args:
        tool_name (str): The name of the tool to call
        params (dict, optional): The parameters to pass to the tool
    
    Returns:
        The response from the tool
    """
    url = "http://localhost:3000/api/tools"  # Default MCP server port is 3000
    
    data = {
        "tool_name": tool_name,
        "tool_params": params or {}
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    
    return response.json()

def main():
    parser = argparse.ArgumentParser(description='Test API structure tools')
    parser.add_argument('--tool', choices=['fetch', 'list', 'details', 'analyze'], required=True, 
                        help='Tool to test: fetch documentation, list endpoints, get endpoint details, or analyze structure')
    parser.add_argument('--base-url', default='http://localhost:8000', help='Base URL of the API')
    parser.add_argument('--path', help='Endpoint path (for get_endpoint_details)')
    parser.add_argument('--method', help='HTTP method (for get_endpoint_details)')
    
    args = parser.parse_args()
    
    try:
        if args.tool == 'fetch':
            result = call_mcp_tool("fetch_api_documentation", {"base_url": args.base_url})
            print("API Documentation fetched successfully!")
            print(f"API Version: {result.get('info', {}).get('version')}")
            print(f"API Title: {result.get('info', {}).get('title')}")
        
        elif args.tool == 'list':
            result = call_mcp_tool("list_api_endpoints", {"base_url": args.base_url})
            print(f"\nFound {len(result)} endpoints:")
            for endpoint in result[:10]:  # Show first 10 to avoid clutter
                print(f"{endpoint['method']} {endpoint['path']} - {endpoint['summary']}")
            if len(result) > 10:
                print(f"... and {len(result) - 10} more")
        
        elif args.tool == 'details':
            if not args.path or not args.method:
                print("Error: Both --path and --method are required for endpoint details")
                return
                
            result = call_mcp_tool("get_endpoint_details", {
                "base_url": args.base_url,
                "path": args.path,
                "method": args.method
            })
            print(f"\nDetails for {args.method} {args.path}:")
            print(f"Summary: {result.get('summary')}")
            print(f"Description: {result.get('description')}")
            print("\nParameters:")
            for param in result.get('parameters', []):
                print(f"  - {param.get('name')} ({param.get('in')}): {param.get('description')}")
            
            print("\nResponses:")
            for status, response in result.get('responses', {}).items():
                print(f"  - {status}: {response.get('description')}")
        
        elif args.tool == 'analyze':
            result = call_mcp_tool("analyze_api_structure", {"base_url": args.base_url})
            print("\nAPI Analysis Summary:")
            print(f"API Title: {result.get('info', {}).get('title')}")
            print(f"API Version: {result.get('info', {}).get('version')}")
            print(f"Endpoints count: {len(result.get('endpoints', {}))}")
            print(f"Schemas count: {len(result.get('schemas', {}))}")
            
            # Show a sample of endpoints and schemas
            if result.get('endpoints'):
                print("\nSample endpoints:")
                for i, (path, methods) in enumerate(result.get('endpoints', {}).items()):
                    if i >= 3:  # Show only 3 examples
                        break
                    print(f"  - {path}: {', '.join(methods.keys())}")
            
            if result.get('schemas'):
                print("\nSample schemas:")
                for i, schema_name in enumerate(list(result.get('schemas', {}).keys())[:3]):
                    if i >= 3:  # Show only 3 examples
                        break
                    print(f"  - {schema_name}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling MCP tool: {e}")
    except json.JSONDecodeError:
        print("Error decoding response as JSON")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
