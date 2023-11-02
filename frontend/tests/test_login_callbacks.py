from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash import html
import dash_bootstrap_components as dbc

# Import the names of callback functions you want to test
from apps.login import login, logout, update_dashboard

###############################################################################
# login() callback
def test_login1():
    """test login with invalid credentials"""
    alert, auth_data = login(
        n_clicks=0,
        username='foo',
        password='bar',
    )
    # assert isinstance(alert, dbc._components.Alert)
    assert auth_data == {'username':None, 'access_token':None}

###############################################################################
# logout() callback
def test_logout1():
    """test logouts"""
    alert, auth_data = logout(
        n_clicks=999,
        auth_data={'username':'foo', 'access_token':'bar'}
    )
    # assert isinstance(alert, dbc._components.Alert)
    assert auth_data == {'username':None, 'access_token':None}

###############################################################################
# update_dashboard() callback
def test_update_dashboard1():
    """test logout"""
    output = update_dashboard(
        auth_data={'username':'foo', 'access_token':'bar'}
    )
    assert isinstance(output[0], html.Div)

def test_update_dashboard2():
    """test logout"""
    output = update_dashboard(
        auth_data={'username':None, 'access_token':None}
    )
    assert isinstance(output[0], html.Div)
