from time import sleep
import requests
import json
import pandas as pd


df_data = pd.read_csv('./data/exchange_rates.csv', parse_dates=True)
df_data['Date'] = pd.to_datetime(df_data['Date'])


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
        # url = f"https://api.exchangerate.host/timeframe?access_key={YOUR_ACCESS_KEY}start_date={start_date}&end_date={end_date}&source={base}&currencies={','.join(symbols)}"
        # response = requests.get(url)
        # data = response.json()
        # return data
        df = df_data.copy()
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)][["Date"]+symbols+[base]]
        currency_columns = df.columns[1:]
        df[currency_columns] = df[currency_columns].div(df[base], axis=0)
        subset_df = df[["Date"]+symbols]
        return subset_df

    def get_fluctuation_data(self, start_date: str, end_date: str, base="USD", symbols=["VND"]):
        url = f"https://api.exchangerate.host/fluctuation?start_date={start_date}&end_date={end_date}&base={base}&symbols={','.join(symbols)}"
        response = requests.get(url)
        data = response.json()
        return data.get("rates")


if __name__ == "__main__":
    df = df_data.set_index('Date')
    # Define the date ranges
    date_ranges = ["Week", "1 Month", "3 Months", "6 Months", "1 Year"]
    date_range_values = [7, 30, 90, 180, 365]  # corresponding to the number of days in each range

    result_increase_dict, result_decrease_dict = {}, {}

    for i, range_name in enumerate(date_ranges):
        start_date = df.index[-1] - pd.DateOffset(days=date_range_values[i] - 1)
        end_date = df.index[-1]

        # Filter the data within the date range
        df_filtered = df.loc[start_date:end_date]

        # Calculate daily percentage change for the filtered data
        percentage_change = df_filtered.ffill().pct_change() * 100

        # Calculate the average daily percentage change
        average_daily_change = percentage_change.mean()
        top_increase_currencies = average_daily_change.nlargest(10)
        top_decrease_currencies = average_daily_change.nsmallest(10)

        result_increase_dict[range_name] = top_increase_currencies.to_dict()
        result_decrease_dict[range_name] = top_decrease_currencies.to_dict()

    # Write the result to a JSON file
    with open('result_increase_by_date_range.json', 'w') as json_file:
        json.dump(result_increase_dict, json_file)

    with open('result_decrease_by_date_range.json', 'w') as json_file:
        json.dump(result_decrease_dict, json_file)




    # currency = Currency()

    # print(currency.get_timeseries_data(start_date="2023-01-01", end_date="2023-09-01"))
    # print(currency.get_historical_data(date="2020-01-01"))
    # print(currency.convert_currency(date="2020-01-01"))
    # symbols = list(currency.get_symbols().keys())
    # for i, symbol in enumerate(symbols):
    #     sleep(1)
    #     print(i)
    #     csv_file = f'data/{symbol}.csv'

    #     # Open the CSV file in write mode
    #     with open(csv_file, 'w', newline='') as csvfile:
    #         # Create a CSV writer
    #         csv_writer = csv.writer(csvfile)

    #         # Write the header row
    #         csv_writer.writerow(['Date']+symbols)

    #         # Iterate through the JSON data and write rows to the CSV file
    #         data = currency.get_timeseries_data(start_date="2020-01-01", end_date="2020-12-31", base=symbol, symbols=symbols)
    #         print(data)
    #         for date, rates in data.items():
    #             csv_writer.writerow([date] + list(rates.get(s) if rates.get(s) else "" for s in symbols))

    #         data = currency.get_timeseries_data(start_date="2021-01-01", end_date="2021-12-31", base=symbol, symbols=symbols)
    #         for date, rates in data.items():
    #             csv_writer.writerow([date] + list(rates.get(s) if rates.get(s) else "" for s in symbols))

    #         data = currency.get_timeseries_data(start_date="2022-01-01", end_date="2022-12-31", base=symbol, symbols=symbols)
    #         for date, rates in data.items():
    #             csv_writer.writerow([date] + list(rates.get(s) if rates.get(s) else "" for s in symbols))

    #         data = currency.get_timeseries_data(start_date="2023-01-01", end_date="2023-09-25", base=symbol, symbols=symbols)
    #         for date, rates in data.items():
    #             csv_writer.writerow([date] + list(rates.get(s) if rates.get(s) else "" for s in symbols))
