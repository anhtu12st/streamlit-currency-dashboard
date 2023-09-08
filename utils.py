import plotly.graph_objects as go
import pandas as pd
import statsmodels.api as sm
import numpy as np


def format_timeseries_data(nested_data):
    formatted_data = {}
    for date, currency_data in nested_data.items():
        for currency, value in currency_data.items():
            if currency not in formatted_data:
                formatted_data[currency] = {}
            formatted_data[currency][date] = value
    return formatted_data


def filter_timeseries_data_by_period(data, period):
    dates = list(data.keys())
    period_index = None
    if period == "Week":
        period_index = 7
    elif period == "1 Month":
        period_index = 30
    elif period == "3 Months":
        period_index = 90
    elif period == "6 Months":
        period_index = 180
    else:
        period_index = 365
    period_index = min(len(dates), period_index)
    dates = dates[-period_index:]
    filtered_data = {}
    for date in dates:
        filtered_data[date] = data[date]
    return filtered_data


def draw_multi_line_charts(st, data):
    # Create an empty list to store the line chart figures
    line_chart_figs = []

    for currency, currency_data in data.items():
        # Convert the data dictionary to a DataFrame
        df = pd.DataFrame.from_dict(
            currency_data, orient='index', columns=['Value'])
        df.index = pd.to_datetime(df.index)

        # Create a Plotly line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Value'], mode='lines', name=currency))
        
        # Regression
        X = sm.add_constant(np.arange(len(df)))  # Independent variable (time)
        y = df['Value']  # Dependent variable (Value)
        model = sm.OLS(y, X).fit()
        predicted_values = model.predict(X)
        fig.add_trace(go.Scatter(x=df.index, y=predicted_values, mode='lines', name='Regression Model', line=dict(dash='dot')))
        
        # Auto Regression
        lag_order = 2  # Order of the autoregressive model (adjust as needed)
        model = sm.tsa.AutoReg(df['Value'], lags=lag_order)
        model_fit = model.fit()
        n_forecast = 10  # Number of periods to forecast into the future
        forecast_values = model_fit.predict(start=len(df), end=len(df) + n_forecast - 1)
        forecast_dates = pd.date_range(start=df.index.max() + pd.DateOffset(days=1), periods=n_forecast, freq='D')
        fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_values, mode='lines', name='Forecast', line=dict(dash='dot')))

        # Customize the chart layout
        fig.update_layout(
            title=f'Line Chart for {currency}',
            xaxis_title='Date',
            yaxis_title='Value',
            hoverlabel=dict(
                bgcolor='white',  # Background color of hover label
                bordercolor='gray',  # Border color of hover label
                font=dict(color='black')  # Text color of hover label
            )
        )

        fig.update_traces(
            mode='lines+markers',
            hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'
        )

        # Append the chart figure to the list
        line_chart_figs.append(fig)

    for fig in line_chart_figs:
        st.plotly_chart(fig)


def draw_multi_vertical_bar_charts(st, data):
    chart_figs = []

    for currency, currency_data in data.items():
        # Convert the data dictionary to a DataFrame
        df = pd.DataFrame.from_dict(
            currency_data, orient='index', columns=['Value'])
        df.index = pd.to_datetime(df.index)

        # Create a Plotly line chart
        fig = go.Figure()

        fig.add_trace(go.Bar(x=df.index, y=df['Value'], name=currency, hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'))

        # Customize the chart layout
        fig.update_layout(
            title=f'Vertical Bar Chart for {currency}',
            xaxis_title='Date',
            yaxis_title='Value',
            yaxis_type='log',
            hoverlabel=dict(
                bgcolor='white',  # Background color of hover label
                bordercolor='gray',  # Border color of hover label
                font=dict(color='black')  # Text color of hover label
            )
        )
        chart_figs.append(fig)

    for fig in chart_figs:
        st.plotly_chart(fig)


def draw_multi_horizontal_bar_charts(st, data):
    chart_figs = []

    for currency, currency_data in data.items():
        # Convert the data dictionary to a DataFrame
        df = pd.DataFrame.from_dict(
            currency_data, orient='index', columns=['Value'])
        df.index = pd.to_datetime(df.index)

        # Create a Plotly line chart
        fig = go.Figure()

        fig.add_trace(go.Bar(x=df['Value'], y=df.index,
                      name=currency, orientation='h', hovertemplate='Date: %{y|%Y-%m-%d}<br>Value: %{x:.2f}<extra></extra>'))
        # Customize the chart layout
        fig.update_layout(
            title=f'Horizontal Bar Chart for {currency}',
            xaxis_title='Value',
            yaxis_title='Date',
            xaxis_type='log',
            hoverlabel=dict(
                bgcolor='white',  # Background color of hover label
                bordercolor='gray',  # Border color of hover label
                font=dict(color='black')  # Text color of hover label
            )
        )
        chart_figs.append(fig)

    for fig in chart_figs:
        st.plotly_chart(fig)
