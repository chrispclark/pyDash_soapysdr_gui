#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 12:44:57 2023

@author: chrissy
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container(
    html.Div(
        [
            html.H1("App Frame"),
            html.Div(),
            html.Hr(),
            # dash.page_container,
        ],
    ),
)
