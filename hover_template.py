'''
    Provides the template for the tooltips.
'''

def hover_overview_harbour():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    harbour = "<span style=\"font-weight: bold\">Harbour: </span> <span style=\"font-weight: normal\">%{customdata[0]}</span> <br><br>"
    region = "<span style=\"font-weight: bold\">Region: </span> <span style=\"font-weight: normal\">%{customdata[4]}</span> <br>"
    lat = "<span style=\"font-weight: normal\">Latitude: </span> <span style=\"font-weight: normal\">%{customdata[2]:.2f}</span> <br>"
    lon = "<span style=\"font-weight: normal\">Longitude: </span> <span style=\"font-weight: normal\">%{customdata[3]:.2f}</span> <br><br>"
    connectivity1 = "<span style=\"font-weight: bold\">Harbours Connected: </span> <span style=\"font-weight: normal\">%{customdata[1]:,}</span> <br>"
    connectivity2 = "<span style=\"font-weight: bold\">Regions Connected: </span> <span style=\"font-weight: normal\">%{customdata[5]:,}</span> <br>"
    frequency = "<span style=\"font-weight: bold\">Frequency: </span> <span style=\"font-weight: normal\">%{customdata[6]:,}</span> <br>"
    deadweight = "<span style=\"font-weight: bold\">DeadWeight Tonnage: </span> <span style=\"font-weight: normal\">%{customdata[7]:,}</span> <br>"

    return harbour+region+lat+lon+connectivity1+connectivity2+frequency+deadweight+"<extra></extra>"

def hover_perRouteView1():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    year = "<span style=\"font-weight: bold\">Year: </span> <span style=\"font-weight: normal\">%{x}</span><br>"
    vessel = "<span style=\"font-weight: bold\">Vessel Type: </span> <span style=\"font-weight: normal\"> All</span><br>"
    trips = "<span style=\"font-weight: bold\">Quantity of Trips: </span> <span style=\"font-weight: normal\">%{y}</span> <br><br>"

    return vessel+year+trips+"<extra></extra>"

def hover_perRouteView2():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    year = "<span style=\"font-weight: bold\">Year: </span> <span style=\"font-weight: normal\">%{x}</span><br>"
    vessel = "<span style=\"font-weight: bold\">Vessel Type: </span> <span style=\"font-weight: normal\">%{meta}</span><br>"
    trips = "<span style=\"font-weight: bold\">Average Trip Duration in Hours: </span> <span style=\"font-weight: normal\">%{y:.1f}</span> <br><br>"

    return vessel+year+trips+"<extra></extra>"

def hover_harbourView_instance():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    
    harbour = "<span style=\"font-weight: bold\">Connected Harbour: </span> <span style=\"font-weight: normal\">%{y}</span> <br>"
    date = "<span style=\"font-weight: bold\">At: </span> <span style=\"font-weight: normal\">%{x}</span> <br>"
    

    return harbour+date+"<extra></extra>"


def hover_harbourView_sunbusrt():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    
    big_cat = "<span style=\"font-weight: bold\">Category: </span> <span style=\"font-weight: normal\">%{label}</span> <br>"
    freq = "<span style=\"font-weight: bold\">Frequency: </span> <span style=\"font-weight: normal\">%{value}</span> <br>"
    return big_cat+freq+"<extra></extra>"

def hover_harbourView_line():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    freq = "<span style=\"font-weight: bold\">Frequency: </span> <span style=\"font-weight: normal\">%{y}</span> <br>"
    date = "<span style=\"font-weight: bold\">Date: </span> <span style=\"font-weight: normal\">%{x}</span> <br>"
    
    return freq+date+"<extra></extra>"

def hover_harbourView_capacity():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    
    Date = "<span style=\"font-weight: bold\">Frequency: </span> <span style=\"font-weight: normal\">%{x}</span> <br>"
    deadweight = "<span style=\"font-weight: bold\">DeadWeight Tonnage: </span> <span style=\"font-weight: normal\">%{y}</span> <br>"
    return deadweight+Date+"<extra></extra>"

def hover_regionBar():
    '''
        Sets the template for the hover tooltips.
        
        Contains many labels, followed by their corresponding
        value and units where appropriate.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    
    region = "<span style=\"font-weight: bold\">Region: </span> <span style=\"font-weight: normal\">%{x}</span> <br>"
    notrips = "<span style=\"font-weight: bold\">No. of Trips: </span> <span style=\"font-weight: normal\">%{y:,}</span> <br>"
    return region+notrips+"<extra></extra>"
