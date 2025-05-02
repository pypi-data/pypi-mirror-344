import hashlib
import hmac
import random
import string
import time
import requests
from typing import Dict, Optional, Union
from datetime import datetime


class WeChatPayV2:

    def __init__(
            self,
            appid: str,
            mch_id: str,
            mch_key: str,
            cert_path: Optional[str] = None,
            key_path: Optional[str] = None,
            notify_url: Optional[str] = None,
            sandbox: bool = False
    ):
        """
        初始化微信支付V2

        :param appid: 应用ID
        :param mch_id: 商户号
        :param mch_key: 商户密钥
        :param cert_path: 证书路径(退款/企业付款需要)
        :param key_path: 证书密钥路径
        :param notify_url: 默认回调地址
        :param sandbox: 是否使用沙箱环境
        """
        self.appid = appid
        self.mch_id = mch_id
        self.mch_key = mch_key
        self.cert_path = cert_path
        self.key_path = key_path
        self.notify_url = notify_url
        self.sandbox = sandbox

        self.base_url = "https://api.mch.weixin.qq.com/sandboxnew" if sandbox else "https://api.mch.weixin.qq.com"

        if sandbox:
            self.mch_key = self._get_sandbox_key()

    def _get_sandbox_key(self) -> str:
        """获取沙箱环境密钥"""
        url = f"{self.base_url}/pay/getsignkey"
        data = {
            "mch_id": self.mch_id,
            "nonce_str": self.generate_nonce_str()
        }
        data["sign"] = self.generate_sign(data)

        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()

        if result.get("return_code") == "SUCCESS":
            return result["sandbox_signkey"]
        raise Exception(f"获取沙箱密钥失败: {result.get('return_msg', '未知错误')}")

    @staticmethod
    def generate_nonce_str(length: int = 32) -> str:
        """生成随机字符串"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_sign(self, data: Dict, sign_type: str = "MD5") -> str:
        """生成签名"""
        # 过滤空值和sign字段
        filtered_data = {k: v for k, v in data.items()
                         if v is not None and v != "" and k != "sign"}

        # 参数名ASCII码从小到大排序
        sorted_data = sorted(filtered_data.items(), key=lambda x: x[0])

        # 拼接成URL参数格式
        str_to_sign = "&".join([f"{k}={v}" for k, v in sorted_data])
        str_to_sign += f"&key={self.mch_key}"

        # 计算签名
        if sign_type == "MD5":
            return hashlib.md5(str_to_sign.encode('utf-8')).hexdigest().upper()
        elif sign_type == "HMAC-SHA256":
            return hmac.new(
                self.mch_key.encode('utf-8'),
                str_to_sign.encode('utf-8'),
                hashlib.sha256
            ).hexdigest().upper()
        raise ValueError(f"不支持的签名类型: {sign_type}")

    def _request(self, endpoint: str, data: Dict, use_cert: bool = False) -> Dict:
        """发送请求到微信支付API"""
        url = f"{self.base_url}{endpoint}"

        # 添加公共参数
        data.setdefault("appid", self.appid)
        data.setdefault("mch_id", self.mch_id)
        data.setdefault("nonce_str", self.generate_nonce_str())

        # 生成签名
        data["sign"] = self.generate_sign(data)

        # 转换为XML
        xml_data = self._dict_to_xml(data)

        # 发送请求
        kwargs = {}
        if use_cert and self.cert_path and self.key_path:
            kwargs["cert"] = (self.cert_path, self.key_path)

        headers = {"Content-Type": "application/xml"}
        response = requests.post(url, data=xml_data, headers=headers, **kwargs)
        response.raise_for_status()

        # 解析XML响应
        return self._xml_to_dict(response.text)

    @staticmethod
    def _dict_to_xml(data: Dict) -> str:
        """字典转XML"""
        xml = ["<xml>"]
        for k, v in data.items():
            if v is None:
                continue
            xml.append(f"<{k}>{v}</{k}>")
        xml.append("</xml>")
        return "".join(xml)

    @staticmethod
    def _xml_to_dict(xml: str) -> Dict:
        """XML转字典"""
        try:
            from xml.etree import ElementTree as ET
        except ImportError:
            raise ImportError("需要安装ElementTree来解析XML响应")

        result = {}
        root = ET.fromstring(xml)
        for child in root:
            result[child.tag] = child.text
        return result

    def verify_notify_sign(self, data: Dict) -> bool:
        """验证回调签名"""
        if "sign" not in data:
            return False

        sign = data.pop("sign")
        calculated_sign = self.generate_sign(data)
        return sign == calculated_sign

    # ============= 支付功能 =============
    def unified_order(
            self,
            out_trade_no: str,
            total_fee: int,
            trade_type: str,
            body: str,
            notify_url: Optional[str] = None,
            client_ip: Optional[str] = None,
            openid: Optional[str] = None,
            product_id: Optional[str] = None,
            time_expire: Optional[Union[str, datetime]] = None,
            attach: Optional[str] = None,
            **kwargs
    ) -> Dict:
        """
        统一下单

        :param out_trade_no: 商户订单号
        :param total_fee: 订单金额(分)
        :param trade_type: 交易类型(JSAPI, NATIVE, APP, MWEB)
        :param body: 商品描述
        :param notify_url: 回调地址
        :param client_ip: 终端IP
        :param openid: 用户标识(JSAPI需要)
        :param product_id: 商品ID(NATIVE需要)
        :param time_expire: 过期时间
        :param attach: 附加数据
        :return: 统一下单结果
        """
        if trade_type not in ["JSAPI", "NATIVE", "APP", "MWEB"]:
            raise ValueError("无效的交易类型")

        data = {
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "trade_type": trade_type,
            "body": body,
            "notify_url": notify_url or self.notify_url,
            "spbill_create_ip": client_ip or "127.0.0.1",
            "openid": openid,
            "product_id": product_id,
            "attach": attach,
            **kwargs
        }

        if time_expire:
            if isinstance(time_expire, datetime):
                time_expire = time_expire.strftime("%Y%m%d%H%M%S")
            data["time_expire"] = time_expire

        return self._request("/pay/unifiedorder", data)

    def get_jsapi_params(self, prepay_id: str) -> Dict:
        """获取JSAPI支付参数"""
        params = {
            "appId": self.appid,
            "timeStamp": str(int(time.time())),
            "nonceStr": self.generate_nonce_str(),
            "package": f"prepay_id={prepay_id}",
            "signType": "MD5"
        }
        params["paySign"] = self.generate_sign(params)
        return params

    def get_app_params(self, prepay_id: str) -> Dict:
        """获取APP支付参数"""
        params = {
            "appid": self.appid,
            "partnerid": self.mch_id,
            "prepayid": prepay_id,
            "package": "Sign=WXPay",
            "noncestr": self.generate_nonce_str(),
            "timestamp": str(int(time.time()))
        }
        params["sign"] = self.generate_sign(params)
        return params

    # ============= 订单操作 =============
    def query_order(
            self,
            transaction_id: Optional[str] = None,
            out_trade_no: Optional[str] = None
    ) -> Dict:
        """
        查询订单

        :param transaction_id: 微信订单号
        :param out_trade_no: 商户订单号
        :return: 订单查询结果
        """
        if not transaction_id and not out_trade_no:
            raise ValueError("至少需要一个订单标识")

        data = {
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no
        }
        return self._request("/pay/orderquery", data)

    def close_order(self, out_trade_no: str) -> Dict:
        """
        关闭订单

        :param out_trade_no: 商户订单号
        :return: 关闭结果
        """
        data = {"out_trade_no": out_trade_no}
        return self._request("/pay/closeorder", data)

    # ============= 退款功能 =============
    def refund(
            self,
            out_refund_no: str,
            total_fee: int,
            refund_fee: int,
            transaction_id: Optional[str] = None,
            out_trade_no: Optional[str] = None,
            notify_url: Optional[str] = None,
            **kwargs
    ) -> Dict:
        """
        申请退款

        :param out_refund_no: 商户退款单号
        :param total_fee: 订单金额(分)
        :param refund_fee: 退款金额(分)
        :param transaction_id: 微信订单号
        :param out_trade_no: 商户订单号
        :param notify_url: 退款通知地址
        :return: 退款结果
        """
        if not transaction_id and not out_trade_no:
            raise ValueError("至少需要一个订单标识")

        if not self.cert_path or not self.key_path:
            raise ValueError("退款需要证书文件")

        data = {
            "out_refund_no": out_refund_no,
            "total_fee": total_fee,
            "refund_fee": refund_fee,
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no,
            "notify_url": notify_url or self.notify_url,
            **kwargs
        }
        return self._request("/secapi/pay/refund", data, use_cert=True)

    def query_refund(
            self,
            transaction_id: Optional[str] = None,
            out_trade_no: Optional[str] = None,
            out_refund_no: Optional[str] = None,
            refund_id: Optional[str] = None
    ) -> Dict:
        """
        查询退款

        :param transaction_id: 微信订单号
        :param out_trade_no: 商户订单号
        :param out_refund_no: 商户退款单号
        :param refund_id: 微信退款单号
        :return: 退款查询结果
        """
        if not any([transaction_id, out_trade_no, out_refund_no, refund_id]):
            raise ValueError("至少需要一个查询参数")

        data = {
            "transaction_id": transaction_id,
            "out_trade_no": out_trade_no,
            "out_refund_no": out_refund_no,
            "refund_id": refund_id
        }
        return self._request("/pay/refundquery", data)

    # ============= 企业付款 =============
    def transfer_to_balance(
            self,
            partner_trade_no: str,
            openid: str,
            amount: int,
            desc: str,
            check_name: str = "NO_CHECK",
            re_user_name: Optional[str] = None,
            device_info: Optional[str] = None
    ) -> Dict:
        """
        企业付款到零钱

        :param partner_trade_no: 商户订单号
        :param openid: 用户openid
        :param amount: 付款金额(分)
        :param desc: 付款说明
        :param check_name: 校验用户姓名选项(NO_CHECK, FORCE_CHECK)
        :param re_user_name: 收款用户姓名
        :param device_info: 设备号
        :return: 付款结果
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("企业付款需要证书文件")

        if check_name == "FORCE_CHECK" and not re_user_name:
            raise ValueError("强制校验姓名时需要提供收款人姓名")

        data = {
            "partner_trade_no": partner_trade_no,
            "openid": openid,
            "amount": amount,
            "desc": desc,
            "check_name": check_name,
            "re_user_name": re_user_name,
            "device_info": device_info
        }
        return self._request("/mmpaymkttransfers/promotion/transfers", data, use_cert=True)

    def query_transfer(
            self,
            partner_trade_no: str
    ) -> Dict:
        """
        查询企业付款

        :param partner_trade_no: 商户订单号
        :return: 查询结果
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("查询企业付款需要证书文件")

        data = {
            "partner_trade_no": partner_trade_no,
            "appid": self.appid,
            "mch_id": self.mch_id
        }
        return self._request("/mmpaymkttransfers/gettransferinfo", data, use_cert=True)

    # ============= 账单功能 =============
    def download_bill(
            self,
            bill_date: str,
            bill_type: str = "ALL",
            tar_type: str = "GZIP"
    ) -> str:
        """
        下载对账单

        :param bill_date: 账单日期(格式: 20140603)
        :param bill_type: 账单类型(ALL, SUCCESS, REFUND)
        :param tar_type: 压缩类型(GZIP)
        :return: 账单数据
        """
        data = {
            "bill_date": bill_date,
            "bill_type": bill_type,
            "tar_type": tar_type
        }
        response = self._request("/pay/downloadbill", data)
        return response.get("data", "")

    def download_fund_flow(
            self,
            bill_date: str,
            account_type: str = "Basic",
            tar_type: str = "GZIP"
    ) -> str:
        """
        下载资金账单

        :param bill_date: 账单日期(格式: 20140603)
        :param account_type: 账户类型(Basic, Operation, Fees)
        :param tar_type: 压缩类型(GZIP)
        :return: 账单数据
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("下载资金账单需要证书文件")

        data = {
            "bill_date": bill_date,
            "account_type": account_type,
            "tar_type": tar_type
        }
        response = self._request("/pay/downloadfundflow", data, use_cert=True)
        return response.get("data", "")

    # ============= 短链接转换 =============
    def short_url(self, long_url: str) -> Dict:
        """
        长链接转短链接

        :param long_url: 长链接
        :return: 转换结果
        """
        data = {
            "long_url": long_url
        }
        return self._request("/tools/shorturl", data)

    def native_pay(
            self,
            out_trade_no: str,
            total_fee: int,
            body: str,
            product_id: str,
            notify_url: Optional[str] = None,
            attach: Optional[str] = None,
            time_expire: Optional[Union[str, datetime]] = None,
            **kwargs
    ) -> Dict:
        """
        扫码支付(Native支付)

        :param out_trade_no: 商户订单号
        :param total_fee: 订单金额(分)
        :param body: 商品描述
        :param product_id: 商品ID(商户自定义)
        :param notify_url: 回调地址
        :param attach: 附加数据
        :param time_expire: 过期时间
        :return: 包含code_url的字典，用于生成支付二维码
        """
        return self.unified_order(
            out_trade_no=out_trade_no,
            total_fee=total_fee,
            trade_type="NATIVE",
            body=body,
            product_id=product_id,
            notify_url=notify_url,
            attach=attach,
            time_expire=time_expire,
            **kwargs
        )

    def generate_qrcode(self, code_url: str, save_path: Optional[str] = None) -> Optional[bytes]:
        """
        生成支付二维码图片

        :param code_url: 从native_pay获取的code_url
        :param save_path: 如需保存到文件，指定路径
        :return: 二维码图片二进制数据(如不保存到文件)
        """
        try:
            import qrcode
        except ImportError:
            raise ImportError("生成二维码需要安装qrcode库: pip install qrcode")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        if save_path:
            img.save(save_path)
            return None
        else:
            from io import BytesIO
            buf = BytesIO()
            img.save(buf)
            return buf.getvalue()

    def native_pay_callback_handler(self, xml_data: str) -> Dict:
        """
        处理扫码支付回调

        :param xml_data: 微信回调的XML数据
        :return: 处理结果字典
        """
        # 解析XML数据
        callback_data = self._xml_to_dict(xml_data)

        # 验证签名
        if not self.verify_notify_sign(callback_data):
            return {
                "return_code": "FAIL",
                "return_msg": "签名验证失败"
            }

        # 检查支付结果
        if callback_data.get("return_code") != "SUCCESS":
            return {
                "return_code": "FAIL",
                "return_msg": callback_data.get("return_msg", "支付失败")
            }

        # 检查业务结果
        if callback_data.get("result_code") != "SUCCESS":
            return {
                "return_code": "FAIL",
                "return_msg": callback_data.get("err_code_des", "业务处理失败")
            }

        # 支付成功，处理业务逻辑
        out_trade_no = callback_data["out_trade_no"]
        transaction_id = callback_data["transaction_id"]
        total_fee = int(callback_data["total_fee"])

        # TODO: 这里添加你的业务处理逻辑
        # 例如更新订单状态、记录支付信息等

        return {
            "return_code": "SUCCESS",
            "return_msg": "OK"
        }
