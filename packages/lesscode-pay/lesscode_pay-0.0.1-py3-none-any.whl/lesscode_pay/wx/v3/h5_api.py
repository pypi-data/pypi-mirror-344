import json

import requests

from lesscode_pay.wx.v3.common_api import CommonApi


class H5Api(CommonApi):
    def create_order(self, appid: str, description: str, out_trade_no: str, notify_url: str,
                     amount: dict,
                     payer: dict,time_expire: str = None,
                     attach: str = None, goods_tag: str = None, support_fapiao: bool = False,
                     detail: dict = None,
                     scene_info: dict = None, settle_info: dict = None):
        """
            【H5下单】
            支持商户：【普通商户】
            :param settle_info: 【结算信息】 结算信息
                profit_sharing 　选填 boolean 【分账标识】订单的分账标识在下单时设置，传入true表示在订单支付成功后可进行分账操作。以下是详细说明：
                    需要分账（传入true）：
                        订单收款成功后，资金将被冻结并转入基本账户的不可用余额。商户可通过请求分账API，将收款资金分配给其他商户或用户。完成分账操作后，可通过接口解冻剩余资金，或在支付成功30天后自动解冻。
                    不需要分账（传入false或不传，默认为false）：
                        订单收款成功后，资金不会被冻结，而是直接转入基本账户的可用余额。

            :param scene_info: 【场景信息】 场景信息
                payer_client_ip 　必填 string(45) 【用户终端IP】 用户的客户端IP，支持IPv4和IPv6两种格式的IP地址。
                device_id 　选填 string(32) 【商户端设备号】 商户端设备号（门店号或收银设备ID）。
                store_info 　选填 object  【商户门店信息】 商户门店信息
                    id 　必填 string(32) 【门店编号】商户侧门店编号，总长度不超过32字符，由商户自定义。
                    name 　选填 string(256) 【门店名称】 商户侧门店名称，由商户自定义。
                    area_code 　选填 string(32) 【地区编码】 地区编码，详细请见省市区编号对照表。
                    address 　选填 string(512) 【详细地址】 详细的商户门店地址，由商户自定义。

            :param detail: 【优惠功能】 优惠功能
                cost_price 　选填 integer 【订单原价】
                    1、商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。
                    2、当订单原价与支付金额不相等，则不享受优惠。
                    3、该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。
                invoice_id 　选填 string(32) 【商品小票ID】 商家小票ID
                goods_detail 　 选填 array[object] 【单品列表】 单品列表信息
                    条目个数限制：【1，6000】
                    merchant_goods_id 　必填 string(32) 【商户侧商品编码】 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成。
                    wechatpay_goods_id 　选填 string(32) 【微信支付商品编码】 微信支付定义的统一商品编号（没有可不传）
                    goods_name 　选填 string(256) 【商品名称】 商品的实际名称
                    quantity 　必填 integer 【商品数量】 用户购买的数量
                    unit_price 　必填 integer 【商品单价】整型，单位为：分。如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50)

            :param payer: 【支付者信息】支付者信息
                openid 　必填 string(128) 【用户标识】用户在商户appid下的唯一标识。下单前需获取到用户的OpenID，详见OpenID获取。

            :param amount:【订单金额】订单金额信息
                total 　必填 integer 总金额】 订单总金额，单位为分，整型。
                    示例：1元应填写 100
                currency 　选填 string(16) 【货币类型】符合ISO 4217标准的三位字母代码，固定传：CNY，代表人民币。

            :param support_fapiao: 【电子发票入口开放标识】 传入true时，支付成功消息和支付详情页将出现开票入口。需要在微信支付商户平台或微信公众平台开通电子发票功能，传此字段才可生效

            :param goods_tag: 【订单优惠标记】代金券在创建时可以配置多个订单优惠标记，标记的内容由创券商户自定义设置。详细参考：创建代金券批次API。如果代金券有配置订单优惠标记，则必须在该参数传任意一个配置的订单优惠标记才能使用券。如果代金券没有配置订单优惠标记，则可以不传该参数。
                示例：如有两个活动，活动A设置了两个优惠标记：WXG1、WXG2；活动B设置了两个优惠标记：WXG1、WXG3；下单时优惠标记传WXG2，则订单参与活动A的优惠；下单时优惠标记传WXG3，则订单参与活动B的优惠；下单时优惠标记传共同的WXG1，则订单参与活动A、B两个活动的优惠；

            :param notify_url: 【商户回调地址】商户接收支付成功回调通知的地址，需按照notify_url填写注意事项规范填写

            :param attach:【商户数据包】商户在创建订单时可传入自定义数据包，该数据对用户不可见，用于存储订单相关的商户自定义信息，其总长度限制在128字符以内。支付成功后查询订单API和支付成功回调通知均会将此字段返回给商户，并且该字段还会体现在交易账单。

            :param time_expire: 【支付结束时间】
                1、定义：支付结束时间是指用户能够完成该笔订单支付的最后时限，并非订单关闭的时间。超过此时间后，用户将无法对该笔订单进行支付。如需关闭订单，请调用关闭订单API接口。
                2、格式要求：支付结束时间需遵循rfc3339标准格式：yyyy-MM-DDTHH:mm:ss+TIMEZONE。yyyy-MM-DD 表示年月日；T 字符用于分隔日期和时间部分；HH:mm:ss 表示具体的时分秒；TIMEZONE 表示时区（例如，+08:00 对应东八区时间，即北京时间）。
                    示例：2015-05-20T13:29:35+08:00 表示北京时间2015年5月20日13点29分35秒。
                3、注意事项：
                    time_expire 参数仅在用户首次下单时可设置，且不允许后续修改，尝试修改将导致错误。
                    若用户实际进行支付的时间超过了订单设置的支付结束时间，商户需使用新的商户订单号下单，生成新的订单供用户进行支付。若未超过支付结束时间，则可使用原参数重新请求下单接口，以获取当前订单最新的prepay_id 进行支付。
                    支付结束时间不能早于下单时间后1分钟，若设置的支付结束时间早于该时间，系统将自动调整为下单时间后1分钟作为支付结束时间。

            :param out_trade_no:【商户订单号】商户系统内部订单号，要求6-32个字符内，只能是数字、大小写字母_-|* 且在同一个商户号下唯一。

            :param description:【商品描述】商品信息描述，用户微信账单的商品字段中可见(可参考JSAPI支付示例说明-账单示意图)，商户需传递能真实代表商品信息的描述，不能超过127个字符

            :param mchid: 【商户号】是由微信支付系统生成并分配给每个商户的唯一标识符，商户号获取方式请参考普通商户模式开发必要参数说明

            :param appid:【公众账号ID】是商户在微信开放平台（移动应用）或公众平台（公众号/小程序）上申请的一个唯一标识。需确保该appid与mchid有绑定关系

            :return:
                prepay_id  string(64) 【预支付交易会话标识】预支付交易会话标识，JSAPI或小程序调起支付时需要使用的参数，有效期为2小时，失效后需要重新请求该接口以获取新的prepay_id。
                {
                  "prepay_id" : "wx201410272009395522657a690389285100"
                }
        """
        uri = "/v3/pay/transactions/h5"
        url = f"{self.base_url}{uri}"

        # 请求体（参考微信支付文档）
        data = {
            "appid": appid,
            "mchid": self.mchid,
            "description": description,
            "out_trade_no": out_trade_no,
            "notify_url": notify_url,
            "amount": amount,
            "payer": payer
        }
        if time_expire:
            data["time_expire"] = time_expire
        if attach:
            data["attach"] = attach
        if goods_tag:
            data["goods_tag"] = goods_tag
        if support_fapiao:
            data["support_fapiao"] = support_fapiao
        if detail:
            data["detail"] = detail
        if scene_info:
            data["scene_info"] = scene_info
        if settle_info:
            data["settle_info"] = settle_info
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

    def create_combine_order(self, combine_appid: str, combine_out_trade_no: str, sub_orders: list,
                             notify_url: str,  scene_info: dict = None,
                             combine_payer_info: dict = None, time_expire: str = None):
        """
            【H5合单下单】
            用户在商户H5页面选择微信支付后，商户需调用该接口在微信支付下单，生成用于调起支付的H5支付链接(h5_url)。
            注意
                普通商户模式只支持2-10笔订单进行合单支付。
            :param combine_appid: 【合单商户应用ID】合单发起方的APPID。APPID是微信开放平台(移动应用)或微信公众平台(小程序、公众号)为开发者的应用程序提供的唯一标识。此处请填写移动应用类型的APPID，并确保该combine_appid与combine_mchid有绑定关系。详见：商户号绑定APPID账号操作指南。
            :param combine_out_trade_no:【合单商户订单号】合单发起方商户系统内部订单号，要求6~32个字符内，只能是数字、大小写字母_-|*，且在同一个合单商户号下唯一。
            :param sub_orders: 【子单信息列表】 合单支付的子单信息列表，一笔合单支付订单可支持2-10笔子单交易。
                        mchid 　必填 string(32) 【子单商户号】子单参与方的商户号，必须与combine_appid有绑定关系。详见：商户号绑定APPID账号操作指南。
                        attach 　必填 string(128) 【商户数据包】商户在创建订单时可传入自定义数据包，该数据对用户不可见，用于存储订单相关的商户自定义信息，其总长度限制在128字符以内。支付成功后查询合单订单API和合单订单支付成功回调通知均会将此字段返回给商户，并且该字段还会体现在交易账单。
                        amount 　必填 object 【子单金额信息】 子订单收款金额信息。
                            total_amount 　必填 integer 【标价金额】 子单的金额，整型，单位为分。子单商户号为境外商户时，标价金额必需超过商户结算币种的最小单位金额，例如商户结算币种为美元，则标价金额必须大于1美分。
                            currency 　必填 string(8) 【标价币种】标价金额的币种，符合ISO 4217标准的三位字母代码，境内商户固定传入：CNY，代表人民币。
                        out_trade_no 　必填 string(32) 【子单商户订单号】 合单发起方商户系统内部订单号，要求6~32个字符内，只能是数字、大小写字母_-|*，且在同一个合单商户号下唯一。
                        detail 　选填 string(6000) 【商品详情】 对订单商品的详细描述。
                        description 　必填 string(127) 【商品描述】商品信息描述，用户微信账单的商品字段中可见(可参考APP合单支付模式介绍-6、账单示意图)，商户需传递能真实代表商品信息的描述，不能超过127个字符。
                        settle_info 　选填 object 结算信息】 结算信息
                            profit_sharing 　选填 boolean 【分账标识】订单的分账标识在下单时设置，传入true表示在订单支付成功后可进行分账操作。以下是详细说明：
                                需要分账（传入true）：
                                    订单收款成功后，资金将被冻结并转入基本账户的不可用余额。商户可通过请求分账API，将收款资金分配给其他商户或用户。完成分账操作后，可通过接口解冻剩余资金，或在支付成功30天后自动解冻。
                                不需要分账（传入false或不传，默认为false）：
                                    订单收款成功后，资金不会被冻结，而是直接转入基本账户的可用余额。
                        goods_tag 　选填 string(32) 【订单优惠标记】代金券在创建时可以配置多个订单优惠标记，标记的内容由创券商户自定义设置。详细参考：创建代金券批次API。
                            如果代金券有配置订单优惠标记，则必须在该参数传任意一个配置的订单优惠标记才能使用券。
                            如果代金券没有配置订单优惠标记，则可以不传该参数。
                            示例：
                                如有两个活动，活动A设置了两个优惠标记：WXG1、WXG2；活动B设置了两个优惠标记：WXG1、WXG3；
                                下单时优惠标记传WXG2，则订单参与活动A的优惠；
                                下单时优惠标记传WXG3，则订单参与活动B的优惠；
                                下单时优惠标记传共同的WXG1，则订单参与活动A、B两个活动的优惠；
            :param notify_url: 【商户回调地址】商户接收合单订单支付成功回调通知的地址，需按照notify_url填写注意事项规范填写
            :param scene_info: 【场景信息】场景信息
                        device_id 　选填 string(16) 【商户端设备号】 终端设备号(门店号或收银设备ID)
                        payer_client_ip 　必填 string(45) 【用户终端IP】用户端实际IP，支持IPv4和IPv6两种格式的IP地址。IP获取请参考获取用户IP指引
            :param combine_payer_info: 选填 object 【合单支付者信息】 合单支付者信息。
                        openid 　选填 string(128) 【用户标识】用户在合单商户号的combine_appid下的唯一标识。下单前需获取到用户的OpenID，详见OpenID获取。
            :param time_expire: 【支付结束时间】
                    1、定义：支付结束时间是指用户能够完成该笔订单支付的最后时限，并非订单关闭的时间。超过此时间后，用户将无法对该笔订单进行支付。如需关闭订单，请调用关闭合单订单API接口。
                    2、格式要求：支付结束时间需遵循rfc3339标准格式：yyyy-MM-DDTHH:mm:ss+TIMEZONE。yyyy-MM-DD 表示年月日；T 字符用于分隔日期和时间部分；HH:mm:ss 表示具体的时分秒；TIMEZONE 表示时区（例如，+08:00 对应东八区时间，即北京时间）。
                        示例：2015-05-20T13:29:35+08:00 表示北京时间2015年5月20日13点29分35秒。
                    3、注意事项：
                        time_expire 参数仅在用户首次下单时可设置，且不允许后续修改，尝试修改将导致错误。
                        若用户实际进行支付的时间超过了订单设置的支付结束时间，商户需使用新的商户订单号下单，生成新的订单供用户进行支付。若未超过支付结束时间，则可使用原参数重新请求下单接口，以获取当前订单最新的prepay_id 进行支付。
                        支付结束时间不能早于下单时间后1分钟，若设置的支付结束时间早于该时间，系统将自动调整为下单时间后1分钟作为支付结束时间。


            :return:
                {
                  "h5_url" : "https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id=wx2016121516420242444321ca0631331346&package=1405458241"
                }
        """
        uri = "/v3/combine-transactions/h5"
        url = f"{self.base_url}{uri}"

        # 请求体（参考微信支付文档）
        data = {
            "combine_appid": combine_appid,
            "combine_out_trade_no": combine_out_trade_no,
            "combine_mchid": self.mchid,
            "sub_orders": sub_orders,
            "notify_url": notify_url,
        }
        if time_expire:
            data["time_expire"] = time_expire

        if scene_info:
            data["scene_info"] = scene_info
        if combine_payer_info:
            data["settle_info"] = combine_payer_info
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
