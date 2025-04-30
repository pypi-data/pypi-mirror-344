import argparse
from trade_mcp.server.mcp_tools import setup_mcp_tools
from trade_mcp.api.client import APIClientManager

def main():
    """Main entry point for the trading MCP server.
    
    Run with:
        python -m trade_mcp.server.main --api-key YOUR_KEY --api-secret YOUR_SECRET --provider aster
    """
    parser = argparse.ArgumentParser(description='Run Trading MCP server')
    parser.add_argument('--api-key', required=True, help='API key for the trading platform')
    parser.add_argument('--api-secret', required=True, help='API secret for the trading platform')
    parser.add_argument('--provider', default='aster', choices=['aster', 'binance'], help='Trading platform provider')
    parser.add_argument('--testnet', action='store_true', help='Use testnet environment')
    args = parser.parse_args()

    # Initialize API client
    APIClientManager.initialize(
        api_key=args.api_key,
        api_secret=args.api_secret,
        provider=args.provider,
        testnet=args.testnet
    )

    # Set up and run MCP server
    mcp = setup_mcp_tools()
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main() 