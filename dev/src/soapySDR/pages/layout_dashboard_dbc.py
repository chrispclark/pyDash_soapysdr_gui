import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import dash_daq as daq
from dash.html import Div
from loguru import logger
import sys

logger.info(dir(daq))

colors = {"background": "rgb(50, 50, 50)", "text": "#FFFFFF"}

PAGE_SIZE = 25

pyver = (
    f"python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
)

layitout_control = [
    dbc.CardHeader("Status"),
    dbc.CardBody(
        [
            html.H5("Status", className="card-title"),
            html.P(
                "Current System Settings",
                className="card-text",
            ),
            html.Div(
                dash_table.DataTable(
                    data=[{}],
                    style_cell={"textAlign": "left"},
                    id="SDRsettings",
                ),
            ),
        ],
    ),
]


layitout_card_content = [
    dbc.CardHeader("Controls"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
            html.Div(id="SDRSampleRateDiv"),
            dcc.Input(
                id="SDRSampleRate", type="number", placeholder="Debounce False"
            ),
            html.Button("<<<", id="btn-dwn1", n_clicks=0),
            html.Div(
                dcc.Slider(
                    min=80.0,
                    max=140.0,
                    step=0.1,
                    value=97.3,
                    id="freq-slider1",
                    # marks={i: '{}'.format(10 ** i) for i in range(4)},
                    marks=None,
                    updatemode="drag",
                    tooltip={"placement": "bottom", "always_visible": True},
                )
            ),
        ]
    ),
]

