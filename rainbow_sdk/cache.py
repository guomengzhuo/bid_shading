# coding: utf-8
import json
import os
import mmap

from rainbow_sdk.utils import logger

MEM_CACHE_FILE_PATH = "/tmp/"
MEM_CACHE_SIZE = 1024 * 1024 * 10  # 默认分配10M内存映射空间


class BaseCache(object):
    def __init__(self, options):
        self.options = options

    def get(self):
        pass

    def set(self, v):
        pass

    def clear(self):
        pass


class FileCache(BaseCache):
    def __init__(self, options):
        logger.info(options)
        super(FileCache, self).__init__(options)
        self.pull_item = options.get("pull_item")
        self.fileCachePath = options.get("fileCachePath")

    @property
    def key(self):
        # 根据请求参数构建缓存文件Key
        file_cache_key = "rainbow_"
        for k, v in self.pull_item.items():
            if k in ["app_id", "group"]:
                file_cache_key += "%s_%s_" % (k, v)
        file_cache_key += "configfile.txt"
        return self.fileCachePath + file_cache_key

    def get(self):
        if os.path.exists(self.key):
            # 读取文件内容返回
            with open(self.key, "r") as f:  # 打开文件
                data = f.read()
                if data:
                    return json.loads(data)
                else:
                    return False
        else:
            return False

    def set(self, config_values):
        # 验证缓存路径是否存在,不存在就创建
        if os.path.exists(self.fileCachePath):
            if not os.path.isdir(self.fileCachePath):
                return False
        else:
            try:
                os.makedirs(self.fileCachePath)
            except Exception as e:
                return False

        if os.name == "nt":
            import win32con
            import win32file
            import pywintypes
            __overlapped = pywintypes.OVERLAPPED()

            def lock(file, flags):
                handler_file = win32file._get_osfhandle(file.fileno())
                win32file.LockFileEx(handler_file, flags, 0, 0xffff0000, __overlapped)

            def unlock(file):
                handler_file = win32file._get_osfhandle(file.fileno())
                win32file.UnlockFileEx(handler_file, 0, 0xffff0000, __overlapped)
            with open(self.key, "w") as code:
                lock(code, win32con.LOCKFILE_EXCLUSIVE_LOCK)
                code.write(json.dumps(config_values))
                unlock(code)
        elif os.name == "posix":
            import fcntl
            with open(self.key, "w") as code:
                fcntl.flock(code.fileno(), fcntl.LOCK_EX)  # 加锁
                code.write(json.dumps(config_values))

        return True

    def clear(self):
        pass

    def clear_all(self):
        pass


class MemCache(BaseCache):
    def __init__(self, options):
        super(MemCache, self).__init__(options)
        self.pull_item = options.get("pull_item")

    @property
    def key(self):
        file_cache_key = MEM_CACHE_FILE_PATH + "rainbow_"
        # 根据请求参数构建缓存文件Key
        for k, v in self.pull_item.items():
            if k in ["app_id", "group"]:
                file_cache_key += "%s_%s_" % (k, v)
        file_cache_key += "configfile.txt"
        return file_cache_key

    def get(self):
        """采用文件映射内存的方式实现内存缓存，提升IO效率"""
        if not os.path.exists(self.key) or os.path.getsize(self.key) == 0:
            return False

        with open(self.key, "r") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                loc = m.find("\x00".encode("utf-8"))
                data = m[0:loc].rstrip()
                if data:
                    return json.loads(data)
                else:
                    return False

    def set(self, config_values):
        # 创建空映射文件
        if not os.path.exists(self.key):
            with open(self.key, "w") as f:
                f.write("\x00" * MEM_CACHE_SIZE)

        with open(self.key, "r+") as f:
            with mmap.mmap(f.fileno(), MEM_CACHE_SIZE) as m:
                m.seek(0)
                word = json.dumps(config_values)
                word.rjust(MEM_CACHE_SIZE, "\x00")
                m.write(word.encode("utf-8"))
                m.flush()

        return True

    def clear(self):
        pass

    def clear_all(self):
        pass
