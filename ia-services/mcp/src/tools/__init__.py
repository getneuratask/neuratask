"""Tools module for MCP server"""
from  tools.checking_health import check_health
from tools.tasks import get_tasks_by_project
__all__ = ["check_health", "get_tasks_by_project"]

if __name__ == "__main__":
    check_health()
    get_tasks_by_project("a05abff7-3968-4328-acaf-482657e817ff")
