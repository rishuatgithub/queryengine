import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

styles = {
    'output': {
        'overflow-y': 'scroll',
        'overflow-wrap': 'break-word',
        'height': 'calc(100% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}

app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=[
            {'data': {'id': 'ca', 'label': 'Canada'}}, 
            {'data': {'id': 'on', 'label': 'Ontario'}}, 
            {'data': {'id': 'qc', 'label': 'Quebec nanancs'}},
            {'data': {'id': 'ab', 'label': 'Ab'}},
            {'data': {'source': 'ca', 'target': 'on'}, 'classes':'red'},
            {'data': {'source': 'ca', 'target': 'ab'}}, 
            {'data': {'source': 'ca', 'target': 'qc'}}
        ],
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '500px'},
        stylesheet=[
        # Group selectors
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-halign':'center',
                'text-valign':'center',
                'width':'label',
                'height':'label',
                'shape':'square',
                'padding':'5px'
            }
        },
        {
            'selector': '.red',
            'style': {
                'background-color': 'red',
                'line-color': 'red'
            }
        }]
    ),
    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs-image-export', children=[
            dcc.Tab(label='generate jpg', value='jpg'),
            dcc.Tab(label='generate png', value='png')
        ]),
        html.Div(style=styles['tab'], children=[
            html.Div(
                id='image-text',
                children='image data will appear here',
                style=styles['output']
            )
        ]),
        html.Div('Download graph:'),
        html.Button("as jpg", id="btn-get-jpg"),
        html.Button("as png", id="btn-get-png"),
        html.Button("as svg", id="btn-get-svg")
    ])
])

@app.callback(
    Output('image-text', 'children'),
    Input('cytoscape-image-export', 'imageData'),
    )
def put_image_string(data):
    return data


@app.callback(
    Output("cytoscape-image-export", "generateImage"),
    [
        Input('tabs-image-export', 'value'),
        Input("btn-get-jpg", "n_clicks"),
        Input("btn-get-png", "n_clicks"),
        Input("btn-get-svg", "n_clicks"),
    ])
def get_image(tab, get_jpg_clicks, get_png_clicks, get_svg_clicks):

    ftype = tab
    action = 'store'

    ctx = dash.callback_context
    if ctx.triggered:
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if input_id != "tabs":
            action = "download"
            ftype = input_id.split("-")[-1]

    return {
        'type': ftype,
        'action': action
        }

app.run_server(debug=True)