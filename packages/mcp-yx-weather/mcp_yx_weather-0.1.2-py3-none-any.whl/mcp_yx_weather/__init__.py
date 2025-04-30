from .yxweather.weather import mcp
def main() -> None:
    print("Hello from mcp-yx-weather!")
    mcp.run(transport='stdio')

