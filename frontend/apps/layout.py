"""base.py
"""
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from app import _, app, config
from apps import home, login, sales, financial

###############################################################################
# Report Definition

def layout(pathname, auth_data, alerts=None):
    """Define app layout

    Parameters
    ----------
        alerts | list of dicts
        Ex.:  [{'message':'This is an alert message', 'type':'danger'},
               {'message':'Another alert message', 'type':'success'}]

    """

    # Process alerts
    alert=[]
    if alerts:
        for i in alerts:
            alert.append(
                dbc.Alert(i['message'],
                          color=i['type'],
                          dismissable=True,
                          className='my-1',
                         )
            )

    ## Objects

    # Header
    header = html.H3(
        config['SITE']['HEADER'],
        style={'height':'62px',
               # https://cssgradient.io/
               'background':'rgb(2,0,36)',
               'background':'linear-gradient(180deg,' \
                                             'rgba(2,0,36,1) 0%,' \
                                             'rgba(77,77,80,1) 65%,' \
                                             'rgba(123,125,125,1) 100%)'
              },
        className='p-3 m-0 text-white text-center',
    )

    # Navbar
    navbar = dbc.NavbarSimple([

            # Dashboards Dropdown
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(_('APPS'), header=True),
                    dbc.DropdownMenuItem(_('Sales'), href='/sales'),
                    dbc.DropdownMenuItem(_('Financial'), href='/financial'),
                ],
                nav=True,
                in_navbar=True,
                label=_('Dashboards'),
            ),

            # Login/Logout button
            dbc.NavLink(
                html.Div(id='login-btn'),
                href='/login'
                ),

        ],

        brand = _('Home'),
        brand_href='/',
        className='p-0',
    )

    ## Layout
    layout = dbc.Container([

        # Alerts
        dbc.Row(
            dbc.Col(alert,
                    width={'size':12, 'offset':0},
                    className='px-0',
            ),
        ),

        # Header Row
        dbc.Row(

            dbc.Col(header,
                    className='p-0',
                    width={'size':12, 'offset':0},
                   ),
                className='mt-3',

               ),

        # Navbar
        dbc.Row(dbc.Col(navbar,
                        className='p-0',
                        width={'size':12, 'offset':0},
                       ),
               ),

        # Contents
        html.Div(id='dashboard',
                className='my-1'
                ),

    ],fluid=False
    )

    return layout

###############################################################################
# Callbacks
@app.callback(
    Output('dashboard', 'children'),
    Input('url', 'pathname'),
    State('auth-data', 'data'),
)
def display_dashboard(pathname, auth_data):

    if pathname =='/':
        return home.layout
    elif pathname =='/login':
        return login.layout(pathname, auth_data)
    elif pathname =='/sales':
        return sales.layout(pathname, auth_data)
    elif pathname =='/financial':
        return financial.layout(pathname, auth_data)
    else:
        return html.Div([html.P(_('404 Page not found!'))])

@app.callback(
    Output('login-btn', 'children'),
    Input('auth-data','data'),
)
def update_login_btn(auth_data):

    if not auth_data['username']:
        return _('Login')

    else:
        return str(auth_data['username'])
