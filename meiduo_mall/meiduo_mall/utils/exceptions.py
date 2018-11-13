"""
由于一些数据库的异常django不能捕获，要自己捕获
做个异常处理的方法
"""

from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

# 获取在配置文件中定义的logger，用来记录日志 这里的django就是setting日志器命名的
logger = logging.getLogger('django')

def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)
    # 没有响应要么就是没报错，要么就是报错没法识别，没法识别如果是数据库错误就返回
    if response is None:
        # 视图上下文
        view = context['view']
        # 捕获数据库的异常，如果exc是数据库异常
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response