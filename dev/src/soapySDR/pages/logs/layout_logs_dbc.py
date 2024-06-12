# import pandas as pd

# import dash
from dash import dcc, html

from logit import logger

logger.info("logs_dbc")

# dash.register_page(__name__)

colors = {"background": "rgb(50, 50, 50)", "text": "#FFFFFF"}

#  ----------------------- Logs Layout --------------------- #
layitout_logs = (
    html.Div(
        [
            html.H6(
                "Event Log...",
                id="status_label",
                style={"display": "inline-block"},
            ),
            dcc.Textarea(
                id="Changes_log",
                value="Textarea content initialized",
                style=dict(
                    width="100%",
                    height=250,
                    backgroundColor=colors["background"],
                    color=colors["text"],
                    font_size=".4em",
                    font_family="sans-serif",
                ),
            ),
            #  ----------------------- Interval Timers --------------------- #
            dcc.Interval(
                id="log-interval",
                interval=10 * 1000,  # in milliseconds
                n_intervals=0,
            ),
            dcc.Interval(
                id="log-interval1",
                interval=10 * 1000,  # in milliseconds
                n_intervals=0,
            ),
        ],
    ),
)
