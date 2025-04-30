from src.mcp_pokemon_server.zekang import mcp


def main() -> None:
    print("Hello from mcp-pokemon-server!")
    mcp.run(transport='studio')
