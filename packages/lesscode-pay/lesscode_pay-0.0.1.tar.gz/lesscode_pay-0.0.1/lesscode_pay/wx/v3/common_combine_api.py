import json

import requests

from lesscode_pay.wx.v3.common_api import CommonApi


class CommonCombineApi(CommonApi):
    def query_combine_trade(self, combine_out_trade_no: str):
        """
            【合单查询订单】
            合单支付下单成功后，合单发起方可调用该接口查询合单订单的交易状态。
            支持商户：【普通商户】
            :param combine_out_trade_no:【合单商户订单号】下单时传入的合单商户订单号
        """
        uri = f"/v3/combine-transactions/out-trade-no/{combine_out_trade_no}"
        url = f"{self.base_url}{uri}"
        auth_header = self.generate_signature(method="GET", uri=uri, body="")
        headers = {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def close_combine_trade(self, combine_out_trade_no: str, combine_appid: str, sub_orders: list):
        """
        【关闭合单订单】
        未支付状态的订单，合单发起方商户可在无需支付时调用此接口关闭订单。常见关单情况包括：
            用户在商户系统提交取消订单请求，商户需执行关单操作。
            订单超时未支付（超出商户系统设定的可支付时间或下单时的time_expire支付截止时间），商户需进行关单处理。
            注意
                此接口只能整单关闭，不支持关闭部分子单，关单的合单发起方商户号、合单商户订单号、子单个数、子单商户号、子单商户订单号必须与下单时传入的完全一致。
        :param combine_out_trade_no:
        :param combine_appid: 【合单商户公众账号ID】合单下单时传入的combine_appid。
        :param sub_orders: 【子单信息列表】合单下单时传入的子单信息列表。
                    mchid 　必填 string 【子单商户号】合单下单时传入的子单商户号。
                    out_trade_no 　必填 string  【子单商户订单号】合单下单时传入的子单商户订单号。
        :return:
        """
        uri = f"/v3/combine-transactions/out-trade-no/{combine_out_trade_no}/close"
        url = f"{self.base_url}{uri}"

        # 请求体（参考微信支付文档）
        data = {
            "combine_appid": combine_appid,
            "sub_orders": sub_orders,
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
