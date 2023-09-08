import requests
import json


class Currency:
    def __init__(self) -> None:
        pass

    def get_symbols(self):
        with open("./data/symbols.json", 'r') as f:
            data = json.load(f)
        return data

    def convert_currency(self, date: str, from_currency="USD", to_currency="VND"):
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&date={date}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_historical_data(self, date: str, base="USD", symbols=["VND"]):
        url = f"https://api.exchangerate.host/{date}?base={base}&symbols={','.join(symbols)}"
        response = requests.get(url)
        data = response.json()
        return data.get("rates")

    def get_timeseries_data(self, start_date: str, end_date: str, base="USD", symbols=["VND"]):
        url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={base}&symbols={','.join(symbols)}"
        response = requests.get(url)
        data = response.json()
        return data.get("rates")

    def get_fluctuation_data(self, start_date: str, end_date: str, base="USD", symbols=["VND"]):
        url = f"https://api.exchangerate.host/fluctuation?start_date={start_date}&end_date={end_date}&base={base}&symbols={','.join(symbols)}"
        response = requests.get(url)
        data = response.json()
        return data.get("rates")


if __name__ == "__main__":
    cur = Currency()

    # print(cur.get_timeseries_data(start_date="2023-01-01", end_date="2023-09-01"))
    # print(cur.get_historical_data(date="2020-01-01"))
    # print(cur.convert_currency(date="2020-01-01"))
