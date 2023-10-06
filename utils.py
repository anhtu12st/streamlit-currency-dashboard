import plotly.graph_objects as go
import pandas as pd
from pandas import DataFrame
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose


def format_timeseries_data(nested_data):
    formatted_data = {}
    for date, currency_data in nested_data.items():
        for currency, value in currency_data.items():
            if currency not in formatted_data:
                formatted_data[currency] = {}
            formatted_data[currency][date] = value
    return formatted_data


def filter_timeseries_df_data_by_period(data: DataFrame, period):
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
    return data.tail(period_index)


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


def draw_seasonal_decomposition_charts(st, data: pd.DataFrame):
    data = data.set_index("Date")

    # Perform seasonal decomposition for the first currency
    decomposition1 = seasonal_decompose(
        data[data.columns[0]], model='additive', period=min(12, data.shape[0] // 3))

    # Original time series
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=data.index, y=data.iloc[:, 0], mode='lines+markers', name=data.columns[0],
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'),
    )

    if len(data.columns) > 1:
        # Perform seasonal decomposition for the second currency
        decomposition2 = seasonal_decompose(
            data[data.columns[1]], model='additive', period=min(12, data.shape[0] // 3))

        # Add trace for the second currency on y2
        fig.add_trace(
            go.Scatter(x=data.index, y=data.iloc[:, 1], mode='lines+markers', name=data.columns[1],
                       yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'),
        )

    fig.update_layout(
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='gray',
            font=dict(color='black')
        ),
        yaxis=dict(
            title=data.columns[0],
        ),
    )

    if len(data.columns) > 1:
        fig.update_layout(
            title=f"Line chart for {', '.join(data.columns)}",
        )
        fig.update_layout(
            yaxis2=dict(
                title=data.columns[1],
                overlaying="y",
                side="right",
            )
        )

    # Trend component
    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(x=data.index, y=decomposition1.trend, mode='lines+markers', name=data.columns[0] + ' Trend',
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Trend: %{y:.2f}<extra></extra>'),
    )

    if len(data.columns) > 1:
        fig_trend.add_trace(
            go.Scatter(x=data.index, y=decomposition2.trend, mode='lines+markers', name=data.columns[1] + ' Trend',
                       yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>Trend: %{y:.2f}<extra></extra>'),
        )
        fig_trend.update_layout(
            yaxis2=dict(
                title=data.columns[1],
                overlaying="y",
                side="right",
            )
        )

    fig_trend.update_layout(
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='gray',
            font=dict(color='black')
        ),
        yaxis=dict(
            title='Trend',
        ),
    )
    fig_trend.update_layout(title=f"Trend Component for {', '.join(data.columns)}")

    # Seasonal component
    fig_seasonal = go.Figure()
    fig_seasonal.add_trace(
        go.Scatter(x=data.index, y=decomposition1.seasonal, mode='lines+markers', name=data.columns[0] + ' Seasonal',
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Seasonal: %{y:.2f}<extra></extra>'),
    )

    if len(data.columns) > 1:
        fig_seasonal.add_trace(
            go.Scatter(x=data.index, y=decomposition2.seasonal, mode='lines+markers', name=data.columns[1] + ' Seasonal',
                       yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>Seasonal: %{y:.2f}<extra></extra>'),
        )
        fig_seasonal.update_layout(
            yaxis2=dict(
                title=data.columns[1],
                overlaying="y",
                side="right",
            )
        )

    fig_seasonal.update_layout(
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='gray',
            font=dict(color='black')
        ),
        yaxis=dict(
            title='Seasonal',
        ),
    )
    fig_seasonal.update_layout(title=f"Seasonal Component for {', '.join(data.columns)}")

    return fig, fig_trend, fig_seasonal


def draw_multi_line_charts(st, data: DataFrame):
    data = data.set_index("Date")
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=data.index, y=data.iloc[:, 0], mode='lines+markers', name=data.columns[0],
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'),
    )
    if len(data.columns) > 1:
        fig.add_trace(
            go.Scatter(x=data.index, y=data.iloc[:, 1], mode='lines+markers', name=data.columns[1],
                       yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>')
        )

    fig.update_layout(
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',  # Background color of hover label
            bordercolor='gray',  # Border color of hover label
            font=dict(color='black')  # Text color of hover label
        ),
        yaxis=dict(
            title=data.columns[0],
        ),

    )
    if len(data.columns) > 1:
        fig.update_layout(
            yaxis2=dict(
                title=data.columns[1],
                overlaying="y",
                side="right",
            )
        )

    fig.update_layout(title=f"Line chart for {', '.join(data.columns)}")
    return fig

    # # Regression
    # X = sm.add_constant(np.arange(len(df)))  # Independent variable (time)
    # y = df['Value']  # Dependent variable (Value)
    # model = sm.OLS(y, X).fit()
    # predicted_values = model.predict(X)
    # fig.add_trace(go.Scatter(x=df.index, y=predicted_values, mode='lines', name='Regression Model', line=dict(dash='dot')))

    # # Auto Regression
    # lag_order = 2  # Order of the autoregressive model (adjust as needed)
    # model = sm.tsa.AutoReg(df['Value'], lags=lag_order)
    # model_fit = model.fit()
    # n_forecast = 10  # Number of periods to forecast into the future
    # forecast_values = model_fit.predict(start=len(df), end=len(df) + n_forecast - 1)
    # forecast_dates = pd.date_range(start=df.index.max() + pd.DateOffset(days=1), periods=n_forecast, freq='D')
    # fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_values, mode='lines', name='Forecast', line=dict(dash='dot')))


def draw_multi_line_charts_bollinger_bands(st, data: pd.DataFrame):
    data = data.set_index("Date")

    # Calculate Bollinger Bands
    window = min(10, data.shape[0] // 3)  # You can adjust the window size
    data['MA'] = data.iloc[:, 0].rolling(window=window).mean()
    data['Upper'] = data['MA'] + 2 * \
        data.iloc[:, 0].rolling(window=window).std()
    data['Lower'] = data['MA'] - 2 * \
        data.iloc[:, 0].rolling(window=window).std()

    fig = go.Figure()

    # Plot the main line
    fig.add_trace(
        go.Scatter(x=data.index, y=data.iloc[:, 0], mode='lines+markers', name=data.columns[0],
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'),
    )

    # Plot Bollinger Bands and fill the area between them
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Upper'], mode='lines', line=dict(color='red'), name='Upper Bollinger Band',
                   yaxis='y1', hoverinfo='none')
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Lower'], mode='lines', line=dict(color='red'), name='Lower Bollinger Band',
                   yaxis='y1', hoverinfo='none', fill='tonexty', fillcolor='rgba(255, 0, 0, 0.2)')
    )

    # Plot the Moving Average line
    fig.add_trace(
        go.Scatter(x=data.index, y=data['MA'], mode='lines', line=dict(color='blue'), name='Moving Average',
                   yaxis='y1', hoverinfo='none')
    )

    fig.update_layout(
        title=f"Bollinger Band for {data.columns[0]}",
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='gray',
            font=dict(color='black')
        ),
        yaxis=dict(
            title=data.columns[0],
        ),
    )

    return fig


def draw_multi_vertical_bar_charts(st, data: DataFrame):
    data = data.set_index("Date")
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=data.index, y=data.iloc[:, 0], name=data.columns[0], offsetgroup=1,
               yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'),
    )
    order = (20, 2, 3)  # Example order, you may need to tune this
    model = ARIMA(data.iloc[:, 0], order=order)
    result = model.fit()
    # Generate forecasts
    forecast_steps = len(data) // 4  # Adjust as needed
    forecast = result.get_prediction(
        start=order[1], end=len(data)+forecast_steps)
    fig.add_trace(
        go.Scatter(x=forecast.predicted_mean.index, y=forecast.predicted_mean, mode='lines', name="ARIMA "+data.columns[0],
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>ARIMA Value: %{y:.2f}<extra></extra>'),
    )
    if len(data.columns) > 1:
        fig.add_trace(
            go.Bar(x=data.index, y=data.iloc[:, 1], name=data.columns[1], offsetgroup=2,
                   yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>')
        )
        model = ARIMA(data.iloc[:, 1], order=order)
        result = model.fit()
        # Generate forecasts
        forecast_steps = len(data) // 4  # Adjust as needed
        forecast = result.get_prediction(
            start=order[1], end=len(data)+forecast_steps)
        fig.add_trace(
            go.Scatter(x=forecast.predicted_mean.index, y=forecast.predicted_mean, mode='lines', name="ARIMA "+data.columns[1],
                       yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>ARIMA Value: %{y:.2f}<extra></extra>'),
        )

    # Customize the chart layout
    fig.update_layout(
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',  # Background color of hover label
            bordercolor='gray',  # Border color of hover label
            font=dict(color='black')  # Text color of hover label
        ),
        yaxis=dict(
            title=data.columns[0],
            type='log'
        )
    )
    if len(data.columns) > 1:
        fig.update_layout(
            yaxis2=dict(
                title=data.columns[1],
                type='log',
                overlaying="y",
                side="right",)
        )

    fig.update_layout(
        title=f"Bar chart with ARIMA prediction for {', '.join(data.columns)}")

    return fig


def draw_multi_area_charts(st, data: DataFrame):
    data = data.set_index("Date")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=data.index, y=data.iloc[:, 0], mode='lines', name=data.columns[0],
                   fill='tozeroy',  # Set fill to 'tozeroy' for area below the line
                   yaxis='y1', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>'),
    )

    if len(data.columns) > 1:
        fig.add_trace(
            go.Scatter(x=data.index, y=data.iloc[:, 1], mode='lines', name=data.columns[1],
                       fill='tozeroy',
                       yaxis='y2', hovertemplate='Date: %{x|%Y-%m-%d}<br>Value: %{y:.2f}<extra></extra>')
        )

    fig.update_layout(
        xaxis_title='Date',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='gray',
            font=dict(color='black')
        ),
        yaxis=dict(
            title=data.columns[0],
            type='log',
        ),
    )
    if len(data.columns) > 1:
        fig.update_layout(
            yaxis2=dict(
                title=data.columns[1],
                overlaying="y",
                side="right",
                type="log",
            )
        )
    return fig


def draw_multi_heatmap_charts(data: DataFrame):
    data = data.set_index("Date")

    fig = go.Figure()

    corr_matrix = data.corr()

    # Plotly heatmap
    fig = px.imshow(corr_matrix, x=corr_matrix.index, y=corr_matrix.columns,
                    color_continuous_scale='Viridis')

    fig.update_layout(title='Correlation Heatmap for Currencies',
                      xaxis_title='Currencies',
                      yaxis_title='Currencies',
                      width=800,  # Adjust the width as needed
                      height=600,  # Adjust the height as needed
                      margin=dict(l=0, r=0, t=30, b=0))  # Adjust margins as needed

    # Return the figure
    return fig


def draw_multi_horizontal_bar_charts(st, data: DataFrame):
    chart_figs = []

    # for currency, currency_data in data.items():
    for currency in data.columns:
        if currency == "Date":
            continue

        # Convert the data dictionary to a DataFrame
        df = data[["Date", currency]]
        df = df.set_index("Date")
        df.columns = ["Value"]
        # df.index = pd.to_datetime(df.index)

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
        return fig
