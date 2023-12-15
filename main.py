from website import website
from pywebio import *

start_server(website, port=8080, debug=True)