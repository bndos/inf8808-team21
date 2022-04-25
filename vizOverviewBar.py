import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from template import THEME
from template import set_default_theme
from template import vessel_color_code
from hover_template import hover_overview_harbour

def init_figure(df,mode):

    if mode.lower() == 'connectivity':
        metric = 'Qty_Harbours_Connected' # Qty_Regions_Connected or Qty_Harbours_Connected
    elif mode.lower() == 'frequency':
        metric = 'Frequency'
    else:
        metric = 'DeadWeight Tonnage'

    # Plotly express Bar Chart
    fig = px.bar(
        df, 
        x='Hardour', 
        y=metric, 
        template=pio.templates["mytemplate"],
        #color='region',
        labels={
                     "Qty_Harbours_Connected": "Total Quantity of Harbours Connected",
                     "Frequency": "Total Amount of Trips in Harbour",
                     "DeadWeight Tonnage": "Total DeadWeight Tonnage",
                     "Hardour": "Harbour",
                 }
        )

    # Layout
    fig.update_traces(marker_color=vessel_color_code['all'])
    fig.update_layout(
        margin = dict(l=80, r=80, t=50, b=280),
        )

    # Hover data
    fig.update(
        data=[
            {"customdata": df, "hovertemplate": hover_overview_harbour(),}
        ]
    )

    return fig

