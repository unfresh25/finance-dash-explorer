from datetime import datetime
from dash import Dash, dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate
import colorlover as cl
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
from functions import adl_ind, bbands, get_cached_logo, get_cached_stock_data, get_cached_stock_info, get_stock_info, macd_ind, obv_ind, stoch_ind, get_stock_data, get_most_active_stocks, get_logo
import plotly.graph_objects as go

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

# Navigation_options = [
#     dbc.NavLink(
#         html.Article([
#             html.Img(src=app.get_asset_url(f'{page}.svg'), alt=page, style={'height': '25px', 'filter': 'invert(100%) sepia(0%) saturate(17%) hue-rotate(337deg) brightness(106%) contrast(104%)'}),
#             page
#         ], style={
#             "display": "flex", 
#             "align-items": "center",
#             "justify-content": "center",
#             "gap": "10px",
#         }
#         ), 
#         href=f'/{"" if page == "AAPL" else page}', 
#         active="exact"
#     ) for page in df.Stock.unique()
# ]

Stock_descriptions = {
    "AAPL": {"Apple Inc.": "American manufacturer of personal computers, smartphones, tablet computers, computer peripherals, and computer software and one of the most recognizable brands in the world."},
    "COKE": {"Coca-Cola": "Publicly traded company (ticker symbol KO) with a top-down corporate structure that includes a chair and board, as well as a chief operating officer."},
    "GOOGL": {"Google Inc.": "American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, search engine, cloud computing, software, and hardware."},
    "TSLA": {"Tesla Inc.": "American manufacturer of electric automobiles, solar panels, and batteries for cars and home power storage."},
    "YHOO": {"Yahoo!": "Global Internet brand and services provider based in Sunnyvale, California, and owned by Verizon Communications since 2017. Yahoo! provides users with online utilities, information, and access to other websites."}
}

