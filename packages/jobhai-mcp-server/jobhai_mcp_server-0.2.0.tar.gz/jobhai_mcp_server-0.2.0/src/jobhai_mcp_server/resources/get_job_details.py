import httpx
from mcp.types import TextContent

RESOURCE_NAME = "get_job_details"
DESCRIPTION = "Fetch job details by job_id"

async def execute(arguments: dict) -> list[TextContent]:
    job_id = arguments.get("job_id")
    if not job_id:
        raise ValueError("job_id is required")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api.jobhai.com/seo-js/open/job?job_id={job_id}")
        response.raise_for_status()
        return [TextContent(type="text", text=response.text)]
