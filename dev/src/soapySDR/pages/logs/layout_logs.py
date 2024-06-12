import dash
import dash_bootstrap_components as dbc
from dash import html

from pages.logs.callbacks_logs import get_callbacks_logs
from pages.logs.callbacks_logs import get_callbacks_logs
from pages.logs.layout_logs_dbc import layitout_logs
from logit import logger

z = get_callbacks_logs()

dash.register_page(__name__)

logger.info("layout_logs")

layout = html.Div(
    children=[
        # className="g-0",
        html.Br(),
        dbc.Row(
            [
                dbc.Col(layitout_logs, style={"width": "100%"}),
            ],
        ),
    ],
)