layitout_slider = (
    html.Div(
        style={
            "width": "50%",
            "float": "left",
            "marginLeft": 20,
            "marginRight": 20,
        },
        children=[
            dcc.Slider(
                min=80.0,
                max=140.0,
                step=0.1,
                value=97.3,
                id="freq-slider",
                # marks={i: '{}'.format(10 ** i) for i in range(4)},
                marks=None,
                updatemode="drag",
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ],
    ),
)

"""
layitout_slider = (
    html.Div(
        children=[
            dmc.Slider(
                id='freq-slider',
                min=80,
                max=120,
                step=0.1,
                precision=0.1,
                value=97.3,
                marks=[
                    {'value': 80, 'label': '80Mhz'},
                    {'value': 90, 'label': '90Mhz'},
                    {'value': 80, 'label': '100Mhz'},
                ],
                mb=97.3,
            ),
            # dmc.Text(id="slider-output"),
            daq.LEDDisplay(id='led_freq', label='Default', value=1),
        ],
    ),
)
"""
layitout_freq_down = (
    html.Div(
        [
            html.Button("<<<", id="btn-dwn", n_clicks=0),
            html.Div(id="container-button-freq-dwn"),
            # className=" py-3 text-5xl font-bold text-gray-800",
        ],
    ),
)

layitout_freq_up = (
    html.Div(
        [
            html.Button(">>>", id="btn-up", n_clicks=0),
            html.Div(id="container-button-freq-up"),
            # className=" py-3 text-5xl font-bold text-gray-800",
        ],
    ),
)


"""
layitout_slider = html.Div(
    html.Div(
        [
            dcc.RangeSlider(
                id='condition-range-slider',
                min=0,
                max=30,
                value=[10, 15],
                allowCross=False
            ),
        ],
        style={"display": "grid", "grid-template-columns": "10% 40% 10%"}),
    style={'width': '20%'}
)


layitout_slider = (
    html.Div(
        [
            html.Div(
                style={'width': '10%', 'float': 'left', 'marginLeft': 20, 'marginRight': 20},
                children=[
                    dcc.Input(id='slider-min-value')
                ],
            ),
            html.Div(
                style={'width': '10%', 'float': 'left', 'marginLeft': 20, 'marginRight': 20},
                children=[
                html.Button('>>>', id='btn-tst', n_clicks=0)
                ],
            ),
            ],
    ),


    html.Div(
        style={'width':'50%', 'float':'left','marginLeft': 20, 'marginRight': 20},
        [
           children=daq.Slider(
                id='freq-slider',
                min=80.0,
                max=120.0,
                step=0.01,
                value=97.3,
                handleLabel={'showCurrentValue': True, 'label': 'VALUE'},
            ),
    ],
),

            # dmc.Text(id="slider-output"),
            daq.LEDDisplay(id='led_freq', label='Default', value=1),
        ],
        style = {'width': '49%', 'display': 'inline-block'}
    ),
    ],
),


layitout_slider = (
    html.Div(
        [
            dmc.Slider(
                id='freq-slider',
                min=80.0,
                max=120.0,
                step=0.01,
                precision=0.1,
                value=97.3,
                marks=[
                    {'value': 80.0, 'label': '80.0Mhz'},
                    {'value': 90.0, 'label': '90.0Mhz'},
                    {'value': 100.0, 'label': '100.0Mhz'},
                ],
                mb=97.3,
            ),
            # dmc.Text(id="slider-output"),
            daq.LEDDisplay(id='led_freq', label='Default', value=1),
        ],
    ),
)

"""
layitout_py_version = (
    html.Div(
        [
            html.H6(
                pyver,
                id="py-ver",
                style={
                    "display": "inline-block",
                    "margin-left": "5px",
                    "color": "white",
                    "font-size": "85%",
                },
                # className=" py-3 text-5xl font-bold text-gray-800",
            ),
        ],
    ),
)

layitout_graph: Div = html.Div(
    [
        html.H4("Displaying figure structure as JSON"),
        dcc.Graph(
            id="draw_graph",
        ),
        dcc.Clipboard(target_id="structure"),
        html.Pre(
            id="structure",
            style={
                "border": "thin lightgrey solid",
                "overflowY": "scroll",
                "height": "1px",
            },
        ),
    ]
)

layitout_button = (
    html.Div(
        [
            html.Button("102.2e6", id="btn-smooth", n_clicks=0),
            html.Button("97.3", id="btn-lbc", n_clicks=0),
            html.Button("153.025", id="btn-flex", n_clicks=0),
            html.Button("StartSDR", id="btn-startSDR", n_clicks=0),
            dbc.Switch(
                id="standalone-switch",
                label="Mute Sound",
                value=False,
            ),
            html.Div(id="container-button-layout"),
            # className=" py-3 text-5xl font-bold text-gray-800",
        ],
    ),
)

layitout_test = (
    html.Div(
        [
            html.H1(
                "test time",
                id="test_label1",
                style={
                    "display": "inline-block",
                    "font-size": "1em",
                },
                # className=" py-3 text-5xl font-bold text-gray-800",
            ),
        ],
    ),
)

layitout_information = (
    html.Div(
        [
            html.H1(
                "info time",
                id="information",
                style={
                    "display": "inline-block",
                    "font-size": "1em",
                },
                # className=" py-3 text-5xl font-bold text-gray-800",
            ),
            html.H1(
                id="spanner",
                style=dict(color="yellow"),  # <-- just so it's easy to see
            ),
        ],
    ),
    #  ----------------------- Interval Timers --------------------- #
    dcc.Interval(
        id="information-interval",
        interval=5 * 1000,  # in milliseconds
        n_intervals=0,
    ),
    dcc.Interval(
        id="SDRsettings-interval",
        interval=5 * 1000,  # in milliseconds
        n_intervals=0,
    ),
    dcc.Interval(
        id="graph_interval",
        interval=1 * 1000,  # in milliseconds
        n_intervals=0,
    ),
    dcc.Interval(
        id="load_interval",
        n_intervals=0,
        max_intervals=0,  # <-- only run once
        interval=1,
    ),
    """
    dcc.Interval(
        id="soundq-interval",
        interval=5 * 1000,  # in milliseconds
        n_intervals=0,
    )
    """,
)
