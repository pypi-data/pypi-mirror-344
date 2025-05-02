
from .server import serve

def main():
    import asyncio

    print("Starting Dog Eye Diagnosis MCP server...")
    asyncio.run(serve())


if __name__ == "__main__":
    main()
