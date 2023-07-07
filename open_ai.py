import json
import openai
from config import openai_api
# Load your API key from an environment variable or secret management service
openai.api_key = openai_api


class OpenAi:
    def __init__(self, text):
        self.text = text

    def format_trade(self):
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user",
                                                                                         "content": 'following this example of prompt and the completion[{\n  "prompt": "🚨Future trade signal!🚨\n\nBybit exchanger\n\n📈**BCH/USDT** (SHORT)\n\nEntry: MARKET\n\nLeverage: cross 20X\n\nTargets: 129.50\n\nStoploss: 253.20\n\nAlways use proper risk management 💯\n\nUsed 10% of ur capital\n\nTrade types: Day Trading",\n  "completion": {\n    "orderType": "Market",\n    "side": "Sell",\n    "symbol": "BCHUSDT",\n    "sl": "253.20",\n    "tp": "129.50",\n    "leverage": "10"\n  }\n},\n{\n  "prompt": "ETHUSDT\nSHORT\nEntry 1899.82\nSl. 1913\nTp 1842\nRr. 1:4.4",\n  "completion": {\n    "orderType": "Limit",\n    "side": "Sell",\n    "symbol": "BTCUSDT",\n    "price": "1899.82",\n    "sl": "1913",\n    "tp": "1842"\n  }\n},\n{\n  "prompt": "BTC SHORT SCALP (HIGH RISK)\n\nENTRY : 31323.54\n\nTP: I\'ll update manually\n\nSl: 31528.28\n\nKindly manage your risk",\n  "completion": {\n    "orderType": "Limit",\n    "side": "Sell",\n    "symbol": "BTCUSDT",\n    "price": "31323.54",\n    "sl": "31528.28"\n  }\n},\n{\n  "prompt": "🚨Future trade signal!🚨\n\nBybit exchanger\n\n📈**FLM/USDT** (LONG)\n\nEntry: MARKET\n\nLeverage: cross 20X\n\nTargets: 0.0999\n\nStoploss: 0.0749\n\nAlways use proper risk management 💯\n\nUsed 10% of ur capital\n\nTrade types: Day Trading",\n  "completion": {\n    "orderType": "Market",\n    "side": "Buy",\n    "symbol": "FLMUSDT",\n    "sl": "0.0749",\n    "tp": "0.0999",\n    "leverage": "20"\n  }\n},]  my prompt is ' + self.text + ' Note: no not display ant text apart from the "completion" json'
                                                                                         }])
        unformatted_trade = json.loads(chat_completion["choices"][0]["message"]["content"])
        trade = unformatted_trade["completion"]
        print(trade)
        if trade["orderType"] == "Market":
            trade["price"] = None
        if "sl" not in trade:
            trade["sl"] = None
        if "tp" not in trade:
            trade["tp"] = None
        calculate_average_tp_sl(tp=trade["tp"], sl=trade["sl"])
        return trade


def calculate_average_tp_sl(tp, sl):
    if tp is None or sl is None:
        return None
    if isinstance(tp, list):
        tp = sum(tp) / len(tp)
    if isinstance(sl, list):
        sl = sum(sl) / len(sl)
    return tp, sl
