import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from template import vessel_color_code
from template import THEME
from hover_template import hover_perRouteView1
from hover_template import hover_perRouteView2

def draw(df_RouteOccurrences, df_route_duration, df_route_merchant, select_route):

	fig = make_subplots(
	    rows=3, 
	    cols=1,
	    row_heights=[0.2,0.4,0.4], 
	    subplot_titles=(
	    	"Total Quantity of Trips in Selected Route", 
	    	"Average Trip Duration per Vessel Category in Selected Route", 
	    	"Deadweight Tonnage for Merchant Vessels in Selected Route"),
	    shared_xaxes=True,
	    vertical_spacing=0.075)

	fig.add_trace(
	    go.Scatter(
	        x=df_RouteOccurrences.index,
	        y=df_RouteOccurrences['route_occurrencies'],
	        fill='tozeroy',
	        name = 'All',
	        showlegend=True,
	        line = {'color': vessel_color_code['all']},
	        hovertemplate = hover_perRouteView1(),
            hoverlabel = dict(
                font_size=14),
	        ),
	    row=1,col=1)  

	for each_type in df_route_duration.columns:
	    fig.add_trace(
	        go.Scatter(
	            x=df_route_duration.index,
	            y=df_route_duration[each_type],
	            name = each_type,
	            meta = each_type,
	            legendgroup = each_type,
	            line = {'color': vessel_color_code[each_type]},
	            hovertemplate = hover_perRouteView2(),
	            hoverlabel = dict(
	                font_size=14),
	            ),
	        row=2,col=1)

	fig.add_trace(
	    go.Box(
	        x=df_route_merchant['year'],
	        y=df_route_merchant['DeadWeight Tonnage'],
	        name = 'Merchant',
	        legendgroup = 'Merchant',
	        showlegend = False,
	        marker_color = vessel_color_code['Merchant'],
	        #boxpoints='all',
	        #jitter=0.3,
	        whiskerwidth=0.5,
	        #marker_size=1,
	        line_width=1,
	        boxmean=True,
            hoverlabel = dict(
                font_size=14),
	        ),
	    row=3,col=1)

	# Y-axis
	fig.update_layout(
		margin=dict(b=150,t=150,l=80,r=80),
	    title = 'Selected Route: '+ select_route,
	    yaxis1={
	    	'title': 'Trips per Year',
	    	},
	    yaxis2={
	    	'title': 'Average Trip Duration in [hours]'},
	    	#'range': [0, ],    
	    yaxis3={
	    	'title': 'Deadweight distribution in [ton]'},
	    xaxis1={
	        'dtick': 1},
	    xaxis2={
	        'dtick': 1},
	    xaxis3={
	        #'range': [2010.5,2021.5],
	        'dtick': 1,
	        'tickvals': df_route_merchant['year']},    
	    font = dict(
	    	family = 'Helvetica Neue',
	    	size=14)
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
            x=[0.5, 0.5, 0.5],
            y=[0.75, 0.5, 0.25],
            text=[
                "No data to display for the selected route.",
                "Return to Harbour View to visualize top routes for a given harbour",
                "and select another option in Route View."
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