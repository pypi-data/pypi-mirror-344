from . import server
from . import openrec_server
import asyncio
import sys

def main():
    """Main entry point for the package."""
    # デフォルトではノートサーバーを実行
    if len(sys.argv) <= 1 or sys.argv[1] != "openrec":
        asyncio.run(server.main())
    else:
        # 'openrec'引数が指定された場合はOpenREC.tv APIサーバーを実行
        openrec_server.mcp.run()

# Optionally expose other important items at package level
__all__ = ['main', 'server', 'openrec_server']