app.layout = html.Div([
    #dcc.Location(id='url'),

    #html.H1("Dashboard Stock Explorer", style={"margin-bottom": "15px", "font-size": "25px", "text-align": "center"}),

    #dbc.Nav(Navigation_options, vertical=False, pills=True, style={"justify-content": "flex-start", "gap": "35px"}),

    html.Nav([
        html.Span("EFINEX", style={'color': '#007eff', 'border-right': '1px solid #5f5f5f', 'height': '36px', 'display': 'flex', 'align-items': 'center', 'width': '70px'}),
        html.Aside([
            html.Span([
                html.Img(src=app.get_asset_url('icons/search.svg'), alt='Search', style={'height': '20px', 'filter': 'invert(38%) sepia(99%) saturate(4271%) hue-rotate(200deg) brightness(105%) contrast(104%)'}),
                dcc.Input(
                    type='text',
                    id=dict(type = 'searchStock', id = 'stock-opt'),
                    placeholder = 'Search an stock...',
                    value = 'AAPL',
                    persistence = False, 
                    autoComplete = 'off',
                    list = 'suggestions-list',
                    style={"width": "100%", "color": "#007eff", "background-color": "transparent", "border": "none"}
                ),
            ], style={'display': 'flex', 'align-items': 'center'}),
            html.Datalist(
                id = 'suggestions-list',
            )
        ], style={"width": "120px", 'border-right': '1px solid #5f5f5f', 'height': '36px', 'display': 'flex'}, className="technical-aside"),

        html.Aside([
            html.Label([
                html.Img(src=app.get_asset_url('icons/indicators.svg'), alt='Technical indicators', style={'height': '30px', 'filter': 'invert(38%) sepia(99%) saturate(4271%) hue-rotate(200deg) brightness(105%'})
            ]),
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
                },
                placeholder="Select technical indicators..."
            ),
        ], style={"min-width": "15%", "max-width": "50%", "display": "flex", "align-items": "center", 'border-right': '1px solid #5f5f5f'}, className="technical-aside"),

        html.Aside([
            html.Div([
                html.Label([
                    html.Img(src=app.get_asset_url('icons/deviation.svg'), alt='Technical indicators', style={'height': '25px', 'filter': 'invert(38%) sepia(99%) saturate(4271%) hue-rotate(200deg) brightness(105%'})
                ]),
                dcc.Input(
                    id='std',
                    type='number',
                    min=1,
                    max=10,
                    placeholder='Std...',
                    style={
                        "color": "#007eff", 
                        "background-color": "transparent", 
                        "border": "none", 
                        "border-bottom": "0.5px solid #5f5f5f",
                        "width": "50%"
                    }
                ),
            ], style = {"display": "flex", "align-items": "center", "gap": "15px"}),
        ], style={"width": "130px", 'border-right': '1px solid #5f5f5f', 'height': '36px', 'display': 'flex'}, className="technical-aside"),

        html.Aside([
            html.Label([
                html.Img(src=app.get_asset_url('icons/periods.svg'), alt='Technical indicators', style={'height': '25px', 'filter': 'invert(38%) sepia(99%) saturate(4271%) hue-rotate(200deg) brightness(105%'})
            ]),
            dcc.Input(
                id='periods',
                type='number',
                min=2,
                max=10,
                placeholder='Periods...',
                style={
                    "color": "#007eff", 
                    "background-color": "transparent", 
                    "border": "none", 
                    "border-bottom": "1px solid #5f5f5f",
                    "width": "40%"
                }
            )
        ], style={"display": "flex", "gap": "15px"}),       
    ], style={'display': 'flex', "justify-content": "flex-start", "align-items": "center", 'gap': '15px'}),

    html.Hr(),  

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
        }, className="graph-aside"),

        html.Aside([
            html.Article([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(id="stock-logo"),
                                html.H4(id="stock-ticker", style={"font-size": "15px", "height": "15px", "margin": "0", "margin-top": "5px"})
                            ], style={"display": "flex", "align-items": "center", "gap": "5px"}),
                            html.Span(id = 'stock-address', style={"font-size": "12px"}),
                        ], style={"display": "flex", "justify-content": "space-between", "align-items": "flex-end"}),                        

                        html.A(
                            id='stock-website',
                            rel="noopener noreferrer",
                            target="_blank",
                            style={
                                "display": "flex", 
                                "align-items": "center", 
                                "margin-top": "10px", 
                                "margin-bottom": "10px", 
                                "text-decoration": "none", 
                                "max-width": "fit-content",
                                "color": "#333"
                            },
                            className='stock-website'
                        ),

                        html.P(id="stock-description", style={"font-size": "15px"}),

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
        ], style={"width": "30%"}, className="info-aside"),

    ], style={"display": "flex", "gap": "20px", "align-items": "flex-start"}, className="graph-section"),

    html.Hr(),

    html.Footer([
        html.Article([
            html.Span("Jorge Borja S."),
            html.Span("Visualización Científica"),
            html.Span("Maestría en Estadística Aplicada")
        ], style={"display": "flex", "flex-direction": "column"}, className="footer-names"),
        html.Img(src="https://www.uninorte.edu.co/o/uninorte-theme/images/uninorte/footer_un/logo.png", style={"height": "50px"})
    ], style={"display": "flex", "justify-content": "space-between", "align-items": "center"}),

    html.Br()
], style={"height": "100vh", "margin": "0 auto", "padding": "50px", "width": "90%"}, className="body-section")

@app.callback(
    Output('suggestions-list', 'children'),
    Input({'id': 'stock-opt', 'type': 'searchStock'}, 'value'),
    prevent_initial_call = True
)
def suggest_stocks(typing):
    all_stocks = get_most_active_stocks()
    filtered_stocks = [stock for stock in all_stocks if typing.lower() in stock.lower()]

    return [html.Option(value=stock) for stock in filtered_stocks]

