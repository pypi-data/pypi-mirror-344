# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("mcp_server_jisuanqi")


# Add calculation tools
@mcp.tool()
def add(a: float, b: float) -> float:
    """
    加法计算
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之和
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    减法计算
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之差
    """
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    乘法计算
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之积
    """
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    除法计算
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之商
    
    Raises:
        ValueError: 当除数为0时抛出异常
    """
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

# Export the MCP instance
__all__ = ["mcp"]

if __name__ == "__main__":
    mcp.run()