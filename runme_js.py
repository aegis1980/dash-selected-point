import json
from operator import index

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd

GRAPH_ID = 'graph_id'
URL_ID  = 'layout_id'

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


def draw_graph(selected = None):

    i = list(df['customdata']).index(selected)
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

    if selected:
        fig.add_trace(
            go.Scatter(
                showlegend=False,
                mode='markers',
                x=[df["x"][i]], 
                y=[df["y"][i]], 
                marker=dict(
                    color = [df["color"][i]],
                    size = [30],
                    line = dict(
                        color = 'Black',
                        width=1
                    )
                )
            )
        )

    return fig

#fig.update_layout(clickmode='event+select')


app.layout = html.Div([
    dcc.Location(URL_ID),
    dcc.Graph(
        id=GRAPH_ID,
        figure=fig #just blank to start
    ),

    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Figure Data**

                data in graph.figure
            """),
            html.Pre(id='figure-data', style=styles['pre']),
        ], className='three columns'),

    ])
])


@app.callback(
    Output(GRAPH_ID, 'figure'),
    Input(GRAPH_ID, 'clickData'),
    State(GRAPH_ID,'figure')
    )
def draw_graph_first(clickData, figure):
    
    if len(figure['data']) > 0:
        raise PreventUpdate
    else:
        point = clickData['points'][0]
        return draw_graph(point['customdata'])



@app.callback(
    Output('click-data', 'children'),
    Input(GRAPH_ID, 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

    
@app.callback(
    Output('figure-data', 'children'),
    Input(GRAPH_ID, 'clickData'),
    State(GRAPH_ID , 'figure')
    )
def display_figure_data(clickData, figureData):
    return json.dumps(figureData, indent=2)


app.clientside_callback(
    """
    function(clickData,figureData) {
        console.log("click");
        if (clickData === undefined){
            return window.dash_clientside.no_update;
        }

        if (figureData['data'].length == 0){
            return window.dash_clientside.no_update;
        }
            
        point = clickData['points'][0];

        hilight = {
            'x' : [[point['x']]],
            'y' : [[point['y']]],
            'marker.color' :[[point['marker.color']]]
        }
        last_trace_index = figureData['data'].length-1; //assumes always the last trace
        return [hilight,[last_trace_index],1];
    }
    """,
    Output(GRAPH_ID, 'extendData'),
    Input(GRAPH_ID, 'clickData'),
    State(GRAPH_ID , 'figure')
)


@app.callback(Output(GRAPH_ID, "clickData"),
              [Input(URL_ID, 'href')])
def onload_default_graph_select(href):
    if href is None:
        raise PreventUpdate
    else:
        return {'points' :[{'customdata': 2}]}    

if __name__ == '__main__':
    app.run_server(debug=True)
