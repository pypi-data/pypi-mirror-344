from mcp.server.fastmcp import FastMCP

mcp = FastMCP("getUseeUser")

@mcp.tool()
def getUseeUser()->str :
    """
    获取雅索当前用户信息
    """
    return "建平是总经理，春哥是副总经理"


if __name__ == "__main__":
    mcp.run(transport="stdio")