@app.callback(
    Output('main-graph','figure'),
    Output('main-graph-article', 'style'),
    Input({'id': 'stock-opt', 'type': 'searchStock'}, 'value'),
    Input('technical-indicators', 'value'),
    Input('std', 'value'),
    Input('periods', 'value')
)
def update_graph(stock_search, indicators, std, periods):
    stock_search = stock_search.upper() if stock_search else 'AAPL'
    ticker = stock_search
    dff = get_cached_stock_data(ticker) 

    row_heights = [0.4 / (len(indicators) + 1)] * (len(indicators) + 1)

    fig_titles = [indicator for indicator in indicators]
    fig_titles.insert(0, ticker)

    fig = make_subplots(rows=len(indicators) + 1, cols=1, shared_xaxes=True, row_heights=row_heights, vertical_spacing=0.03, subplot_titles=fig_titles)

    candlestick = {
        'x': dff.index,
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
        'x': dff.index, 'y': y,
        'type': 'scatter', 'mode': 'lines',
        'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
        'legendgroup': ticker,
        'showlegend': True if i == 0 else False,
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
            'x': dff.index,
            'y': obv['OBV'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'OBV',
            'legendgroup': 'OBV',
            'line': {'color': '#6F61C0'}
        }
        fig.add_trace(obv_trace, row=row_counter, col=1)

        obv_trace = {
            'x': dff.index,
            'y': obv['OBV Signal'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'OBV Signal',
            'legendgroup': 'OBV',
            'line': {'color': '#D7BBF5'}
        }
        fig.add_trace(obv_trace, row=row_counter, col=1)

        fig.update_xaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))

        row_counter += 1
        subplots_height += 200

    if 'MACD' in indicators:
        macd = macd_ind(dff)
        macd_trace = {
            'x': dff.index,
            'y': macd['MACD'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'MACD',
            'legendgroup': 'MACD',
            'line': {'color': '#00AD7C'}
        }
        fig.add_trace(macd_trace, row=row_counter, col=1)

        macd_trace = {
            'x': dff.index,
            'y': macd['Signal'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'MACD Signal',
            'legendgroup': 'MACD',
            'line': {'color': '#B5FF7D'}
        }
        fig.add_trace(macd_trace, row=row_counter, col=1)

        fig.update_xaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))
        
        row_counter += 1
        subplots_height += 200

    if 'SO' in indicators:
        so = stoch_ind(dff, window_size=5 if periods == None else periods)
        so_trace = {
            'x': dff.index,
            'y': so['%D'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'SO',
            'showlegend': True,
            'legendgroup': 'SO',
            'line': {'color': '#F90716'}
        }
        fig.add_trace(so_trace, row=row_counter, col=1)

        so_trace = {
            'x': dff.index,
            'y': so['Signal'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'SO Signal',
            'showlegend': True,
            'legendgroup': 'SO',
            'line': {'color': '#FFCA03'}
        }
        fig.add_trace(so_trace, row=row_counter, col=1)

        fig.update_xaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))

        row_counter += 1
        subplots_height += 200

    if 'A/D' in indicators:
        adl = adl_ind(dff)
        adl_trace = {
            'x': dff.index,
            'y': adl['A/D'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'A/D',
            'legendgroup': 'A/D',
            'line': {'color': '#332FD0'}
        }
        fig.add_trace(adl_trace, row=row_counter, col=1)

        adl_trace = {
            'x': dff.index,
            'y': adl['Signal'],
            'type': 'scatter',
            'mode': 'lines',
            'name': 'A/D Signal',
            'legendgroup': 'A/D',
            'line': {'color': '#E15FED'}
        }
        fig.add_trace(adl_trace, row=row_counter, col=1)

        fig.update_xaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))
        fig.update_yaxes(gridcolor='#111', row=row_counter, col=1, tickfont=dict(color='gray'))

        row_counter += 1
        subplots_height += 200

    fig.update_layout(
        margin={'b': 0, 'r': 10, 'l': 60, 't': 0},
        legend={'x': 0, 'font': {'color': 'gray'}, 'orientation': 'h'},
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        xaxis={'gridcolor': '#111', 'tickfont': {'color': 'gray'}},
        yaxis={'gridcolor': '#111', 'tickfont': {'color': 'gray'}},
        height=subplots_height,
        legend_y=1,
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
                    dict(count=2,
                        label="2Y",
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
    Input({'id': 'stock-opt', 'type': 'searchStock'}, 'value')
)
def update_stock_levels(hoverData, stock_search):
    stock_search = stock_search.upper() if stock_search else 'AAPL'
    ticker = stock_search
    dff = get_cached_stock_data(ticker)

    if hoverData is None:
        latest_index = -1
    else:
        latest_index = hoverData['points'][0]['pointIndex']

    high = round(dff['High'].iloc[latest_index], 2)
    low = round(dff['Low'].iloc[latest_index], 2)
    open_price = round(dff['Open'].iloc[latest_index], 2)
    close = round(dff['Close'].iloc[latest_index], 2)

    stock_levels = [
        html.Span([html.Span(letter), html.Span(f'{price}', style={'color': '#16FF00' if price > dff[level].iloc[latest_index - 1] else '#FF1E1E'})], style={"display": "flex", "gap": "5px"})
        for letter, level, price in [('O', 'Open', open_price), ('H', 'High', high), ('L', 'Low', low), ('C', 'Close', close)]
    ]

    return stock_levels

stock_descriptions = {stock: list(description.values())[0] for stock, description in Stock_descriptions.items()}

@app.callback(
    Output('stock-logo', 'children'),
    Output('stock-ticker', 'children'),
    Output('stock-address', 'children'),
    Output('stock-website', 'children'),
    Output('stock-website', 'href'),
    Output('stock-description', 'children'),
    Output('stock-price', 'children'),
    Input({'id': 'stock-opt', 'type': 'searchStock'}, 'value')
)
def update_stock_info(stock_search):
    stock_search = stock_search.upper() if stock_search else 'AAPL'
    ticker = stock_search
    stock_address, stock_description, stock_name, stock_website_link = get_cached_stock_info(ticker)

    stock_logo_filename = get_cached_logo(ticker)
    stock_logo = html.Img(src=f'assets/stocks/{stock_logo_filename}', style={"height": "20px", "filter": "invert(100%) sepia(0%) saturate(17%) hue-rotate(337deg) brightness(106%) contrast(104%)"})

    stock_website = [html.H3(stock_name, style={"font-size": "12px", "margin": "0"}), html.Img(src='assets/icons/redirect.svg', style={"height": "12px"})]

    dff = get_stock_data(ticker)
    close = dff['Close'].iloc[-1]
    date = dff.index[-1]
    formatted_date = datetime.strftime(date, '%b %d')  # Format month name and day
    date_month_day = pd.to_datetime(formatted_date, format='%b %d')
    date = date_month_day.strftime('%b %d') + ' ' + date.strftime('%H:%M') + ' UTC-4'

    stock_price = []
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
            html.Span(f'({date})')
        ],
        style={"display": "flex", "align-items": "flex-end", "gap": "5px", "margin-top": "-15px", "font-size": "12px"}
        )
    )

    return stock_logo, ticker, stock_address, stock_website, stock_website_link, stock_description, stock_price

