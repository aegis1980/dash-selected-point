import json

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "color": ["blue", "green", "orange", "tan"]
})

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        showlegend=False,
        mode='markers',
        x=df["x"], 
        y=df["y"], 
        marker=dict(
            color=df["color"],
            size = 10
        ),
        customdata=df["customdata"]
    )
)

fig.add_trace(
    go.Scatter(
        showlegend=False,
        mode='markers',
        x=[1], 
        y=[1], 
        marker=dict(
            color = ['red'],
            size = [30],
            line = dict(
                color = 'Black',
                width=1
            )
        )
    )
)

#fig.update_layout(clickmode='event+select')


app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')
    ])
])


@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
        Output('basic-interactions', 'extendData'),
        Input('basic-interactions', 'clickData')
    )
def highlight_click(clickData):
    if not clickData:
        raise PreventUpdate
    point = clickData['points'][0]

    hilight = {
        'x' : [[point['x']]],
        'y' : [[point['y']]],
        'marker.color' :[[point['marker.color']]]
    }
    r = [hilight,[1],1]
    return r

if __name__ == '__main__':
    app.run_server(debug=True)
