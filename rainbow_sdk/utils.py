# coding: utf-8
import importlib
import logging

logger = logging.getLogger("rainbow")


def get_route(mod_id, cmd_id, timeout=0.2, python_ver="3.6", libc_ver="2.1"):
    """获得cl5路由信息 ."""
    # 动态加载模块
    python_ver_dir = "python{}".format(python_ver.replace(".", "_"))
    libc_ver_dir = "libc_{}".format(libc_ver.replace(".", "_"))
    package = "python_sdk.cl5.{}.{}".format(python_ver_dir, libc_ver_dir)
    l5sys = importlib.import_module(".l5sys", package)
    # 获取路由，传递要调用的后端服务注册的 sid(modId:cmdId)值,设置调用超时时间
    ret, qos = l5sys.ApiGetRoute({"modId": mod_id, "cmdId": cmd_id}, timeout)
    if ret < 0:
        return False
    ip = qos["hostIp"]
    port = qos["hostPort"]
    return ip, port


def get_local_host_ip(ifname=b"eth1"):
    """获得本机的IP地址 ."""
    import socket
    ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        pass
    finally:
        s.close()

    if ip:
        return ip

    import platform
    import socket

    if platform.system() == "Linux":
        import fcntl
        import struct

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        o_ip = socket.inet_ntoa(
            fcntl.ioctl(s.fileno(), 0x8915, struct.pack("256s", ifname[:15]))[20:24]
        )
    else:
        try:
            o_ip = socket.gethostbyname(socket.gethostname())
        except Exception as e:
            # 如果Mac环境未配置本机HOST，默认未127.0.0.1
            o_ip = "127.0.0.1"

    return o_ip
