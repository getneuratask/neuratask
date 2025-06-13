from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import asyncio
from tools import checking_health, tasks


# Create a FastMCP server
mcp = FastMCP("API Structure MCP Server")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def check_health() -> dict:
    """Check the health of the service"""
    return checking_health.check_health()

@mcp.tool()
def get_tasks_by_project(project_id: str) -> List[Dict[str, Any]]:
    """Get tasks by project ID"""
    return tasks.get_tasks_by_project(project_id)

# Main entry point for the script
def main():
    """Run the MCP server"""
    asyncio.run(mcp.run())


if __name__ == "__main__":
    main()



