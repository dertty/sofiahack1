import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from preprossor import Preporcessor, filter_exclam, filter_bad_signs, filter_roman, filter_bad_signs, filter_abb, filter_stations
import re
import numpy as np

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

AICore = Preporcessor([filter_exclam, filter_bad_signs, filter_roman, filter_bad_signs, filter_abb, filter_stations])

button = html.Div(
    [
        dbc.Button("Click me", id="button", className="mr-1", size='lg'),
    ]
)

alert = dbc.Alert(
            "Уровень норимализации 100%",
            id="alert",
            is_open=False,
            duration=4000,
        )

input_form = html.Div(
    [
        dbc.Input(type="text", id="input_address", placeholder="Введите адрес"),
        dbc.FormText(
            "Исправь адрес и найди свой путь",
            color="secondary",
        ),
    ]
)

card = dbc.FormText(" ", color="secondary", id='output')

app.layout = dbc.Container([
    dbc.Row(dbc.Col(
        [
            dbc.Row([dbc.Col(html.Div(html.H1("Sofia Hack #1")))]),
            dbc.Row(
                [
                    dbc.Col(html.Div(input_form)),
                    dbc.Col(html.Div(button)),
                ]),
            dbc.Row([dbc.Col(card)]),
        ]), justify="center", align="center", className="h-50")
], style={"height": "100vh"})

# @app.callback(
#     Output("input_address", "placeholder"),
#     [Input("button", "n_clicks")], [Input("input_address", "placeholder")]
# )
# def on_button_click(n, placeholder):
#     return re.sub('г.', 'город ', placeholder)

@app.callback(
    Output("output", "children"),
    [Input("button", "n_clicks"), Input("input_address", "value")],
)
def toggle_alert_no_fade(n, text):
    if n:
        return str(AICore.preprocess([text])[0])
    else:
        return ''

# @app.callback(
#     Output("input_address", "placeholder"),
#     [Input("button", "n_clicks"), Input("input_address", "value")],
# )
# def toggle_alert_no_fade(n, value):
#     text = value
#     return AICore([value])


if __name__ == "__main__":
    app.run_server(debug=True)

