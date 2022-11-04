# coding: utf-8

import base64
import hashlib
import hmac
import random
import time


class Signature(object):
    def __init__(self, app_id, user_id, secret_key):
        self.app_id = app_id
        self.user_id = user_id
        self.secret_key = secret_key

    def get_client_header(self, sign_method="sha256"):
        """构造鉴权头部

        请求Header中需添加以下参数： rainbow_sgn_type, rainbow_version, rainbow_app_id, rainbow_user_id,
        rainbow_timestamp, rainbow_nonce, rainbow_sgn_method, rainbow_sgn_body, rainbow_signature

        rainbow_sgn_type	string	签名类型	    该字段为 apisign
        rainbow_version     string	版本号	        暂固定为"2020"
        rainbow_app_id      string	项目ID	        "bf904363-16c6-47f6-85cb-fdcacf288988"
        rainbow_user_id     string	用户ID	        "bx90434316c647f685cbfdcacf286988"，用来标识哪个用户
        rainbow_timestamp	string	当前时间戳	    "1569490800"
        rainbow_nonce	    string	随机正整数	    "3557156860265374221"
        rainbow_sgn_method	string	签名方式	    "sha256"或"sha1"，默认sha1
        rainbow_sgn_body	string	包体签名字符串	"UodgxU3P77iThrEJtsiHi2kjYJmNA2jGEgYNnMD%2FX0s%3D"
        rainbow_signature	string	签名串	        "%2BysXvBSshSbHOsCX2zWBE1tapVs68hi5GLdcQtwBUNk%3D"

        使用以上字段按顺序
        rainbow_version.rainbow_app_id.rainbow_user_id.rainbow_timestamp.rainbow_nonce.rainbow_sgn_method.rainbow_sgn_body
        进行字符串拼接后，在拼接secret_key得到签名串
        使用hash_hmac方法计算 Sha256 哈希值，然后将此哈希使用 base64_encode 进行转码，得到请求头中的 rainbow_signature

        """
        rainbow_version = "2020"
        rainbow_sgn_type = "apisign"
        rainbow_app_id = self.app_id
        rainbow_user_id = self.user_id
        rainbow_timestamp = str(int(time.time()))
        rainbow_nonce = str(random.randint(1000, 99999))
        rainbow_sgn_method = sign_method
        rainbow_sgn_body = ""

        # 字符串拼接顺序: 当前时间戳，token_id, 机器ip, 请求API名称, 随机数
        sign_str = "%s.%s.%s.%s.%s.%s.%s" % (
            rainbow_version,
            rainbow_app_id,
            rainbow_user_id,
            rainbow_timestamp,
            rainbow_nonce,
            rainbow_sgn_method,
            rainbow_sgn_body
        )

        # 使用sha256 算法将拼接字符串通过密钥计算哈希值，并输出原始二进制数据，然后通过base64进行转码得到最终的签名字符串
        # h = hmac.new(self.secret_key, local_sign_str, hashlib.sha256)
        if sign_method == "sha256":
            h = hmac.new(
                bytearray(self.secret_key, "utf-8"),
                bytearray(sign_str, "utf-8"),
                hashlib.sha256,
            )
        else:
            h = hmac.new(
                bytearray(self.secret_key, "utf-8"),
                bytearray(sign_str, "utf-8"),
                hashlib.sha1,
            )
        s = h.digest()
        local_signature = base64.b64encode(s).decode("utf-8")

        header = {
            "rainbow_version": str(rainbow_version),
            "rainbow_sgn_type": str(rainbow_sgn_type),
            "rainbow_app_id": str(rainbow_app_id),
            "rainbow_user_id": str(rainbow_user_id),
            "rainbow_timestamp": rainbow_timestamp,
            "rainbow_nonce": rainbow_nonce,
            "rainbow_sgn_method": rainbow_sgn_method,
            "rainbow_sgn_body": rainbow_sgn_body,
            "rainbow_signature": local_signature,
        }

        return header
