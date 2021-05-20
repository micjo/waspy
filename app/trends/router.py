import dash
import asyncio
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from app.trends.aggregator import Aggregator
from config import daemons
import time
# aggregator = agg.Aggregator(rbs_config)
# aggregator.run_in_background()

# y_values=[0,1,2,3,4]
# @app.route("/graph")
# def graph():
    # global y_values
    # y_values = [x+1 for x in y_values]
    # fig = go.Scatter(x=[0, 1, 2, 3, 4], y=y_values)
    # return fig.to_html(include_plotlyjs=False)

# @app.route("/trends/rbs_current")
# def rbs_current():
    # return jsonify(aggregator.getSamples())

# @app.route("/trends/aml_positions")
# def aml_position():
    # return jsonify(aggregator.getPositions())


aggr = Aggregator(daemons)
asyncio.create_task(aggr.run_main())

app_dash = dash.Dash(__name__, requests_pathname_prefix='/dash/')
app_dash.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                    'type': 'scatter', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
    )
])


@app_dash.callback(Output('example-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    print("update graph")

    positions = aggr.getPositions()
    currents = aggr.getSamples()
    timestamps = [x for x,y in positions]
    position_values = [float(y) for x,y in positions]
    current_values = [float(y) for x,y in currents]
    print(position_values)
    print(current_values)
    figure = go.Figure(
            data = [
                go.Scatter(x=timestamps, y = position_values, name="position"), #type: ignore
                go.Scatter(x=timestamps, y = current_values, name="current"), #type: ignore
                ],
            layout = go.Layout( uirevision="ee")
            )

    figure.update_yaxes(range=[-50,50])


    return figure
