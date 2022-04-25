import plotly.graph_objects as go
import plotly.express as px
from template import vessel_color_code
from hover_template import hover_regionBar

def get_sankey_fig(df_nodes, df_links):
    # Sankey plot setup
    data_trace = dict(
        type="sankey",
        domain=dict(x=[0, 1], y=[0, 1]),
        orientation="h",
        valueformat=".0f",
        node=dict(
            pad=10,
            # thickness = 30,
            line=dict(color="black", width=0),
            label=df_nodes["Label"].dropna(axis=0, how="any"),
            color=df_nodes["Color"],
            # color="#897F76"
        ),
        link=dict(
            source=df_links["Source"].dropna(axis=0, how="any"),
            target=df_links["Target"].dropna(axis=0, how="any"),
            value=df_links["Value"].dropna(axis=0, how="any"),
            color=df_links["Link Color"].dropna(axis=0, how="any"),
        ),
    )

    fig = go.Figure(data=[data_trace])

    fig.update_layout(title_text="Region view", clickmode="event+select")

    return fig


def get_bar_chart(df_region_connectivity, region):
    
    fig = go.Figure(
        data = go.Bar(
            x=df_region_connectivity["Arrival Region"],
            y=df_region_connectivity["Count"],
            ),
        layout={'title':region}
        )


    # Layout
    fig.update_traces(marker_color=vessel_color_code['all'])
    fig.update_xaxes(title_text='Region')
    fig.update_yaxes(title_text='Number of Trips from Selected Region')

    # Hover data
    fig.update_traces(hovertemplate=hover_regionBar())
    
    return fig
