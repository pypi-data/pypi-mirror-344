from .server import app

def main():
    """MCP Time Server - Time and timezone conversion functionality for MCP"""
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(
        description="give a model the ability to handle time queries and timezone conversions"
    )
    parser.add_argument("--local-timezone", type=str, help="Override local timezone")

    args = parser.parse_args()
    print("-----加载2-----")
    uvicorn.run(app)




if __name__ == "__main__":
    main()