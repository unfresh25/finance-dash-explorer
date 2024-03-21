from dash import Dash, dcc, html, Input, Output, dash_table
import colorlover as cl
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings("ignore")

app = Dash(
        __name__, 
        external_stylesheets=[dbc.themes.CYBORG], 
        title="Finance Explorer", 
        update_title=None
    )

server=app.server

colorscale = cl.scales['9']['qual']['Paired']

df = pd.read_csv('https://raw.githubusercontent.com/lihkir/Uninorte/main/AppliedStatisticMS/DataVisualizationRPython/Lectures/Python/PythonDataSets/dash-stock-ticker-demo.csv')
df = df.sort_values(by=['Date'], ascending=True)

Navigation_options = [
    dbc.NavLink(
        html.Article([
            html.Img(src=app.get_asset_url(f'{page}.svg'), alt=page, style={'height': '25px'}),
            page
        ], style={
            "display": "flex", 
            "align-items": "center",
            "justify-content": "center",
            "gap": "10px",
        }
        ), 
        href=f'/{"" if page == "AAPL" else page}', 
        active="exact"
    ) for page in df.Stock.unique()
]

Stock_descriptions = {
    "AAPL": {"Apple Inc.": "American manufacturer of personal computers, smartphones, tablet computers, computer peripherals, and computer software and one of the most recognizable brands in the world."},
    "COKE": {"Coca-Cola": "Publicly traded company (ticker symbol KO) with a top-down corporate structure that includes a chair and board, as well as a chief operating officer."},
    "GOOGL": {"Google Inc.": "American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, search engine, cloud computing, software, and hardware."},
    "TSLA": {"Tesla Inc.": "American manufacturer of electric automobiles, solar panels, and batteries for cars and home power storage."},
    "YHOO": {"Yahoo!": "Global Internet brand and services provider based in Sunnyvale, California, and owned by Verizon Communications since 2017. It was founded in 1994 by Jerry Yang and David Filo, graduate students at Stanford University in California. Yahoo! provides users with online utilities, information, and access to other websites."}
}

app.layout = html.Div([
    dcc.Location(id='url'),

    html.H1("Dashboard Stock Explorer", style={"margin-bottom": "15px", "font-size": "25px", "text-align": "center"}),

    dbc.Nav(Navigation_options, vertical=False, pills=True, style={"justify-content": "flex-start", "gap": "35px"}),

    html.Hr(),  

    html.Section([
        html.Aside([
            dcc.Dropdown(
                id='technical-indicators',
                options=[
                    {'label': 'OBV', 'value': 'OBV'},
                    {'label': 'MACD', 'value': 'MACD'},
                    {'label': 'SO', 'value': 'SO'},
                    {'label': 'A/D', 'value': 'A/D'}
                ],
                value=['OBV'],
                multi=True,
                style={
                    "color": "black", 
                    "background-color": "transparent", 
                    "border": "none", 
                    "border-bottom": "1px solid #5f5f5f",
                },
                placeholder="Select technical indicators..."
            ),
        ], style={"width": "35%"}),

        html.Aside([
            dcc.Input(
                id='std',
                type='number',
                placeholder='Std...',
                style={
                    "color": "#fff", 
                    "background-color": "transparent", 
                    "border": "none", 
                    "border-bottom": "1px solid #5f5f5f",
                    "width": "30%"
                }
            ),
            dcc.Input(
                id='periods',
                type='number',
                placeholder='Periods...',
                style={
                    "color": "#fff", 
                    "background-color": "transparent", 
                    "border": "none", 
                    "border-bottom": "1px solid #5f5f5f",
                    "width": "30%"
                }
            )
        ], style={"display": "flex", "gap": "15px"}),        
    ], style={
        "display": "flex", 
        "justify-content": "flex-start", 
        "align-items": "flex-end",
        "gap": "15px"
    }),

    html.Section([
        html.Aside([        
            html.Article([                
                html.Div(id="stock-levels", style={"display": "flex", "gap": "5px", "margin-left": "2rem"}),
                html.Div([                
                    dcc.Graph(id='main-graph', style={"height": "95%"}),
                ], style={"height": "95%", "margin-top": "10px"})
            ], style={
                "width": "100%",
                "height": "95%",
            }, id='main-graph-article')
        ], style={
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "width": "70%",    
            "padding": "20px",
            "border-radius": "12px",
            "border": "1px solid rgba(255, 255, 255, 0.125)",
            "margin-top": "10px",
        }),

        html.Aside([
            html.Article([
                html.Div([
                    html.Div([
                        html.H2(id="stock-name", style={"font-size": "20px"}),
                        html.P(id="stock-description"),
                        html.Div(id="stock-price", style={"display": "flex", "flex-direction": "column"})
                    ], style={
                        "width": "100%",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "width": "100%",    
                        "padding": "20px",
                        "border-radius": "12px",
                        "border": "1px solid rgba(255, 255, 255, 0.125)",
                        "margin-top": "10px",
                    }),
                ], style={"height": "100%"}),
                html.Div(
                    id='stock-table',
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "width": "100%",    
                        "padding": "20px",
                        "border-radius": "12px",
                        "border": "1px solid rgba(255, 255, 255, 0.125)",
                        "margin-top": "10px",
                    }
                ),                                
            ], style={"height": "100%"}),
        ], style={"width": "30%"}),

    ], style={"display": "flex", "gap": "20px", "align-items": "flex-start"}),

    html.Hr(),

    html.Footer([
        html.Article([
            html.Span("Jorge Borja S."),
            html.Span("Visualización Científica"),
            html.Span("Maestría en Estadística Aplicada")
        ], style={"display": "flex", "flex-direction": "column"}),
        html.Img(src="https://www.uninorte.edu.co/o/uninorte-theme/images/uninorte/footer_un/logo.png", style={"height": "50px"})
    ], style={"display": "flex", "justify-content": "space-between", "align-items": "center"}),

    html.Br()  
], style={"height": "100vh", "margin": "0 auto", "padding": "50px", "width": "90%"})

