from open_data_mcp.core.server import mcp
import open_data_mcp.tools.search  # noqa: F401
import open_data_mcp.prompts.search  # noqa: F401


def main():
    mcp.run()


if __name__ == "__main__":
    main()
