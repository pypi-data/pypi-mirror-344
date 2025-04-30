import os
import json
import os

import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel,Field
from typing import Dict, Any, Optional

from mcp.server import FastMCP

mcp=FastMCP("mcp_Weather_sse")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_API_URL = "http://api.map.baidu.com"

#自定义输入参数模型（自动生成input_schema）

@mcp.tool(
    name="make_baidu_get_weather_request",
    description="根据行政区划编码，获取指定行政区划的实时天气和预报信息",
)
async def make_baidu_get_weather_request(district_id :str)-> Dict[str, Any]:
    #注意下面三引号包括的部分，那是docstring，一种文档说明字符串
    #在mcp开发中，mcp.tool()装饰器会根据方法的参数定义自动生成input_schema
    #以及docstring中的description，作为tool的描述
    #所以在开发mcp_server的过程中，docstring要仔细写
    """查天气，向百度天气api发送请求,并返回原始数据

    Name:天气查询服务

    Description:用户可通过区县的行政区划编码或者经纬度（经度在前纬度在后，逗号分隔）来查询实时天气和预报信息

    Args:
        district_id (str): 区县的行政区划编码，6位（例如：222405）
    """
    print("==服务端== 实际接收到的参数:", district_id)
    print("==服务端== 参数类型:", type(district_id))
    #assert isinstance(params, dict), "参数必须是字典类型"

    #设置请求参数
    #更多参数信息请参考https://lbsyun.baidu.com/faq/api?title=webapi/weather/base
    params = {
        "district_id": district_id,
        "data_type": "all",
        "ak": BAIDU_API_KEY,
    }
    url = f"{BAIDU_API_URL}/weather/v1/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,params=params)

            response.raise_for_status()
            result = response.json()


            if result.get("status")!=0:
                error_msg = result.get("message", "unkown error")
                raise Exception(f"==Server== API response error: {error_msg}")

            return {
                "status": response.status_code,
                "data": response.json(),  #MCP规范建议封装原始数据
                "metadata":{"source":"baidu"}
            }
        except httpx.HTTPStatusError as e:
            raise ValueError(f"=Server= HTTP请求失败，状态码：{e.response.status_code}") from e
        except Exception as e:
            raise ValueError(f"=Server= 请求失败，错误信息：{e}") from e


def main():
    print("sse server starting...")
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()