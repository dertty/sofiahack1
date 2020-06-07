import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from preprossor import Preporcessor, filter_exclam, filter_bad_signs, filter_roman, filter_bad_signs, filter_abb, filter_stations
# from classifier import NagibatorClassifier
# import transformers as ppb
import pandas as pd
import base64
import datetime
import io
import dash_table

import flask
from flask.helpers import send_file
server = flask.Flask('app')

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)
server = app.server
app.config.suppress_callback_exceptions = True

AICore = Preporcessor([filter_exclam, filter_bad_signs, filter_roman, filter_bad_signs, filter_abb, filter_stations])

buttons = html.Div(
    [
        dbc.Row(
            [
                dbc.Button("Try", id="button", className="mr-1", size='lg'),
                dcc.Upload(
                    children=dbc.Button("Upload CSV", id="csv_button", className="mr-1", size='lg', color="secondary"),
                    id='upload-data', )]),
    ]
)

alert = dbc.Alert("Уровень норимализации 100%", id="alert", is_open=False, duration=4000,)

input_form = html.Div(
    [
        dbc.Input(type="text", id="input_address", placeholder="Введите адрес"),
        dbc.FormText("Исправь адрес и найди свой путь", color="secondary",),
    ]
)

card = dbc.FormText(" ", color="secondary", id='output')

app.layout = dbc.Container([
    dbc.Row(dbc.Col(
        [
            dbc.Row([dbc.Col(html.Div(html.H1("Sophia Hack #1")))]),
            dbc.Row(
                [
                    dbc.Col(html.Div(input_form)),
                    dbc.Col(html.Div(buttons)),
                ]),
            dbc.Row([dbc.Col(card)]),
            dbc.Row(html.Div(id='output-data-upload')),
        ]), justify="center", align="center", className="h-50")
], style={"height": "100vh"})


@app.callback(
    Output("output", "children"),
    [Input("button", "n_clicks"), Input("input_address", "value")],
)
def toggle_alert_no_fade(n, text):
    if n:
        if text:
            return str(AICore.preprocess([text])[0])
    else:
        return ''


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(content, name, date):
    if content is not None:
        children = [parse_contents(content, name, date)]
        return children


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=';')

        if 'adr' not in df.columns or 'id' not in df.columns:
            return html.Div(['There was an error processing this file. Check the column names: id, adr.'])
        df['norm_adr'] = AICore.preprocess(df.adr)
        # бесплатный сервер не расчитан на такое, считаем локально
        # classifier = NagibatorClassifier(clf_path, ppb.DistilBertModel, ppb.DistilBertTokenizer,
        #                                  'distilbert-base-multilingual-cased')
        # df['is_fixed'] = classifier.predict(df['norm_adr'].values)

        df = df[['id', 'adr', 'norm_adr']]
        df.to_csv('result{}{}.csv'.format(filename, date), sep=';')
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df[:100].to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),
        html.A(filename, href='result{}{}.csv'.format(filename, date))

    ])


if __name__ == "__main__":
    app.run_server(debug=False)

