import base64
import hashlib
import json
import time
from urllib.parse import quote, urlparse

import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


class CommonApi:

    def __init__(self, cert_private_key: str, cert_serial_no: str, mchid: str,
                 base_url: str = "https://api.mch.weixin.qq.com"):
        self.base_url = base_url
        self.cert_private_key = cert_private_key
        self.cert_serial_no = cert_serial_no
        self.mchid = mchid

    def generate_signature(self, method: str, uri: str, body: str):
        """生成微信支付V3签名"""
        timestamp = str(int(time.time()))
        nonce = hashlib.md5(timestamp.encode()).hexdigest()

        # 构造签名串
        message = f"{method}\n{uri}\n{timestamp}\n{nonce}\n{body}\n"

        # 使用私钥签名
        private_key = serialization.load_pem_private_key(
            self.cert_private_key.encode(),
            password=None
        )
        signature = private_key.sign(
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        signature_base64 = base64.b64encode(signature).decode()
        """

        Authorization: WECHATPAY2-SHA256-RSA2048 mchid="1900007291",nonce_str="593BEC0C930BF1AFEB40B4A08C8FB242",signature="gEuexJ547PHFV77TQ6eiE4tphVYfWfUe1Wc2dBmVnoMYU2rl/M4zhw+b3vBhuMw6AC7pteNkryLA7UWU2h+umo0OdSuuLm1++O3NckQPCSfm6dypsjn4GYm84KMqXWFrhFmyxEwIdEJDr3w1UYfxOcu55OQupfLkrt/ZzuOspnliJFrPzGQFUk7lGqMMtpz3EfbDUNxnVsHblORg3hVmuYNmbGWnS2ovU30Y2Q+iKFDxzkaXBk8LTy6HzvxizRo6Q+J4SVM7O0hKXfgo1QdI68kpzNULb3EVBXlhTyPUzhkHzzLxECL1qHl3HH2hEv8++C+4wBlsagF3j/O6PABojA==",timestamp="1554208460",serial_no="408B07E79B8269FEC3D5D3E6AB8ED163A6A380DB"
        """

        return f'WECHATPAY2-SHA256-RSA2048 mchid="{self.mchid}",nonce_str="{nonce}",timestamp="{timestamp}",serial_no="{self.cert_serial_no}",signature="{signature_base64}"'

    def query_order(self, transaction_id: str):
        """
            【微信支付订单号查询订单】
            订单支付成功后，商户可通过微信交易订单号或使用商户订单号查询订单；若订单未支付，则只能使用商户订单号查询订单。
            支持商户：【普通商户】
            :param transaction_id:【微信支付订单号】 微信支付侧订单的唯一标识，订单支付成功后，支付成功回调通知和商户订单号查询订单会返回该参数。

        """

        params = {"mchid": self.mchid}
        params_str = "&".join([f"{k}={quote(v)}" if isinstance(v, str) else v for k, v in params.items()])
        uri = f"/v3/pay/transactions/id/{transaction_id}?{params_str}"
        url = f"{self.base_url}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def query_trade(self, out_trade_no: str):
        """
            【商户订单号查询订单】
            订单支付成功后，商户可使用微信订单号查询订单或商户订单号查询订单；若订单未支付，则只能使用商户订单号查询订单。
            支持商户：【普通商户】
            :param out_trade_no:【商户订单号】 商户下单时传入的商户系统内部订单号。

        """

        params = {"mchid": self.mchid}
        params_str = "&".join([f"{k}={quote(v)}" if isinstance(v, str) else v for k, v in params.items()])
        uri = f"/v3/pay/transactions/out-trade-no/{out_trade_no}?{params_str}"
        url = f"{self.base_url}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def close_trade(self, out_trade_no: str):
        """
            【关闭订单】
                未支付状态的订单，可在无需支付时调用此接口关闭订单。常见关单情况包括：
                    用户在商户系统提交取消订单请求，商户需执行关单操作。
                    订单超时未支付（超出商户系统设定的可支付时间或下单时的time_expire支付截止时间），商户需进行关单处理。
            支持商户：【普通商户】
            :param out_trade_no:【商户订单号】 商户下单时传入的商户系统内部订单号。
        """
        uri = f"/v3/pay/transactions/out-trade-no/{out_trade_no}/close"
        url = f"{self.base_url}{uri}"

        # 请求体（参考微信支付文档）
        data = {
            "mchid": self.mchid
        }
        body = json.dumps(data, ensure_ascii=False)

        # 生成签名
        auth_header = self.generate_signature(method="POST", uri=uri, body=body)

        # 发送请求
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=body.encode('utf-8'))
        return response

    def create_refunds(self, out_refund_no: str, amount: dict,
                       transaction_id: str = None,
                       out_trade_no: str = None, reason: str = None, notify_url: str = None,
                       funds_account: str = None,
                       goods_detail: list = None, ):
        """
            【退款申请】
            :param out_refund_no:
            :param amount:
            :param transaction_id:
            :param out_trade_no:
            :param reason:
            :param notify_url:
            :param funds_account:
            :param goods_detail:
            :return:
        """
        uri = f"/v3/refund/domestic/refunds"
        url = f"{self.base_url}{uri}"

        # 请求体（参考微信支付文档）
        data = {
            "out_refund_no": out_refund_no,
            "amount": amount
        }
        if transaction_id:
            data["transaction_id"] = transaction_id
        if out_trade_no:
            data["out_trade_no"] = out_trade_no
        if reason:
            data["reason"] = reason
        if notify_url:
            data["notify_url"] = notify_url
        if funds_account:
            data["funds_account"] = funds_account
        if goods_detail:
            data["goods_detail"] = goods_detail
        body = json.dumps(data, ensure_ascii=False)

        # 生成签名
        auth_header = self.generate_signature(method="POST", uri=uri, body=body)

        # 发送请求
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=body.encode('utf-8'))
        return response.json()

    def query_refunds(self, out_refund_no: str):
        """
            【查询单笔退款（通过商户退款单号）】
                提交退款申请后，推荐每间隔1分钟调用该接口查询一次退款状态，若超过5分钟仍是退款处理中状态，建议开始逐步衰减查询频率(比如之后间隔5分钟、10分钟、20分钟、30分钟……查询一次)。
                    退款有一定延时，零钱支付的订单退款一般5分钟内到账，银行卡支付的订单退款一般1-3个工作日到账。
                    同一商户号查询退款频率限制为300qps，如返回FREQUENCY_LIMITED频率限制报错可间隔1分钟再重试查询。
            支持商户：【普通商户】
            :param out_refund_no:
        """
        uri = f"/v3/refund/domestic/refunds/{out_refund_no}"
        url = f"{self.base_url}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def apply_abnormal_refund(self, refund_id: str, out_refund_no: str, type: str, bank_type: str = None,
                              bank_account: str = None, real_name: str = None):
        """
        【发起异常退款】
            提交退款申请后，退款结果通知或查询退款确认状态为退款异常，可调用此接口发起异常退款处理。支持退款至用户、退款至交易商户银行账户两种处理方式。
            注意：
                退款至用户时，仅支持以下银行的借记卡：招行、交通银行、农行、建行、工商、中行、平安、浦发、中信、光大、民生、兴业、广发、邮储、宁波银行。
                请求频率限制：150qps，即每秒钟正常的申请退款请求次数不超过150次
        :param refund_id:
        :param out_refund_no:
        :param type:
        :param bank_type:
        :param bank_account:
        :param real_name:
        :return:
        """
        uri = f"/v3/refund/domestic/refunds/{refund_id}/apply-abnormal-refund"
        url = f"{self.base_url}{uri}"

        # 请求体（参考微信支付文档）
        data = {
            "out_refund_no": out_refund_no,
            "type": type
        }
        if bank_type:
            data["bank_type"] = bank_type
        if bank_account:
            data["bank_account"] = bank_account
        if real_name:
            data["real_name"] = real_name
        body = json.dumps(data, ensure_ascii=False)

        # 生成签名
        auth_header = self.generate_signature(method="POST", uri=uri, body=body)

        # 发送请求
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=body.encode('utf-8'))
        return response.json()

    def trade_bill(self, bill_date: str, bill_type: str = None,
                   tar_type: str = None):
        """
            【申请交易账单】
            微信支付在每日10点后生成昨日交易账单文件，商户可通过接口获取账单下载链接。账单包含交易金额、时间及营销信息，利于订单核对、退款审查及银行到账确认。详细介绍参考：下载账单-产品介绍。
                注意：
                    仅支付成功的订单包含在账单内。
                    账单金额单位为人民币“元”。
                    此接口仅可下载三个月内的账单。
            支持商户：【普通商户】
            :param bill_date:
            :param bill_type:
            :param tar_type:
        """
        params = {"bill_date": bill_date}
        if bill_type:
            params["bill_type"] = bill_type
        if tar_type:
            params["tar_type"] = tar_type
        params_str = "&".join([f"{k}={quote(v)}" if isinstance(v, str) else v for k, v in params.items()])
        uri = f"/v3/bill/tradebill?{params_str}"
        url = f"{self.base_url}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def fund_flow_bill(self, bill_date: str, tar_type: str = None, account_type: str = None, ):
        """
            【申请资金账单】
            下载接口说明
                微信支付按天提供商户各账户的资金流水账单文件，商户可以通过该接口获取账单文件的下载地址。账单文件详细记录了账户资金操作的相关信息，包括业务单号、收支金额及记账时间等，以便商户进行核对与确认。详细介绍参考：下载账单-产品介绍。
                注意：
                    资金账单中的数据反映的是商户微信账户资金变动情况；
                    当日账单将在次日上午9点开始生成，建议商户在次日上午10点以后获取；
                    资金账单中所有涉及金额的字段均以“元”为单位。
                文件格式说明
                    账单文件主要由明细数据和汇总数据两大部分构成，每部分均包含一行表头以及多行详细数据。
                    明细数据的每一行都代表一笔具体的资金操作。为防止数据在Excel中被自动转换为科学计数法，每项数据前均添加了字符`。若需汇总计算金额等数据，可以批量移除该字符。
            :param bill_date:
            :param tar_type:
            :param account_type:
            :return:
        """

        params = {"bill_date": bill_date}
        if account_type:
            params["account_type"] = account_type
        if tar_type:
            params["tar_type"] = tar_type
        params_str = "&".join([f"{k}={quote(v)}" if isinstance(v, str) else v for k, v in params.items()])
        uri = f"/v3/bill/fundflowbill?{params_str}"
        url = f"{self.base_url}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def download_bill(self, download_url: str):
        url_info = urlparse(download_url)
        uri = f"{url_info.path}?{url_info.query}"
        url = f"{url_info.scheme}://{url_info.netloc}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response
