import httpx
from mcp.types import TextContent

RESOURCE_NAME = "get_dashboard_data"
DESCRIPTION = "Fetch dashboard data"

async def execute(arguments: dict) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://api.jobhai.com/seo-js/open/dashboard")
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
