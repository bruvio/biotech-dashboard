import logging
import os
import pdb
import sys

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import flask
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from scipy.optimize import curve_fit

from src.utils.data import get_data
from src.utils.fitting_functions import exp_func

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_app():
    app = flask.Flask(__name__)
    return app


server = create_app()


app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.SLATE])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
colors = {
    "background": "#111111",
    # 'background': '#0000ff',
    "text": "rgb(255,0,0)",
    "plots": "rgb(255,128,0)",
}


colors = {
    "background": "#111111",
    # 'background': '#0000ff',
    "text": "rgb(255,0,0)",
    "plots": "rgb(255,128,0)",
}


def serve_layout():
    """[function used to refresh page]

    Returns:
        [type]: [every time the page is refreshed the data is re-read and updated. Useful for future data injestion]
    """
    try:
        try:
            # reading data
            assay, ic50, labels, df = get_data()
        except Exception:
            logger.warning("\n error reading database or empty database")
            return html.Div("lallero! \n There is an error!")
        else:
            if assay is None or ic50 is None or labels is None or df is None:
                logger.warning("\n error reading database or empty database")
                return html.Div("lallero! \n There is an error!")
            # extracting exp/simulation labels
            test_outcomes = []
            for outcome in labels[" Assay Result Label"].unique():

                test_outcomes.append({"label": str(outcome), "value": outcome})

            # creating a dictionary containing compound ids for a given label
            compounds = dict()

            for label in labels[" Assay Result Label"].unique():
                filtered_df = df[df["Label"] == label]
                ids = filtered_df["ID"].unique()
                compounds[label] = ids

            return html.Div(
                children=[
                    # page title
                    html.H1(
                        children="bruvio - BioTech Testing Dashboard",
                        style={"textAlign": "center", "color": colors["text"]},
                    ),
                    # first plot using a dropdown menu to select the label to plot its data
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="test-picker",
                                options=test_outcomes,
                                value="Candidate",
                            ),
                            dcc.Graph(id="graph"),
                        ]
                    ),
                    # second plot that allows to further select a compound to plot for the given label selected above
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="compound-picker",
                            ),
                            dcc.Graph(id="graph1"),
                        ]
                    ),
                ],
                style={"backgroundColor": colors["background"]},
            )
    except Exception:
        logger.warning("\n error reading database or empty database")
        return html.Div("lallero! \n There is an error!")


@app.callback(
    dash.dependencies.Output("compound-picker", "options"),
    [dash.dependencies.Input("test-picker", "value")],
)
def set_compound_options(testlabel):
    """callback to update the plot by selecting the result label

    Args:
        testlabel ([string]): [assay result label ]

    Returns:
        [type]: [updates the plot after setting the compund id's inhibition to use]
    """
    try:
        _, _, labels, df = get_data()
    except Exception:
        logger.warning("\n error reading database or empty database")
    compounds = dict()

    for label in labels[" Assay Result Label"].unique():
        filtered_df = df[df["Label"] == label]
        ids = filtered_df["ID"].unique()
        compounds[label] = ids
    return [{"label": i, "value": i} for i in compounds[testlabel]]


@app.callback(Output("graph", "figure"), [Input("test-picker", "value")])
def update_figure(selected):
    """[updates plots after selecting the assay label to use]

    Args:
        selected ([string]): [description]

    Returns:
        [type]: [once selected the label to use the entire dataset for that label will be plotted]
    """
    dum, dum, dum, df = get_data()
    filtered_df = df[df["Label"] == selected]
    traces = []
    ids = filtered_df["ID"].unique()
    for id_ in ids:
        subdf = filtered_df[filtered_df["ID"] == id_]
        traces.append(
            go.Scatter(
                x=subdf["Concentration"],
                y=subdf["Inhibition"],
                mode="markers",
                opacity=0.7,
                marker={"size": 10},
                name="ID " + str(id_),
            )
        )

    return {
        "data": traces,
        "layout": go.Layout(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["plots"]},
            xaxis={"title": "Concentration M"},
            yaxis={"title": "% Inhibition"},
            hovermode="closest",
        ),
    }


@app.callback(
    Output("graph1", "figure"),
    [Input("test-picker", "value"), Input("compound-picker", "value")],
)
def update_figure1(selected, compound):
    """[summary]

    Args:
        selected ([string]): [assay label]
        compound ([string]): [compound id within the selected assay label]

    Returns:
        [type]: [plots the inhibition vs concentration data for the given compound id and overlays a exponential fit]
    """
    dum, dum, dum, df = get_data()

    filtered_df = df[df["Label"] == selected]
    compound_df = filtered_df[filtered_df["ID"] == compound]

    traces = []

    traces.append(
        go.Scatter(
            x=compound_df["Concentration"],
            y=compound_df["Inhibition"],
            mode="markers",
            opacity=0.7,
            marker={"size": 15},
            name="ID " + str(compound),
        ),
    )
    ydata = np.asarray(compound_df["Inhibition"])
    xdata = np.asarray(compound_df["Concentration"])
    p0 = [100, 1]  # this is an mandatory initial guess
    try:
        popt, _ = curve_fit(exp_func, xdata, ydata, p0, method="dogbox", maxfev=5000)
        x = np.linspace(xdata.min(), xdata.max(), 1000)
        yModel_fit = exp_func(x, *popt)

        fit = pd.DataFrame(
            {
                "x": x,
                "y": yModel_fit,
            }
        )
        label = "fit: a=%5.3f, b=%5.3f" % tuple(popt)
        traces.append(
            go.Scatter(
                x=fit["x"],
                y=fit["y"],
                mode="lines",
                opacity=0.7,
                marker={"size": 10},
                name=label + " - ID " + str(compound),
            ),
        )
    except ValueError:
        logger.debug("wait for fitted data")

    return {
        "data": traces,
        "layout": go.Layout(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["plots"]},
            xaxis={"title": "Concentration M"},
            yaxis={"title": "% Inhibition  - Compound " + str(compound)},
            hovermode="closest",
        ),
    }


app.layout = serve_layout()


if __name__ == "__main__":
    app.run_server(debug=True)
