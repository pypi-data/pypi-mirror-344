import os
from typing import Dict, Any
import requests
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional, Union

def get_api_key() -> str:
    """从环境变量获取高德API Key"""
    api_key = os.getenv("AMAP_MAPS_API_KEY")
    if not api_key:
        raise ValueError("请设置AMAP_MAPS_API_KEY环境变量")
    return api_key


# 初始化MCP服务
mcp = FastMCP("params-trans")


@mcp.tool()
def params_trans(
        int_param = None,
        float_param = None,
        bool_param = None,
        string_param = None
) -> Dict[str, Dict[str, Any]]:
    """
    验证单个参数的类型并返回详细的验证结果

    Args:
        int_param: 需要验证为整数的参数
        float_param: 需要验证为浮点数的参数
        bool_param: 需要验证为布尔值的参数
        string_param: 需要验证为字符串的参数

    Returns:
        字典，包含每个参数的详细验证结果:
        - 每个参数的验证结果包含:
            - 'value': 参数值
            - 'expected_type': 预期类型
            - 'actual_type': 实际类型
            - 'is_valid': 是否验证通过
            - 'message': 验证消息

    Example:

        {
            'int_param': {
                'value': 42,
                'expected_type': int,
                'actual_type': int,
                'is_valid': True,
                'message': '参数类型正确，预期类型: int，实际类型: int'
            },
            'float_param': {
                'value': "3.14",
                'expected_type': float,
                'actual_type': str,
                'is_valid': False,
                'message': '参数类型错误，预期类型: float，实际类型: str'
            }
        }
    """
    results = {}

    # 验证整数参数
    if int_param is not None:
        expected_type = int
        actual_type = type(int_param)
        is_valid = isinstance(int_param, expected_type)

        results['int_param'] = {
            'value': int_param,
            'expected_type': expected_type.__name__,
            'actual_type': actual_type.__name__,
            'is_valid': is_valid,
            'message': (
                f'参数类型正确，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
                if is_valid else
                f'参数类型错误，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
            )
        }

    # 验证浮点数参数
    if float_param is not None:
        expected_type = float
        actual_type = type(float_param)
        is_valid = isinstance(float_param, expected_type)

        results['float_param'] = {
            'value': float_param,
            'expected_type': expected_type.__name__,
            'actual_type': actual_type.__name__,
            'is_valid': is_valid,
            'message': (
                f'参数类型正确，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
                if is_valid else
                f'参数类型错误，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
            )
        }

    # 验证布尔值参数
    if bool_param is not None:
        expected_type = bool
        actual_type = type(bool_param)
        is_valid = isinstance(bool_param, expected_type)

        results['bool_param'] = {
            'value': bool_param,
            'expected_type': expected_type.__name__,
            'actual_type': actual_type.__name__,
            'is_valid': is_valid,
            'message': (
                f'参数类型正确，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
                if is_valid else
                f'参数类型错误，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
            )
        }

    # 验证字符串参数
    if string_param is not None:
        expected_type = str
        actual_type = type(string_param)
        is_valid = isinstance(string_param, expected_type)

        results['string_param'] = {
            'value': string_param,
            'expected_type': expected_type.__name__,
            'actual_type': actual_type.__name__,
            'is_valid': is_valid,
            'message': (
                f'参数类型正确，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
                if is_valid else
                f'参数类型错误，预期类型: {expected_type.__name__}，实际类型: {actual_type.__name__}'
            )
        }
    return results


def main():
    mcp.run()


if __name__ == "__main__":
    main()