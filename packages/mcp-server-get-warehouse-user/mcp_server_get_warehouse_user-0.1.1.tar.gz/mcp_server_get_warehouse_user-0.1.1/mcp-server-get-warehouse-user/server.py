from tkinter import NO
from mcp.server.fastmcp import FastMCP
import json
import httpx
from typing import Any
import argparse
import sys

mcp = FastMCP()
MY_SERVER_API_BASE="http://8.153.97.36:8093/empInfo/getSql"  # 添加这行

# 全局变量用于存储密码
EMP_PASSWORD = None

async def get_emp_info() -> Any:
    """获取员工信息"""
    print("获取员工信息")
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(MY_SERVER_API_BASE, json={
                "password": EMP_PASSWORD,
                "sql":"select COUNT(*) from emp_info"
            })
            if response.status_code == 200:
                print(f"获取员工信息成功: {response.json()}")
                return response.json()
            else:
                print(f"获取员工信息失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取员工信息失败: {e}")
            return None

@mcp.tool()
async def  get_warehouse_user()-> str:
    """
    输入获取员工信息，返回目前员工总数
    ：param emp_info: 员工信息
    ：return: 员工信息
    """
    print("工具被调用1")
    emp_info = await get_emp_info()
    if emp_info:
        return json.dumps(emp_info, ensure_ascii=False)
    else:
        return "获取员工信息失败"

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='获取仓库用户信息')
    parser.add_argument("--password", type=str, required=True, help="用来连接的密码")
    
    # 如果没有参数，显示帮助信息并退出
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    return parser.parse_args()

if __name__ == "__main__":
    """主方法入口"""
    args = parse_args()
    EMP_PASSWORD = args.password
    mcp.run(transport="stdio")