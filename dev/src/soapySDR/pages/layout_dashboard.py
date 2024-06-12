import dash  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from dash import html

from .callbacks_dashboard import get_callbacks_dashboard  # type: ignore

from .layout_dashboard_dbc import (
    layitout_py_version,
    layitout_slider,
    layitout_test,
    layitout_button,
    layitout_freq_down,
    layitout_freq_up,
    layitout_graph,
    layitout_information,
    layitout_card_content,
    layitout_control,
)

# graphit = sdr_control.draw_graph()
# from flask_loguru import logger
from loguru import logger

z = get_callbacks_dashboard()
logger.info("Application Started")
dash.register_page(__name__, path="/")

layout = (
    html.Div(
        children=[
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        layitout_py_version,
                        style={"text": "white"},
                        width={"size": 1, "offset": 1, "order": "1"},
                    ),
                    dbc.Col(
                        layitout_test,
                        style={"width": "20%"},
                        width={"size": 1, "offset": 1, "order": "1"},
                    ),
                ],
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            layitout_card_content,
                            color="light",
                        ),
                        style={"text": "blue"},
                        width={"size": 10, "offset": 1, "order": "1"},
                    ),
                    dbc.Col(
                        layitout_test,
                        style={"width": "20%"},
                        width={"size": 1, "offset": 1, "order": "1"},
                    ),
                ],
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        layitout_button,
                        style={"height": "100%", "text": "white"},
                        width={
                            "size": 6,
                            "offset": 1,
                            "order": "1",
                        },
                    ),
                ],
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        layitout_graph,
                        style={"height": "1%", "width": "50%"},
                        width={"size": 6, "offset": 1, "order": "1"},
                    ),
                    dbc.Col(
                        dbc.Card(
                            layitout_control,
                            color="light",
                        ),
                        style={"text": "blue"},
                        width={"size": 2, "offset": 1, "order": "2"},
                    ),
                ],
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        layitout_information,
                        style={"width": "50%"},
                        width={"size": 6, "offset": 1, "order": "1"},
                    ),
                ],
            ),
        ],
    ),
    html.Br(),
)