def obv_ind(df):
    df['OBV'] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()

    return df

def macd_ind(df):
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def stoch_ind(df, window_size=5):
    df['High-Low'] = df['High'] - df['Low']
    df['%K'] = (df['Close'] - df['Low']) / df['High-Low'] * 100
    df['%D'] = df['%K'].rolling(window=window_size).mean()

    return df    

def adl_ind(df):
    df['MFM'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['ADL'] = df['MFM'] * df['Volume']
    df['A/D'] = df['ADL'].cumsum()

    return df

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

@app.callback(
    Output('main-graph','figure'),
    Output('main-graph-article', 'style'),
    Input('url', 'pathname'),
    Input('technical-indicators', 'value'),
    Input('std', 'value'),
    Input('periods', 'value')
)
def update_graph(pathname, indicators, std, periods):
    ticker = "AAPL" if pathname.lstrip('/') == "" else pathname.lstrip('/')
    dff = df[df['Stock'] == ticker]

    row_heights = [0.4 / (len(indicators) + 1)] * (len(indicators) + 1)

    fig_titles = [indicator for indicator in indicators]
    fig_titles.insert(0, ticker)

    fig = make_subplots(rows=len(indicators) + 1, cols=1, shared_xaxes=True, row_heights=row_heights, vertical_spacing=0.03, subplot_titles=fig_titles)

    candlestick = {
        'x': dff['Date'],
        'open': dff['Open'],
        'high': dff['High'],
        'low': dff['Low'],
        'close': dff['Close'],
        'type': 'candlestick',
        'name': ticker,
        'legendgroup': ticker,
        'showlegend': False,
        'increasing': {'line': {'color': colorscale[0]}},
        'decreasing': {'line': {'color': colorscale[1]}}
    }

    fig.add_trace(candlestick, row=1, col=1)

    bb_bands = bbands(dff.Close, num_of_std=5 if std == None else std, window_size=3 if periods == None else periods)
    bollinger_traces = [{        
        'x': dff['Date'], 'y': y,
        'type': 'scatter', 'mode': 'lines',
        'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
        'legendgroup': ticker,
        'showlegend': False,
        'name': f'{ticker} - bollinger bands'
    } for i, y in enumerate(bb_bands)]

    for bollinger_trace in bollinger_traces:
        fig.add_trace(bollinger_trace, row=1, col=1)

    fig.update_xaxes(rangeslider= {'visible':False}, row=1, col=1)

    row_counter = 2
    subplots_height = 600

    if 'OBV' in indicators:
        obv = obv_ind(dff)
        obv_trace = {
            'x': dff['Date'],
            'y': obv['OBV'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'OBV',
            'showlegend': False,
            'line': {'color': '#6F61C0'}
        }

        fig.add_trace(obv_trace, row=row_counter, col=1)
        fig.update_xaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))

        row_counter += 1
        subplots_height += 200

    if 'MACD' in indicators:
        macd = macd_ind(dff)
        macd_trace = {
            'x': dff['Date'],
            'y': macd['MACD'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'MACD',
            'showlegend': False,
            'line': {'color': '#0B666A'}
        }

        fig.add_trace(macd_trace, row=row_counter, col=1)
        fig.update_xaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))
        
        row_counter += 1
        subplots_height += 200

    if 'SO' in indicators:
        so = stoch_ind(dff, window_size=5 if periods == None else periods)
        so_trace = {
            'x': dff['Date'],
            'y': so['%D'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'Stochastic Oscillator',
            'showlegend': False,
            'line': {'color': '#FE6244'}
        }

        fig.add_trace(so_trace, row=row_counter, col=1)
        fig.update_xaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))

        row_counter += 1
        subplots_height += 200

    if 'A/D' in indicators:
        adl = adl_ind(dff)
        adl_trace = {
            'x': dff['Date'],
            'y': adl['A/D'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'Accumulation/Distribution Line',
            'showlegend': False,
            'line': {'color': '#F5A623'}
        }

        fig.add_trace(adl_trace, row=row_counter, col=1)
        fig.update_xaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(showgrid=False, row=row_counter, col=1, tickfont=dict(color='gray'))

        row_counter += 1
        subplots_height += 200

    fig.update_layout(
        margin={'b': 0, 'r': 10, 'l': 60, 't': 0},
        legend={'x': 0, 'font': {'color': 'gray'}},
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        xaxis={'showgrid': False, 'tickfont': {'color': 'gray'}},
        yaxis={'showgrid': False, 'tickfont': {'color': 'gray'}},
        height=subplots_height,
    )

    fig.update_annotations(font_color='gray')

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=[
                    dict(count=1,
                        label="1M",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6M",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1Y",
                        step="year",
                        stepmode="backward"),
                    dict(label="ALL",
                         step="all")
                ]),
            type="date"),
    )

    fig.update_xaxes(
        rangeselector_bgcolor="rgb(2,0,36)",
        rangeselector_font_color="#fff",
        rangeselector_activecolor="rgb(44,41,94)",
        rangeselector_bordercolor="rgba(255, 255, 255, 0.2)",
        rangeselector_borderwidth=0.5,
        rangeselector_yanchor="middle",
        rangeselector_font_size=12,
    )

    graph_style = {'height': f'{subplots_height}px'}

    return fig, graph_style


