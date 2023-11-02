import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import sqlite3
import locale
import datetime as dt
from app import app
from dash import dcc, html, dash_table
from apps import mod_datepicker
from dash.dependencies import Input, Output, State

###############################################################################
# Settings
DF_NAME='vendas'
DEFAULTS = {
    # 'period':'this_year',
    'period':'20110101,20141231',
    'is_open':'true',
},

###############################################################################
# Layout Objects
###############################################################################

# Plots
graph01 = dcc.Graph(id='venda-plot')
graph02 = dcc.Graph(id='venda-pie')
table01 = html.Div(id='venda-ng-table')
download_button = dbc.Button(
    id='btn',
    children=[html.I(className="fa fa-download mr-1"), "Download"],
    color="secondary",
    className="mt-1"
),

###############################################################################
# Dasboard layout
def layout(pathname, auth_data):
    """Define dashboard layout
    """
    layout = [

        # Filters row
        dbc.Row([dbc.Col(mod_datepicker.get_filter_card(DF_NAME))
        ]),

        # Graph row
        dbc.Row(
            [
                dbc.Col(graph01, width={'size':8, 'offset':0}),
                dbc.Col(graph02),
            ]
        ),

        dbc.Row(download_button),
        dcc.Download(id="download-component"),

        # Hidden div inside the app that stores the intermediate value
        html.Div(id='defaults', style={'display': 'none'},
                 children=str(DEFAULTS),
                ),

        # Table row

    ]
    return layout

###############################################################################
# Data lookup functions
def lookup_data(since, until, segments):

    print('INFO: lookup data')

    try:
        since = dt.datetime.strptime(str(since), '%Y%m%d').date()
        until = dt.datetime.strptime(str(until), '%Y%m%d').date()
        segment_list = ', '.join(
            ["'" + segment + "'" for segment in segments]
        )

    except:
        since = until = dt.date(1900,1,1)
        segment_list = ''

    conn = sqlite3.connect('./data/sales.db')

    query = f"""
    SELECT
        "Order Date" as date
        ,Segment as segment
        ,Sales as sales
        ,Market as market 
    FROM orders
    WHERE "Order Date" BETWEEN '{since}' AND '{until}'
        AND segment in ({segment_list})
    ORDER BY "Order Date" ASC
    """
    df = pd.read_sql(query, conn)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].apply(lambda x: x.year)
    df['month'] = df['date'].apply(lambda x: x.month)
    df['mes'] = df['date'].apply(
        lambda x: f'{x.month}/{x.year}'
    )
    df = df.groupby(['mes','segment', 'market']).agg(
        {
            'date':'first',
            'year':'first',
            'month':'first',
            'sales':'sum',

        }
    ).reset_index()

    df = df[[
            'date', 'year', 'month', 'mes', 'segment', 'market', 'sales',
        ]].sort_values(
        'date', ascending=True
    )

    return df

###############################################################################
# Callbacks
###############################################################################

@app.callback(
    Output(DF_NAME+'-filters', 'children'),
    Input(DF_NAME+'-filters', 'children'),
)
def set_filters(div):

    store = dcc.Dropdown(
        id='segment',
        options=[
            {'label': 'Consumer', 'value': 'Consumer'},
            {'label': 'Home Office', 'value': 'Home Office'},
            {'label': 'Corporate', 'value': 'Corporate'},
        ],
        value=['Consumer', 'Home Office', 'Corporate'],
        multi=True
    )

    # Final Table
    table_card = dbc.Row([

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.P('Segmentos', className='mb-1 font-weight-bold'),
                    store,
                ], className='p-2',
                            ),
            )
        ], width=5.5, #xl=4, lg=4, md=8, sm=8, xs=12,
                className='px-0',
        ),

    ], className='m-0')

    return table_card

@app.callback(
    Output("download-component", "data"),
    Input("btn", "n_clicks"),
    State('date-picker', 'start_date'),
    State('date-picker', 'end_date'),
    State('segment', 'value'),
    prevent_initial_call=True,
)
def download_table(n_clicks, start_date, end_date, segment):

    # Parse parameters
    if start_date and end_date:
        a = start_date.split('-')
        since = int(a[0] + a[1] + a[2])
        a = end_date.split('-')
        until = int(a[0] + a[1] + a[2])
        if until < since: until = since
    else:
        since = until = 0

    if n_clicks and n_clicks > 0:
        # Lookup data
        df = lookup_data(since, until, segment)
        return dcc.send_data_frame(
            df.to_csv, "sales_data.csv"
        )
    else:
        return

@app.callback(
    Output(component_id='venda-plot', component_property='figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('segment', 'value'),
)
def update_venda_graph(start_date, end_date, segments):

    # Parse parameters
    if start_date and end_date:
        a = start_date.split('-')
        since = int(a[0] + a[1] + a[2])
        a = end_date.split('-')
        until = int(a[0] + a[1] + a[2])
        if until < since: until = since
    else:
        since = until = 0

    # Lookup data
    df = lookup_data(since, until, segments)
    df = df[[ 'date', 'year', 'month', 'mes', 'segment', 'sales',
         ]]

    df = df.groupby(['mes','segment',]).agg(
        {
            'date':'first',
            'year':'first',
            'month':'first',
            'sales':'sum',

        }
    ).reset_index().sort_values('date', ascending=True)
    return px.bar(
        df, x="mes", y="sales", color="segment", title="Vendas"
    )

@app.callback(
    Output(component_id='venda-pie', component_property='figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('segment', 'value'),
)
def update_pie(start_date, end_date, segments):

    # Parse parameters
    if start_date and end_date:
        a = start_date.split('-')
        since = int(a[0] + a[1] + a[2])
        a = end_date.split('-')
        until = int(a[0] + a[1] + a[2])
        if until < since: until = since
    else:
        since = until = 0

    # Lookup data
    df = lookup_data(since, until, segments)
    return px.pie(
            df, values='sales', names='market',
            color_discrete_sequence=px.colors.sequential.RdBu
        )


