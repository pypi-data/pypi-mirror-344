import asyncio

from explorium_mcp_server.models.prospects import FetchProspectsFilters
from explorium_mcp_server.tools.prospects import fetch_prospects


async def main():
    res = fetch_prospects(
        FetchProspectsFilters(business_id=["43d292ca62195430814bafcd77643fc2"], job_level=["cxo"]))
    a = 1


if __name__ == '__main__':
    asyncio.run(main())