@app.callback(
    Output('stock-levels', 'children'),
    Input('main-graph', 'hoverData'),
    Input('url', 'pathname')
)
def update_stock_levels(hoverData, pathname):
    ticker = "AAPL" if pathname.lstrip('/') == "" else pathname.lstrip('/')
    dff = df[df['Stock'] == ticker]

    if hoverData is None:
        high = round(dff['High'].iloc[-1], 2)
        low = round(dff['Low'].iloc[-1], 2)
        open_price = round(dff['Open'].iloc[-1], 2)
        close = round(dff['Close'].iloc[-1], 2)

        stock_levels = [
            html.Span([html.Span(letter), html.Span(f'{price}', style={'color': 'green' if price > dff[level].iloc[-2] else 'red'})], style={"display": "flex", "gap": "5px"})
            for letter, level, price in [('O', 'Open', open_price), ('H', 'High', high), ('L', 'Low', low), ('C', 'Close', close)]
        ]

        return stock_levels

    point_index = hoverData['points'][0]['pointIndex']
    high = dff['High'].iloc[point_index]
    low = dff['Low'].iloc[point_index]
    open_price = dff['Open'].iloc[point_index]
    close = dff['Close'].iloc[point_index]

    stock_levels = [
        html.Span([html.Span(letter), html.Span(f'{price}', style={'color': 'green' if price > dff[level].iloc[point_index - 1] else 'red'})], style={"display": "flex", "gap": "5px"})
        for letter, level, price in [('O', 'Open', open_price), ('H', 'High', high), ('L', 'Low', low), ('C', 'Close', close)]
    ]

    return stock_levels


