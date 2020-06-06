import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

button = html.Div(
    [
        dbc.Button("Click me", id="button", className="mr-1", size='lg'),
    ]
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

dbc.FormGroup(

)


app.layout = dbc.Container([
    dbc.Row(dbc.Col(
        [
            dbc.Row([dbc.Col(html.Div(html.H1("Sofia Hack #1")))]),
            dbc.Row(
                [
                    dbc.Col(html.Div(input_form)),
                    dbc.Col(html.Div(button)),
                ]),
        ]), justify="center", align="center", className="h-50")
], style={"height": "100vh"})

@app.callback(
    Output("input_address", "placeholder"), [Input("button", "n_clicks")]
)
def on_button_click(n):
    return 'Пока что ничего не считает'


if __name__ == "__main__":
    app.run_server(debug=True)