import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from app import _, app, config, DEBUG, API_URL
from apps import layout

###############################################################################
# Dash App's layout
app.title = config['SITE']['TITLE']

app.layout = dbc.Container([

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # main auth data store
    html.Div(
        dcc.Store(
            data={'username':None, 'access_token':None},
            id='auth-data'
        )
    ),

    # Contents
    html.Div(id='page-content', className='my-1'),

],fluid=False
)

###############################################################################
# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('auth-data', 'data'),
)
def display_page(pathname, auth_data):

    return layout.layout(pathname, auth_data)

###############################################################################
## Main
if __name__ == '__main__':

    # Print Server version
    print(
        f"\nDash v{dash.__version__}\n" \
        f"DCC v{dcc.__version__}\n" \
        f"DBC v{dbc.__version__}\n" \
        f"API_URL: {API_URL}\n"
    )

    # Run Server
    app.run_server(host='0.0.0.0', debug=DEBUG)

