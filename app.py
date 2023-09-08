import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from constants import TIME_PERIODS

from currency import Currency
from utils import draw_multi_horizontal_bar_charts, draw_multi_line_charts, draw_multi_vertical_bar_charts, filter_timeseries_data_by_period, format_timeseries_data

currency = Currency()

# Create a DataFrame with sample data
data = {
    'Date': pd.date_range(start='2023-01-01', periods=250, freq='D'),
    'Value': np.random.rand(250)
}
df = pd.DataFrame(data)

# Define the Streamlit app


def main():
    ###
    # SIDEBAR
    ###
    # Create a left sidebar
    st.sidebar.title('Sidebar')

    list_symbols = list(currency.get_symbols().keys())
    selected_period = st.sidebar.radio(
        'Select a time period:', TIME_PERIODS, index=0)
    base_currency = st.sidebar.selectbox(
        'Base Currency:', list_symbols, index=list_symbols.index("USD"))
    selected_currencies = st.sidebar.multiselect(
        'Select currencies:', list_symbols, default="VND", key="multiselect")
    chart_type = st.sidebar.selectbox(
        'Chart Type:', ["Line Chart", "Vertical Bar Chart", "Horizontal Bar Chart"], index=0)

    ###
    # MANIPULATE DATA
    ###
    # Get the current date
    current_date = datetime.datetime.now()
    date_before_365_days = current_date - datetime.timedelta(days=365)
    current_date_formatted = current_date.strftime('%Y-%m-%d')
    date_before_365_formatted = date_before_365_days.strftime('%Y-%m-%d')

    timeseries_data = currency.get_timeseries_data(
        base=base_currency, symbols=selected_currencies, start_date=date_before_365_formatted, end_date=current_date_formatted)
    filtered_timeseries_data = filter_timeseries_data_by_period(
        timeseries_data, selected_period)

    ###
    # MAIN CONTENT
    ###
    # Set the title of the app
    st.title(chart_type)

    draw_timeseries_data = format_timeseries_data(filtered_timeseries_data)
    if chart_type == "Line Chart":
        draw_multi_line_charts(st, draw_timeseries_data)
    elif chart_type == "Vertical Bar Chart":
        draw_multi_vertical_bar_charts(st, draw_timeseries_data)
    elif chart_type == "Horizontal Bar Chart":
        draw_multi_horizontal_bar_charts(st, draw_timeseries_data)

    


if __name__ == '__main__':
    main()