@app.callback(
    Output('stock-name', 'children'),
    Output('stock-description', 'children'),
    Output('stock-price', 'children'),
    Input('url', 'pathname')
)
def update_stock_info(pathname):
    ticker = "AAPL" if pathname.lstrip('/') == "" else pathname.lstrip('/')
    description_dict = Stock_descriptions.get(ticker, {})
    stock_name = next(iter(description_dict.keys()), "")
    stock_description = next(iter(description_dict.values()), "")

    dff = df[df['Stock'] == ticker]
    dff = dff.sort_values(by='Date', ascending=True)
    
    stock_price = []

    close = dff['Close'].iloc[-1]
    date = dff['Date'].iloc[-1]

    stock_price_t = f'{close:,.2f}' if close is not None else ''
    stock_price_container = html.Div(
        [
            html.Span(html.H3(stock_price_t, style={"color": "#fff"})),
            html.P("USD")
        ],
        style={"display": "flex", "align-items": "flex-end", "gap": "5px"}
    )
    stock_price.append(stock_price_container)
    stock_price.append(html.Div(
        [
            html.Span("• Market Closed", style={"margin-top": "-15px"}),
            " | ",
            html.Span(date)
        ],
        style={"display": "flex", "align-items": "flex-end", "gap": "5px", "margin-top": "-15px"}
        )
    )

    return stock_name, stock_description, stock_price



default_stock_table = [
    {'Stock': 'AAPL', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'GOOGL', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'YHOO', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'TSLA', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'COKE', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0}
]

stock_table = default_stock_table

@app.callback(
    Output('stock-table', 'children'),
    Input('url', 'pathname')
)
def update_stock_table(pathname):
    global stock_table

    if stock_table == default_stock_table:
        for i, stock_data in enumerate(default_stock_table):
            stock_table[i]['Last'] = df.loc[df['Stock'] == stock_data['Stock'], 'Close'].iloc[-1]
            stock_table[i]['Chg'] = round(df.loc[df['Stock'] == stock_data['Stock'], 'Close'].iloc[-1] - df.loc[df['Stock'] == stock_data['Stock'], 'Close'].iloc[-2], 2)
            stock_table[i]['Chg%'] = round(((df.loc[df['Stock'] == stock_data['Stock'], 'Close'].iloc[-1] - df.loc[df['Stock'] == stock_data['Stock'], 'Close'].iloc[-2]) / df.loc[df['Stock'] == stock_data['Stock'], 'Close'].iloc[-2]) * 100, 2)

    stock_table_df = pd.DataFrame(stock_table)

    return [
        dash_table.DataTable(
            columns=[
                {'name': 'Stock', 'id': 'Stock', 'type': 'text'},
                {'name': 'Last', 'id': 'Last', 'type': 'numeric'},
                {'name': 'Chg', 'id': 'Chg', 'type': 'numeric'},
                {'name': 'Chg%', 'id': 'Chg%', 'type': 'numeric'},
            ],
            data=stock_table_df.to_dict('records'),
            row_selectable=False,
            sort_action='native',
            style_cell={
                "backgroundColor": "transparent",
                "color": "gray",
                "border": "none",
                "font-size": "16px",
            },
            style_data_conditional=[
                {
                    "if": {"column_id": "Chg", "filter_query": "{Chg} < 0"},
                    "color": "red",
                },
                {
                    "if": {"column_id": "Chg%", "filter_query": "{Chg%} < 0"},
                    "color": "red",
                },
                {
                    "if": {"column_id": "Chg", "filter_query": "{Chg} >= 0"},
                    "color": "green",
                },
                {
                    "if": {"column_id": "Chg%", "filter_query": "{Chg%} >= 0"},
                    "color": "green",
                },
                {
                    "if": {"row_index": 0},
                    "border-bottom": "1px solid rgba(0, 0, 0, 0.1)",
                },
            ],
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)

