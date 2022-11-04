# coding: utf-8


class RainbowException(Exception):
    status_code = 500


class ForbiddenException(RainbowException):
    code = 100


class ServerErrorException(RainbowException):
    """服务错误"""

    code = 500


class RpcErrorException(RainbowException):
    """rpc错误	rpc请求的错误，比如请求连接失败等"""

    code = 600


class RpcTimeoutException(RainbowException):
    """rpc超时错误	rpc请求超时返回的错误码"""

    code = 601


class WithoutChangeException(RainbowException):
    """版本无变更	本地请求的版本已是最新版本，会返回该错误码"""

    code = 702


class NotConfigException(RainbowException):
    """找不到任何配置	客户端回滚为空版本的时候"""

    code = 704


class NotVersionException(RainbowException):
    """	找不到任何版本	客户未发布任何版本、应用被删除、分组被删除，都会返回该错误码"""

    code = 707


class PollingTimeoutException(RainbowException):
    """长轮询服务端超时，客户端应该再次尝试请求"""

    code = 708
