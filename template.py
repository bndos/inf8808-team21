"""
    Contains the template to use in the data visualization.
"""
import plotly.graph_objects as go
import plotly.io as pio


THEME = {
    "background_color": "#fff",
    "font_family": "Helvetica Neue",
    "accent_font_family": "Helvetica Neue",
    "dark_color": "#2A2B2E",
    "pale_color": "#DFD9E2",
    "line_chart_color": "#97939A",
    "label_font_size": 14,
    "label_background_color": "#ffffff",
    "colorscale": "Bluyl"
    # 'colorscale': 'Viridis'
}

# Combined view of occurrencies, trip duration and deadweight
vessel_color_code = {
    'all'           :'#0b4a9e', #blue'
    'Merchant'      :'#2A9D8F', #green
    'Passenger'     :'#E9C46A', #yellow    
    'Tug'           :'#F4A261', #lightorange           
    'Landing Craft' :'#E76F51', #darkorange    
    'Trawler'       :'#ff5656', #red      
    'Yacht'         :'#c66bce', #pink           
    'Other/Unknown' :'#667c70', #green2grey  
    'Barge'         :'#666456', #brown          
    'Fishing'       :'#3082a5', #lightblue          
    }

def create_custom_theme():
    """
        Adds a new layout template to pio's templates.

        The template sets the font color and
        font to the values defined above in
        the THEME dictionary, using the dark
        color.

        The plot background and paper background
        are the background color defined
        above in the THEME dictionary.

        Also, sets the hover label to have a
        background color and font size
        as defined for the label in the THEME dictionary.
        The hover label's font color is the same
        as the theme's overall font color. The hover mode
        is set to 'closest'.

        Sets the line chart's line color to the one
        designated in the THEME dictionary. Also sets
        the color scale to be used by the heatmap
        to the one in the THEME dictionary.

        Specifies the x-axis ticks are tilted 45
        degrees to the right.
    """
    # TODO : Generate template described above
    pio.templates["mytemplate"] = go.layout.Template(
        layout={
            "colorscale": {
                "sequential": THEME["colorscale"]
            },
            "xaxis": {
                "tickangle": -45
            },
            "yaxis": {
                "automargin": True
            },
            # 'activeshape': {'fillcolor': THEME['line_chart_color']}, # doesnt work
            "font": {
                "color": THEME["dark_color"],
                "family": THEME["font_family"],
                "size": THEME["label_font_size"],
            },
            "plot_bgcolor": THEME["background_color"],
            "paper_bgcolor": THEME["background_color"],
            "hovermode": "closest",
            "hoverlabel": {
                "bgcolor": THEME["label_background_color"],
                "font": {
                    "color": THEME["dark_color"],
                    "family": THEME["font_family"],
                    "size": THEME["label_font_size"],
                },
            },
        },
    )


def set_default_theme():
    """
        Sets the default theme to be a combination of the
        'plotly_white' theme and our custom theme.
    """
    # TODO : Set default theme
    pio.templates.default = "plotly_white+mytemplate"
