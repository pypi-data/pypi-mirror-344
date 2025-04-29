from mcp.server.fastmcp import FastMCP
import httpx

server = FastMCP("ip-server")


@server.tool()
async def ip() -> str:
    """
    Obtain the public IP address of the current machine.
    Returns:
        str: The result of the IP.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api64.ipify.org?format=json")
        if response.status_code != 200:
            return "Error: Failed to get IP."
        response = response.json()
        return response["ip"]


def test_main():
    """
    Test the tool.
    """

    async def test_ip():
        res = await ip()
        print(res)

    import asyncio

    asyncio.run(test_ip())


def main():
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
    # test_main()