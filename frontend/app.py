"""app.py
"""
import dash
import dash_bootstrap_components as dbc
import configparser
import gettext
import locale
import os.path
_ = gettext.gettext

## Settings
CONFIG_FILE = 'config.ini'

# Read configuration File
if not os.path.isfile(CONFIG_FILE):
    print('ERROR: file "{}" does not exist'.format(CONFIG_FILE))
    exit(-1)
try:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
except:
    print('ERROR: Unable to read config file ("{}")'.format(CONFIG_FILE))
    exit(-1)

# App settings
if config['APP']['DEBUG'].lower() == 'true':
    DEBUG=True
else:
    DEBUG=False

# Backend settings
API_URL = os.getenv('API_URL')

# Set locale
locale.setlocale(locale.LC_MONETARY, config['SITE']['LANG'])

if config['SITE']['LANG'].split('.')[0]=='pt_BR':
    pt_br = gettext.translation(
        'messages',
        localedir='locales',
        languages=['pt-br']
    )
    pt_br.install()
    _ = pt_br.gettext # Brazilian portuguese

# Dash app object
THEME = dbc.themes.BOOTSTRAP
FA = "https://use.fontawesome.com/releases/v5.15.3/css/all.css"
app = dash.Dash(
    __name__,
    external_stylesheets=[THEME, FA],
    meta_tags=[
        {
            'name': 'viewport',
            'content': 'width=device-width, \
                        initial-scale=0.8,  \
                        maximum-scale=1.0,  \
                        minimum-scale=0.5,'
        }
    ]
)
app.config.suppress_callback_exceptions=True

