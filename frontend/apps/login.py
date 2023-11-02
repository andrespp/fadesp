"""login.py
"""
import requests
import dash_bootstrap_components as dbc
from app import app, _, API_URL
from dash import html 
from dash.dependencies import Input, Output, State

# Login Form
login_form = [

    html.Div(
        [
            dbc.Label(_('Username'), html_for='username'),
            dbc.Input(type='text', id='username', placeholder=_('Enter username')),
        ],
        className="mb-3",
    ),

    html.Div(
        [
            dbc.Label(_('Password'), html_for='password'),
            dbc.Input(
                type='password',
                id='password',
                placeholder=_('Enter password'),
            ),
        ],
        className="mb-3",
    ),

    dbc.Button(_('Login'),
               id='login-button',
               type='submit',
               color='secondary',
              ),

]

login_form_layout =  [
    html.Div([

        # Header
        dbc.Row([
            dbc.Col([
                html.H3(_('Login Page')),
            ],
                width=6,
                className='text-center',
            ),
        ],
            justify='around',
            className='pt-5'
        ),

        # Form
        dbc.Row([

            dbc.Col(login_form,
                    className='p-0',
                    width=6,
            ),

        ],
            justify='around',
            className='py-3'
        ),

    ], className='p-5 mt-4')
]

logged_layout = html.Div(dbc.Row(
    [
        dbc.Col(
            [
                html.P('NaN', id='username-p'),
                dbc.Button(
                    _('Logout'),
                    color='secondary',
                    id='exit-btn'
                ),
            ],
            width=6,
            className='text-center',
        ),
    ],
        justify='around',
        className='pt-5'
)),

def layout(pathname, auth_data):
    """Define page layout
    """
    print(pathname, end=' ')
    print(auth_data)

    if not auth_data['username']:

        # Page Layout
        layout = login_form_layout

    else:
        layout = logged_layout

    return html.Div(
        [
            # Alerts
            dbc.Row(
                dbc.Col(
                    html.Div(id='login-alert'),
                    width={'size':12, 'offset':0},
                    className='px-3',
                ),
            ),
            html.Div(layout, id='login-page')
        ]
    )

###############################################################################
# API functions
###############################################################################

def api_login(app_url, username, password):
    request_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json"
    }
    payload = {"username": username, "password": password}
    request_url = f"{app_url}/token"

    try:
        response = requests.post(
            request_url, headers=request_headers, data=payload
        )
        return response
    except Exception as e:
        print(e)
        return None

def build_request_headers(
        access_token,
        accept_type="application/json",
        **kwargs
    ):
    headers = {
        "accept": accept_type
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    if "content_type" in kwargs:
        headers["Content-Type"] = kwargs["content_type"]

    return headers

###############################################################################
# Callbacks
###############################################################################

# Callbacks
@app.callback(
    Output('login-alert', 'children', allow_duplicate=True),
    Output('auth-data','data', allow_duplicate=True),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True,
)
def login(n_clicks, username, password):

    if not n_clicks:
        return None, {'username':None, 'access_token':None}

    # login
    try:
        response =  api_login(API_URL, username, password)
    except Exception as e:
        print(e)
        response = None

    if response:
        access_token = response.json()['access_token']
        return dbc.Alert(
            _('Welcome') + ' ' + username + '!',
            color="success"
        ), {'username':username, 'access_token':access_token}
    else:
        app.ACCESS_TOKEN = None
        return dbc.Alert(
            _('Login Failed!'),
            color="danger"
        ), {'username':None, 'access_token':None}

@app.callback(
    Output('login-alert', 'children', allow_duplicate=True),
    Output('auth-data','data', allow_duplicate=True),
    Input('exit-btn', 'n_clicks'),
    State('auth-data','data'),
    prevent_initial_call=True,
)
def logout(n_clicks, auth_data):

    if not n_clicks:
        return None, auth_data

    # logout
    else:
        return dbc.Alert(
            _('Logged out!'),
            color="success"
        ), {'username':None, 'access_token':None}


@app.callback(
    Output('login-page', 'children'),
    Input('auth-data','data'),
    prevent_initial_call=True,
)
def update_dashboard(auth_data):

    if not auth_data['username']:
        return login_form_layout

    else:
        return logged_layout

@app.callback(
    Output('username-p', 'children'),
    Input('auth-data','data'),
    prevent_initial_call=True,
)
def update_username_p(auth_data):

    return html.P(_(f'Logged as: ') + str(auth_data['username']))