default_stock_table = [
    {'Stock': 'AAPL', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'GOOGL', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'YHOO', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'TSLA', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0},
    {'Stock': 'COKE', 'Last': 0.0, 'Chg': 0.0, 'Chg%': 0.0}
]

stock_table = default_stock_table

closing_prices = {stock: df.loc[df['Stock'] == stock, 'Close'].iloc[-1] for stock in df['Stock'].unique()}
previous_closes = {stock: df.loc[df['Stock'] == stock, 'Close'].iloc[-2] for stock in df['Stock'].unique()}
chg_values = {stock: closing_prices[stock] - previous_closes[stock] for stock in df['Stock'].unique()}
chg_percentages = {stock: (chg_values[stock] / previous_closes[stock]) * 100 for stock in df['Stock'].unique()}

@app.callback(
    Output('stock-table', 'children'),
    Input({'id': 'stock-opt', 'type': 'searchStock'}, 'value'),
)
def update_stock_table(stock_search):
    global stock_table

    if stock_table == default_stock_table:
        for i, stock_data in enumerate(default_stock_table):
            stock = stock_data['Stock']
            stock_table[i]['Last'] = round(closing_prices.get(stock, 0.0), 2)
            stock_table[i]['Chg'] = round(chg_values.get(stock, 0.0), 2)
            stock_table[i]['Chg%'] = round(chg_percentages.get(stock, 0.0), 2)

    stock_table_df = pd.DataFrame(stock_table)

    return [
        dash_table.DataTable(
            columns=[
                {'name': 'Stock', 'id': 'Stock', 'type': 'text'},
                {'name': 'Last', 'id': 'Last', 'type': 'numeric'},
                {'name': 'Chg', 'id': 'Chg', 'type': 'numeric'},
                {'name': 'Chg%', 'id': 'Chg%', 'type': 'numeric'}
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
                    "color": "#FF1E1E",
                },
                {
                    "if": {"column_id": "Chg%", "filter_query": "{Chg%} < 0"},
                    "color": "#FF1E1E",
                },
                {
                    "if": {"column_id": "Chg", "filter_query": "{Chg} >= 0"},
                    "color": "#16FF00",
                },
                {
                    "if": {"column_id": "Chg%", "filter_query": "{Chg%} >= 0"},
                    "color": "#16FF00",
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
    #app.run_server(debug=True, host='0.0.0.0', port=5000)

