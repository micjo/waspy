# contains all daemons
# aggregator = agg.Aggregator(rbs_config)
# aggregator.run_in_background()

y_values=[0,1,2,3,4]
@app.route("/graph")
def graph():
    global y_values
    y_values = [x+1 for x in y_values]
    fig = go.Scatter(x=[0, 1, 2, 3, 4], y=y_values)
    return fig.to_html(include_plotlyjs=False)

@app.route("/trends/rbs_current")
def rbs_current():
    return jsonify(aggregator.getSamples())

@app.route("/trends/aml_positions")
def aml_position():
    return jsonify(aggregator.getPositions())
