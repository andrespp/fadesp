from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
import dash_bootstrap_components as dbc

# Import the names of callback functions you want to test
from index import display_page

def test_display_page():
    output = display_page('/', {'user':'foo'})
    assert isinstance(output, dbc._components.Container)

