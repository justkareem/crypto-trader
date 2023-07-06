from openai import InvalidRequestError
from pybit.unified_trading import HTTP
from pybit.exceptions import InvalidRequestError
import re
import os


class Bybit:
    def __init__(self):
        self.session = HTTP(
            testnet=True,
            api_key="",
            api_secret="")
        self.usdt_balance = float(
            self.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")["result"]["list"][0][
                "totalAvailableBalance"])
        print("USDT balance gotten!")
        print(self.usdt_balance)
        self.leverage = float(20)

    def market_price(self, symbol):
        return float(self.session.get_tickers(category="linear", symbol=symbol)["result"]["list"][0]["markPrice"])

    def qty(self, symbol):
        qty = str(round((self.usdt_balance * self.leverage * 0.1) / self.market_price(symbol), 2))
        return qty

    def set_leverage(self, leverage, symbol):
        try:
            self.session.set_leverage(
                category="linear",
                symbol=symbol,
                buyLeverage=str(leverage),
                sellLeverage=str(leverage),
            )
        except InvalidRequestError:
            print("Leverage already set!")
        self.leverage = float(leverage)

    def positions_too_many(self):
        positions = self.session.get_positions(
            category="linear",
            settleCoin="USDT",
        )
        open_positions = positions["result"]["list"]
        number_of_positions = len(open_positions)
        if number_of_positions > 3:
            open_orders = self.session.get_open_orders(
                category="linear",
                settleCoin="USDT",
                openOnly=0,
                orderFilter="Order"
            )
            orders = open_orders["result"]["list"]
            self.cancel_all_orders(orders)
            return True
        else:
            return False

    def open_orders_too_many(self):
        orders = self.session.get_open_orders(
            category="linear",
            settleCoin="USDT",
            openOnly=0,
            orderFilter="Order"
        )
        number_of_orders = len(orders["result"]["list"])
        if number_of_orders > 5:
            return True
        else:
            return False

    def cancel_all_orders(self, data):
        open_orders = []
        for item in data:
            item['category'] = 'linear'
            open_orders = {'category': item['category'], 'symbol': item['symbol'], 'orderId': item['orderId'], }
            self.session.cancel_order(**open_orders)

    def place_trade(self, trade):
        global response
        if self.positions_too_many():
            return None
        elif self.open_orders_too_many():
            return None
        if "leverage" in trade:
            self.set_leverage(trade["leverage"], trade["symbol"])
        params = {
            "category": "linear",
            "symbol": trade["symbol"],
            "side": trade["side"],
            "qty": self.qty(trade["symbol"]),
            "orderType": trade["orderType"],
            "isLeverage": 1,
            "price": trade["price"],
            "takeProfit": trade["tp"],
            "stopLoss": trade["sl"]
        }

        # Remove parameters with value None
        params = {key: value for key, value in params.items() if value is not None}
        print(params)

        try:
            # Place your order here
            response = self.session.place_order(**params)
        except InvalidRequestError as e:
            error_message = e.args[0]  # Get the error message from the exception
            match = re.search(r"MaxNewOrderQtyX:(\d+)", error_message)  # Extract the MaxNewOrderQty value using regex
            if match:
                max_new_order_qty = match.group(1)
                qty = int(max_new_order_qty) // (10 ** 8)
                params["qty"] = str(qty)
                response = self.session.place_order(**params)
            else:
                print("MaxNewOrderQty not found in the error message")
                print("Trade not placed due to " + error_message)
                return None

        # response = self.session.place_order(
        #     category="linear",
        #     symbol=trade["symbol"],
        #     side=trade["side"],
        #     qty=self.qty(trade["symbol"]),
        #     orderType=trade["orderType"],
        #     isLeverage=1,
        #     price=trade["price"],
        #     takeProfit=trade["tp"],
        #     stopLoss=trade["sl"]
        # )
        return response, trade, self.usdt_balance, self.leverage
