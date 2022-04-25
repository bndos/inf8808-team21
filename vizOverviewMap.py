import plotly.graph_objects as go
import plotly.express as px

from template import vessel_color_code
from hover_template import hover_overview_harbour

def init_figure(df_connectivity,mode):
    '''
        Initializes the Graph Object figure used to display the overview map.

        Returns:
            fig: The figure which will display the map
    '''
    fig = go.Figure()

    
    if mode.lower() == 'connectivity':
        metric = 'Qty_Harbours_Connected' # Qty_Regions_Connected or Qty_Harbours_Connected
        scale = 400
    elif mode.lower() == 'frequency':
        metric = 'Frequency'
        scale = 800
    else:
        metric = 'DeadWeight Tonnage'
        scale = 800

    fig.add_trace(
        go.Scattergeo(
            locationmode = 'ISO-3',
            lon = df_connectivity['lon'],
            lat = df_connectivity['lat'],
            #text = df_connectivity['Hardour'],
            #hovertemplate ="Harbour: <b>%{text}</b><br><br>" + "longitude: %{lon}<br>" + "latitude: %{lat}<br><extra></extra>",
            hoverlabel = dict(
                font_size=14),
            marker = dict(
                size = df_connectivity[metric]/df_connectivity[metric].max()*scale,
                color = vessel_color_code['all'],
                #line_color='rgb(40,40,40)',
                #line_width=0.5,
                sizemode = 'area'
            )))

    fig.update_layout(
#        title = go.layout.Title(
#            text = 'Most Connected Harbours',
#            ),
        font=dict(
            family = 'Helvetica Neue',
            size = 12,
            #color = "RebeccaPurple"
            ),
        margin = dict(l=80, r=80, t=0, b=50),
        geo = go.layout.Geo(
            resolution = 50,
            scope = 'north america',
            showframe = True,
            showcoastlines = True,
            landcolor = "rgb(229, 229, 229)",
            countrycolor = "white" ,
            coastlinecolor = "white",
            projection_type = 'natural earth',
            lonaxis_range= [-132,-45],
            lataxis_range= [38,80],
            #|domain = dict(x = [ 0, 1 ], y = [ 0, 1 ])
            )
        )
    
    # Hover data
    fig.update(
        data=[
            {"customdata": df_connectivity, "hovertemplate": hover_overview_harbour(),}
        ]
    )

    return fig

#def draw(fig, df_connectivity, mode):
#    scale = 400
#    print('Mode in draw function: '+mode)
#    if mode.lower() == 'connectivity':
#        metric = 'Qty_Harbours_Connected' # Qty_Regions_Connected or Qty_Harbours_Connected
#    elif mode.lower() == 'frequency':
#        metric = 'Frequency'
#    else:
#        metric = None
#
#    fig.add_trace(go.Scattergeo(
#        locationmode = 'ISO-3',
#        lon = df_connectivity['lon'],
#        lat = df_connectivity['lat'],
#        text = df_connectivity['Hardour'],
#        #marker_color = df_connectivity['region'],
#        marker = dict(
#            size = df_connectivity[metric]/df_connectivity[metric].max()*scale,
#            #color = df_connectivity['region'],
#            #line_color='rgb(40,40,40)',
#            #line_width=0.5,
#            sizemode = 'area'
#        )))
#
#    return fig
