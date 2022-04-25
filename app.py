# -*- coding: utf-8 -*-

# Libraries
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd

# Support Modules
import preprocess
import template
import vizOverviewMap
import vizOverviewBar
import vizPerRouteView
import vizPerHarbour
import viz_region

# Launch
app = dash.Dash(__name__)
app.css.append_css({"external_url": "./assets/style.css"})
app.title = "Projet | INF8808"

# Load data
df_trips = preprocess.load_data()
df_connectivity = preprocess.get_connectivity(df_trips)
df_nodes, df_links = preprocess.load_sankey_data(df_trips)
selected_region = "Arctic Region"
df_region_connectivity = preprocess.load_region_connectivity(df_trips, selected_region)
list_harbours = preprocess.get_harbour_list(df_trips)

# Template
template.create_custom_theme()
template.set_default_theme()

# Load Figures
fig_sankey = viz_region.get_sankey_fig(df_nodes, df_links)
fig_bar_chart_region = viz_region.get_bar_chart(df_region_connectivity, selected_region)
fig_loading = vizPerHarbour.get_empty_figure()
fig_loading = vizPerHarbour.add_rectangle_shape(fig_loading)

# Per Harbour view
#principal_harbour = "Arnold's Cove"  # should be replaced by he harbour selected id_dropdown_harbourView ?
#df_instance_from, top_order_from = vizPerHarbour.get_strip_df(
#    df_trips, principal_harbour, depart=True, nb_hardour=10
#)
#fig_instance_from = vizPerHarbour.get_strip_fig(df_instance_from, top_order_from)

#df_instance_to, top_order_to = vizPerHarbour.get_strip_df(
#    df_trips, principal_harbour, depart=False, nb_hardour=10
#)
#fig_instance_to = vizPerHarbour.get_strip_fig(df_instance_to, top_order_to)

#df_sunburst_Harbour = vizPerHarbour.get_sunburst_df(df_trips, principal_harbour)
#fig_sunburst_Harbour = vizPerHarbour.get_sunburst_fig(df_sunburst_Harbour)

#df_line_Harbour = vizPerHarbour.get_line_df(df_trips, principal_harbour)
#fig_line_Harbour = vizPerHarbour.get_line_fig(df_line_Harbour)

#fig_Capacity_DTW_Harbour = vizPerHarbour.get_CapacityDTW_fig(
#    df_trips, principal_harbour
#)

