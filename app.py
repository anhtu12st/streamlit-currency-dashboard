import datetime
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from constants import CUSTOM_CSS, TIME_PERIODS

from currency import Currency
from utils import draw_multi_area_charts, draw_multi_heatmap_charts, draw_multi_horizontal_bar_charts, draw_multi_line_charts, draw_multi_line_charts_bollinger_bands, draw_multi_vertical_bar_charts, draw_seasonal_decomposition_charts, filter_timeseries_data_by_period, filter_timeseries_df_data_by_period, format_timeseries_data

currency = Currency()

with open('./data/result_increase_by_date_range.json', 'r') as file:
    top_data = json.load(file)

with open('./data/result_decrease_by_date_range.json', 'r') as file:
    decrease_data = json.load(file)

# Define the Streamlit app
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def main():
    ###
    # SIDEBAR
    ###
    # Create a left sidebar
    st.sidebar.title('Sidebar')

    list_symbols = list(currency.get_symbols().keys())
    selected_period = st.sidebar.radio(
        'Select a time period:', TIME_PERIODS, index=2)
    base_currency = st.sidebar.selectbox(
        'Base Currency:', list_symbols, index=list_symbols.index("USD"))
    selected_1st_currencies = st.sidebar.selectbox(
        'Select 1st currencies:', list_symbols, index=list_symbols.index("VND"), key="1st")
    selected_2nd_currencies = st.sidebar.selectbox(
        'Select 2nd currencies:', [None]+list(filter(lambda x: x != selected_1st_currencies, list_symbols)), index=0, key="2nd")
    selected_currencies_heatmap = st.sidebar.multiselect('Select Currencies for Correlation', list_symbols)

    
    

    ###
    # MANIPULATE DATA
    ###
    # Get the current date
    current_date = datetime.datetime(2023, 9, 25)
    date_before_365_days = current_date - datetime.timedelta(days=365)
    current_date_formatted = current_date.strftime('%Y-%m-%d')
    date_before_365_formatted = date_before_365_days.strftime('%Y-%m-%d')
    selected_currencies = [selected_1st_currencies] + \
        ([selected_2nd_currencies] if selected_2nd_currencies else [])

    timeseries_data = currency.get_timeseries_data(
        base=base_currency, symbols=selected_currencies, start_date=date_before_365_formatted, end_date=current_date_formatted)
    filtered_timeseries_data = filter_timeseries_df_data_by_period(
        timeseries_data, selected_period)

    ###
    # MAIN CONTENT
    ###
    # Set the title of the app
    # st.title(base_currency)

    # draw_timeseries_data = format_timeseries_data(filtered_timeseries_data)
    draw_timeseries_data = filtered_timeseries_data

    col1, col2 = st.columns(2)
    df_top_increase = pd.DataFrame(list(top_data.get(selected_period).items()), columns=['Currency', 'Average Change (%)'])
    col1.subheader(f"Top increase in {selected_period}")
    col1.table(df_top_increase)

    df_top_decrease = pd.DataFrame(list(decrease_data.get(selected_period).items()), columns=['Currency', 'Average Change (%)'])
    col2.subheader(f"Top decrease in {selected_period}")
    col2.table(df_top_decrease)

    fig = draw_multi_line_charts_bollinger_bands(st, draw_timeseries_data)
    st.plotly_chart(fig, use_container_width=True)

    if selected_2nd_currencies:
        fig = draw_multi_line_charts_bollinger_bands(st, draw_timeseries_data.iloc[:,[0,2]])
        st.plotly_chart(fig, use_container_width=True)

    fig = draw_multi_vertical_bar_charts(st, draw_timeseries_data)
    st.plotly_chart(fig, use_container_width=True)

    fig, fig_trend, fig_seasonal = draw_seasonal_decomposition_charts(st, draw_timeseries_data)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.plotly_chart(fig_seasonal, use_container_width=True)

    # fig1 = draw_multi_line_charts(st, draw_timeseries_data)
    # fig1 = draw_multi_heatmap_charts(draw_timeseries_data)
    # fig2 = draw_multi_area_charts(st, draw_timeseries_data)
    # st.plotly_chart(fig1, use_container_width=True)
    # st.plotly_chart(fig2, use_container_width=True)

    if len(selected_currencies_heatmap) > 1:
        timeseries_data = currency.get_timeseries_data(
            base=base_currency, symbols=selected_currencies_heatmap, start_date=date_before_365_formatted, end_date=current_date_formatted)
        filtered_timeseries_data = filter_timeseries_df_data_by_period(
            timeseries_data, selected_period)
        fig = draw_multi_heatmap_charts(filtered_timeseries_data)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
