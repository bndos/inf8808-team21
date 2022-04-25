import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from random import choices
from template import vessel_color_code
from template import THEME
from hover_template import hover_harbourView_instance, hover_harbourView_sunbusrt, hover_harbourView_line, hover_harbourView_capacity

def get_strip_fig(strip_df,top_order):
  
  fig=px.strip(strip_df, 
    x='Date',
    y='Connected Hardour',
    color='Major Vessel Type',
    color_discrete_map=vessel_color_code,
    stripmode='overlay',
    orientation = 'h',
    category_orders = {'Connected Hardour':top_order},
    )
  fig.update_traces(marker=dict(size=15,opacity=0.5,symbol = 'hexagon-open',line_width=2))
  #https://plotly.com/python/marker-style/
  fig.update_yaxes(showgrid=True)
  fig.update(
        data=[
            {"hovertemplate": hover_harbourView_instance(),}
        ]
    )
  return fig

def get_sunburst_fig(df):

  fig = px.sunburst(
      df,
      path=['Major Vessel Type', 'Vessel Type'], 
      values='Frequency',
      color = 'Major Vessel Type',
      color_discrete_map=vessel_color_code,
      )
  fig.update(
        data=[
            {"hovertemplate": hover_harbourView_sunbusrt(),}
        ]
    )

  return fig

def get_line_fig(df):
    fig = px.line(
      df, 
      x='Date', 
      y='Frequency', 
      color='Major Vessel Type',
      color_discrete_map=vessel_color_code,
      )
    fig.update(
        data=[
            {"hovertemplate": hover_harbourView_line()}
        ]
    )
    
    return fig

def get_CapacityDTW_fig(df_trip,Harbour_selected):
    df_xor = df_trip[['Arrival Hardour', 'Departure Hardour', 'Major Vessel Type','Vessel Type','Arrival Date','DeadWeight Tonnage']][((df_trip['Departure Hardour']==Harbour_selected)&(df_trip['Arrival Hardour']!=Harbour_selected)|(df_trip['Departure Hardour']!=Harbour_selected)&(df_trip['Arrival Hardour']==Harbour_selected))]
    df_xor = df_xor[['DeadWeight Tonnage','Arrival Date']]
    df_xor['Date'] = df_xor['Arrival Date'].apply(lambda x: x[0:7])
    df_xor = df_xor.groupby(by=['Date']).mean()
    #df_xor = df_xor.reset_index()
    
    fig = px.area(
      df_xor, 
      y='DeadWeight Tonnage',
      )
    
    fig.update_traces(line_color=vessel_color_code['all'])
    fig.update(
        data=[
            {"hovertemplate": hover_harbourView_capacity()}
        ]
    )
    
    

    return fig

def get_empty_figure():
    """
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    """

    # TODO : Construct the empty figure to display. Make sure to

    fig = go.Figure()

    # Create scatter trace of text labels
    fig.add_trace(
        go.Scatter(
            x=[0.5],
            y=[0.5],
            text=[
                "Loading data. Please wait.",
            ],
            mode="text",
            textfont=dict(
                color="#2A2B2E",
                size=18,
                # family=THEME['accent_font_family'],
            ),
        )
    )

    # Update axes properties
    fig.update_xaxes(
        showticklabels=False, showgrid=False, zeroline=False,
    )

    fig.update_yaxes(
        showticklabels=False, showgrid=False, zeroline=False,
    )

    return fig

def add_rectangle_shape(fig):
    """
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    """
    # TODO : Draw the rectangle

    fig.update_layout(xaxis=dict(domain=[0, 1]), yaxis=dict(domain=[0.25, 0.75]))

    fig.add_shape(
        type="rect",
        x0=0,
        x1=1,
        y0=0,
        y1=1,
        fillcolor=THEME["pale_color"],
        line_color=THEME["pale_color"],
        layer="below",
    )

    fig.update_shapes(opacity=1, xref="x", yref="y")

    return fig  