# Initialize Layout
def init_app_layout(__name__):
    """
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    """
    return html.Div(
        className="content",
        style={"backgroundColor": "white", "height": "auto",},
        children=[
            html.Header(
                children=[
                    html.H1(
                        "Maritime Transport in Canada",
                        style={
                            "font-family": "Helvetica Neue",
                            "font-size": 30,
                            "textAlign": "center",
                        },
                    ),
                    html.H2(
                        "XPERT SOLUTIONS TECHNOLOGIQUES",
                        style={
                            "font-family": "Helvetica Neue",
                            "font-size": 18,
                            "textAlign": "center",
                        },
                    ),
                ]
            ),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Overview",
                        # style={
                        #     'backgroundColor':'white'
                        #     },
                        children=[
                            html.Div(
                                className="dd-container",
                                style={"padding": 10, "flex": 1, "width": "22%"},
                                children=[
                                    "Map Bubble Area and criteria for the Top 10 based on:",
                                    html.Br(),
                                    dcc.Dropdown(
                                        options=[
                                            {
                                                "label": "Connectivity",
                                                "value": "Connectivity",
                                            },
                                            {
                                                "label": "Frequency",
                                                "value": "Frequency",
                                            },
                                            {
                                                "label": "Deadweight Tonnage",
                                                "value": "Deadweight Tonnage",
                                            },
                                        ],
                                        value="Connectivity",
                                        id="id_dropdown",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="viz-overview-container",
                                style={"width": "100%", "backgroundColor": "white",},
                                children=[
                                    html.Div(
                                        className="viz-map-container",
                                        style={
                                            "padding": 10,
                                            "width": "60%",
                                            "backgroundColor": "white",
                                            "float": "left",
                                        },
                                        children=[
                                            html.H2(
                                                "Harbour Map",
                                                style={"textAlign": "center",},
                                            ),
                                            dcc.Graph(
                                                id="id_fig_overview_map",
                                                className="graph",
                                                figure={},
                                                style={
                                                    #    'width': '100vh',
                                                    "height": "65vh",
                                                },
                                                config=dict(
                                                    scrollZoom=True,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="viz-bar-container",
                                        style={
                                            "padding": 10,
                                            "width": "37%",
                                            "backgroundColor": "white",
                                            "float": "right",
                                        },
                                        children=[
                                            html.H2(
                                                "Top 10 Harbours",
                                                style={"textAlign": "center",},
                                            ),
                                            dcc.Graph(
                                                id="id_fig_overview_bar",
                                                className="graph",
                                                figure={},
                                                style={
                                                    #    'width': '100vh',
                                                    "height": "65vh",
                                                },
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Br(),
                        ],
                    ),
                    dcc.Tab(
                        label="Per Harbour View",
                        # style={
                        #     'backgroundColor':'white'
                        #     },
                        children=[
                            html.Div(
                                className="dd-container",
                                style={"padding": 10, "flex": 1, "width": "22%"},
                                children=[
                                    "Please select a harbour:",
                                    html.Br(),
                                    dcc.Dropdown(
                                        options=[
                                            {"label": harbour, "value": harbour}
                                            for harbour in list_harbours
                                        ],
                                        value="Quebec",
                                        id="id_dropdown_harbourView",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="viz-instance-from",
                                style={
                                    "position": "absolute",
                                    "width": "45%",
                                    "height": "50%",
                                    "left": "0%",
                                    "backgroundColor": "white",
                                },
                                children=[
                                    html.Div(
                                        className="viz-instance-from-graph",
                                        style={"backgroundColor": "white",},
                                        children=[
                                            html.H2(
                                                "Top 10 provenances of selected Harbour",
                                                style={
                                                    "textAlign": "center",
                                                    "width": "80%",
                                                },
                                            ),
                                            dcc.Graph(
                                                id="id_fig_instance-from-container-graph",
                                                className="graph_instance_from",
                                                figure=fig_loading,
                                                style={"width": "100%"},
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            html.Div(
                                className="viz-instance-to-container",
                                style={
                                    "position": "absolute",
                                    "width": "45%",
                                    "height": "50%",
                                    "left": "50%",
                                },
                                children=[
                                    html.Div(
                                        className="viz-instance-to-graph",
                                        style={"backgroundColor": "white",},
                                        children=[
                                            html.H2(
                                                "Top 10 destinations of selected Harbour",
                                                style={
                                                    "textAlign": "center",
                                                    "width": "80%",
                                                },
                                            ),
                                            dcc.Graph(
                                                id="id_fig_instance-to-graph",
                                                className="graph",
                                                figure=fig_loading,
                                                style={},
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            html.Div(
                                className="viz-sunburst-container",
                                style={
                                    "position": "absolute",
                                    "width": "30%",
                                    "height": "30%",
                                    "left": "0%",
                                    "margin-top": "38%",
                                },
                                children=[
                                    html.Div(
                                        className="viz-sunburst-h2_graph",
                                        style={
                                            "width": "100%",
                                            "backgroundColor": "white",
                                        },
                                        children=[
                                            html.H2(
                                                "Activity Type (proportional to frequency on all connections)",
                                                style={
                                                    "textAlign": "center",
                                                    "width": "80%",
                                                },
                                            ),
                                            dcc.Graph(
                                                id="id_fig_sunburst-container-graph",
                                                className="graph",
                                                figure=fig_loading,
                                                style={},
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            html.Div(
                                className="viz-lineplot",
                                style={
                                    "position": "absolute",
                                    "width": "30%",
                                    "height": "30%",
                                    "left": "33%",
                                    "margin-top": "38%",
                                },
                                children=[
                                    html.Div(
                                        className="viz-lineplot-under-div",
                                        style={
                                            "width": "100%",
                                            "backgroundColor": "white",
                                        },
                                        children=[
                                            html.H2(
                                                "Activity Type by date",
                                                style={
                                                    "textAlign": "center",
                                                    "width": "80%",
                                                },
                                            ),
                                            dcc.Graph(
                                                id="id_fig_line-container-graph",
                                                className="graph",
                                                figure=fig_loading,
                                                style={},
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            html.Div(
                                className="viz-DTW",
                                style={
                                    "position": "absolute",
                                    "width": "30%",
                                    "height": "30%",
                                    "left": "66%",
                                    "margin-top": "38%",
                                },
                                children=[
                                    html.Div(
                                        className="viz-DTW-under-div",
                                        style={
                                            "width": "100%",
                                            "backgroundColor": "white",
                                        },
                                        children=[
                                            html.H2(
                                                "Capacity by date (in sum)",
                                                style={
                                                    "textAlign": "center",
                                                    "width": "80%",
                                                },
                                            ),
                                            dcc.Graph(
                                                id="id_fig_Capacity-DTW-container-graph",
                                                className="graph",
                                                figure=fig_loading,
                                                style={},
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Br(),
                        ],
                    ),
                    dcc.Tab(
                        label="Per Route View",
                        children=[
                            html.Div(
                                dbc.Container([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H3(
                                                "Select Departure and Arrival Harbours to visualize a Route",
                                                style={
                                                    "padding": 10,
                                                    "font-family": "Helvetica Neue",
                                                    "font-size": 16,
                                                },
                                            ),
                                            html.Div(
                                                className="dd-container_departure",
                                                style={
                                                    "padding": 10,
                                                    "flex": 1,
                                                    "width": "35%",
                                                    "backgroundColor": "white",
                                                    "float": "left",
                                                },
                                                children=[
                                                    "Select Departure Harbour:",
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": harbour, "value": harbour}
                                                            for harbour in list_harbours
                                                        ],
                                                        value="Quebec",
                                                        id="id_dd-departure",
                                                    ),
                                                ],
                                            ),
                                        ], width=12),
                                    ]),

                                    dbc.Row([
                                        html.Div(
                                            className="dd-container_arrival",
                                            style={
                                                "padding": 10,
                                                "flex": 1,
                                                "width": "35%",
                                                "float": "left",
                                            },
                                            children=[
                                                "Select Arrival Harbour:",
                                                dcc.Dropdown(
                                                    options=[
                                                        {"label": harbour, "value": harbour}
                                                        for harbour in list_harbours
                                                    ],
                                                    value="Montreal",
                                                    id="id_dd-arrival",
                                                ),
                                            ],
                                        ),
                                    ]),

                                    dbc.Row([
                                        html.Div(
                                            className="viz-container",
                                            style={
                                                "flex": 1,
                                                "width": "100%",
                                                "float": "bottom",
                                                "margin": "auto",
                                                "backgroundColor": "white",
                                            },
                                            children=[
                                                dcc.Graph(
                                                    id="id_fig_perRouteView",
                                                    className="graph",
                                                    figure={},
                                                    style={},
                                                    config=dict(
                                                        scrollZoom=False,
                                                        showTips=True,
                                                        showAxisDragHandles=False,
                                                        doubleClick=False,
                                                        displayModeBar=True,
                                                    ),
                                                )
                                            ],
                                        ),
                                    ]),

                                ]),
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Per Region View",
                        children=[
                            html.Div(
                                className="viz-overview-container",
                                style={
                                    "width": "100%",
                                    "height": "100vh",
                                    "backgroundColor": "white",
                                },
                                children=[
                                    html.Div(
                                        className="viz-map-container",
                                        style={
                                            "padding": 0,
                                            "width": "60%",
                                            "backgroundColor": "white",
                                            "float": "left",
                                        },
                                        children=[
                                            dcc.Graph(
                                                id="id_fig_region_view",
                                                className="graph",
                                                figure=fig_sankey,
                                                style={
                                                    #    'width': '100vh',
                                                    "height": "80vh",
                                                },
                                                config=dict(
                                                    scrollZoom=True,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=True,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                            html.H4(
                                                "Try clicking the region departure!",
                                                style={"textAlign": "center",},
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="viz-bar-container",
                                        style={
                                            "padding": 10,
                                            "width": "37%",
                                            "backgroundColor": "white",
                                            "float": "right",
                                        },
                                        children=[
                                            html.H2(
                                                "Outgoing traffic of the selected region",
                                                style={"textAlign": "center",},
                                            ),
                                            dcc.Graph(
                                                id="id_fig_region_bar",
                                                className="graph",
                                                figure=fig_bar_chart_region,
                                                style={
                                                    #    'width': '100vh',
                                                    "height": "65vh",
                                                },
                                                config=dict(
                                                    scrollZoom=False,
                                                    showTips=False,
                                                    showAxisDragHandles=False,
                                                    doubleClick=False,
                                                    displayModeBar=False,
                                                ),
                                            ),
                                        ],
                                    ),
                                    html.Div(),
                                ],
                            ),
                            html.Br(),
                        ],
                    ),
                ]
            ),
        ],
    )


app.layout = init_app_layout(__name__)

# Callbacks for Overview
@app.callback(
    [
        dash.dependencies.Output(
            component_id="id_fig_overview_map", component_property="figure"
        ),
        dash.dependencies.Output(
            component_id="id_fig_overview_bar", component_property="figure"
        ),
    ],
    dash.dependencies.Input(component_id="id_dropdown", component_property="value"),
)
def update_output(mode):
    fig_overview_map_cb = vizOverviewMap.init_figure(df_connectivity, mode)
    df_overviewTop10_cb = preprocess.get_overview_top10(df_connectivity, mode)
    fig_overview_bar_cb = vizOverviewBar.init_figure(df_overviewTop10_cb, mode)
    return fig_overview_map_cb, fig_overview_bar_cb

# Callbacks for Harbour View
@app.callback(
    [
        dash.dependencies.Output(
            component_id="id_fig_instance-from-container-graph",
            component_property="figure",
        ),
        dash.dependencies.Output(
            component_id="id_fig_instance-to-graph", 
            component_property="figure"
        ),
        dash.dependencies.Output(
            component_id="id_fig_sunburst-container-graph", 
            component_property="figure"
        ),
        dash.dependencies.Output(
            component_id="id_fig_line-container-graph", 
            component_property="figure"
        ),
        dash.dependencies.Output(
            component_id="id_fig_Capacity-DTW-container-graph",
            component_property="figure",
        ),
    ],
    dash.dependencies.Input(
        component_id="id_dropdown_harbourView", component_property="value"
    ),
)
def update_harbour_view(principal_harbour):

    df_instance_from, top_order_from = preprocess.get_strip_df(
        df_trips, principal_harbour, depart=True, nb_hardour=10
    )
    fig_instance_from_cb = vizPerHarbour.get_strip_fig(df_instance_from, top_order_from)

    df_instance_to, top_order_to = preprocess.get_strip_df(
        df_trips, principal_harbour, depart=False, nb_hardour=10
    )
    fig_instance_to_cb = vizPerHarbour.get_strip_fig(df_instance_to, top_order_to)

    df_sunburst_Harbour = preprocess.get_sunburst_df(df_trips, principal_harbour)
    fig_sunburst_Harbour_cb = vizPerHarbour.get_sunburst_fig(df_sunburst_Harbour)

    df_line_Harbour = preprocess.get_line_df(df_trips, principal_harbour)
    fig_line_Harbour_cb = vizPerHarbour.get_line_fig(df_line_Harbour)

    fig_Capacity_DTW_Harbour_cb = vizPerHarbour.get_CapacityDTW_fig(
        df_trips, principal_harbour
    )

    return fig_instance_from_cb, fig_instance_to_cb, fig_sunburst_Harbour_cb, fig_line_Harbour_cb, fig_Capacity_DTW_Harbour_cb

# Callbacks Route View
@app.callback(
    [
        dash.dependencies.Output(
            component_id="id_fig_perRouteView", component_property="figure"
        ),
        dash.dependencies.Output(
            component_id="id_fig_perRouteView", component_property="style"
        ),
    ],
    [
        dash.dependencies.Input(
            component_id="id_dd-departure", component_property="value"
        ),
        dash.dependencies.Input(
            component_id="id_dd-arrival", component_property="value"
        ),
    ],
)
def update_output(value1, value2):
    select_route = value1 + " to " + value2
    (
        df_RouteOccurrences,
        df_route_duration,
        df_route_merchant,
    ) = preprocess.get_route_stats(df_trips, select_route)

    if df_RouteOccurrences.size == 0:
        fig_perRouteView = vizPerRouteView.get_empty_figure()
        fig_perRouteView = vizPerRouteView.add_rectangle_shape(fig_perRouteView)
        style = {"width": "150vh", "height": "50vh"}
    else:
        fig_perRouteView = vizPerRouteView.draw(
            df_RouteOccurrences, df_route_duration, df_route_merchant, select_route
        )
        style = {"width": "150vh", "height": "130vh"}

    return fig_perRouteView, style



@app.callback(
    dash.dependencies.Output(component_id="id_fig_region_bar", component_property="figure"),
    [dash.dependencies.Input(component_id="id_fig_region_view", component_property="hoverData")],
)
def display_click_data(hoverData):
    new_selected_region = "Arctic Region"
    if hoverData is not None and len(hoverData["points"][0]["label"]):
        new_selected_region = hoverData["points"][0]["label"]

    df_region_connectivity = preprocess.load_region_connectivity(df_trips, new_selected_region)
    fig_bar_chart_region = viz_region.get_bar_chart(
        df_region_connectivity, new_selected_region
    )

    return fig_bar_chart_region
