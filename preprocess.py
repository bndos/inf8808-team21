import pandas as pd
import datetime as dt
import numpy as np
import random
import plotly.express as px

"""
    Contains some functions to preprocess the data used in the visualisation.
"""

def identify_major_vessel_type(vessel_type):
    
    if 'merchant' in vessel_type.lower():
        major_vessel_type = 'Merchant'
    elif 'landing craft' in vessel_type.lower():
        major_vessel_type = 'Landing Craft'
    elif 'tug' in vessel_type.lower():
        major_vessel_type = 'Tug'
    elif 'excursion passenger' in vessel_type.lower() or 'cruise ' in vessel_type.lower():
        major_vessel_type = 'Passenger'
    elif 'yacht' in vessel_type.lower() or 'yatch' in vessel_type.lower() or 'yacth'in vessel_type.lower():
        major_vessel_type = 'Yacht'
    elif 'barge' in vessel_type.lower():
        major_vessel_type = 'Barge'
    elif 'trawler' in vessel_type.lower():
        major_vessel_type = 'Trawler'
    elif 'fish' in vessel_type.lower() or 'crab' in vessel_type.lower() or 'shrimp' in vessel_type.lower() or 'lobster' in vessel_type.lower() or 'dragger' in vessel_type.lower():
        major_vessel_type = 'Fishing'
    else:
        major_vessel_type = 'Other/Unknown'
        
    return major_vessel_type
        

def load_data():
    url = "https://www.dropbox.com/s/d6jrkruu90b138g/TRIP.csv?dl=1"

    df_trip = pd.read_csv(url)

    # Simplify Vessel Type Info
    df_trip['Major Vessel Type'] = df_trip['Vessel Type'].map(identify_major_vessel_type)

    # Fix Harbour Names
    #def fix_name(harbour_name):
    #    harbour_name = harbour_name.lower()
    #    harbour_name = harbour_name.title()
    #    return harbour_name
    #df_trip['Arrival Hardour'] = df_trip['Arrival Hardour'].map(fix_name)
    #df_trip['Departure Hardour'] = df_trip['Departure Hardour'].map(fix_name)        
    return df_trip


def get_connectivity(trip_df):

    # Combining Departures with Arrivals
    arrival_df = trip_df[
        [
            "Arrival Hardour",
            "Departure Hardour",
            "Arrival Latitude",
            "Arrival Longitude",
            "Arrival Region",
            "DeadWeight Tonnage",
        ]
    ]
    arrival_df = arrival_df.set_axis(
        ["Hardour", "Connected Hardour", "lat", "lon", "region", "DeadWeight Tonnage"],
        axis=1,
    )

    departure_df = trip_df[
        [
            "Arrival Hardour",
            "Departure Hardour",
            "Departure Latitude",
            "Departure Longitude",
            "Departure Region",
            "DeadWeight Tonnage",
        ]
    ]
    departure_df = departure_df.set_axis(
        ["Connected Hardour", "Hardour", "lat", "lon", "region", "DeadWeight Tonnage"],
        axis=1,
    )

    result_df = pd.concat([arrival_df, departure_df])

    # Add Frequency
    df_frequency = result_df.value_counts("Hardour")
    df_frequency = df_frequency.reset_index()
    df_frequency = df_frequency.set_axis(["Hardour", "Frequency"], axis=1)

    # Add DeadWeight Tonnage
    result_df["DeadWeight Tonnage"] = result_df["DeadWeight Tonnage"].astype(float)
    df_tonnage = (
        result_df.groupby(["Hardour"])["DeadWeight Tonnage"].sum().reset_index()
    )

    result_df.drop_duplicates(
        ["Hardour", "Connected Hardour"], keep="last", inplace=True
    )

    # ?
    result_df["Qty_Harbours_Connected"] = result_df.groupby(["Hardour"])[
        "Connected Hardour"
    ].transform("count")
    result_df = result_df[["Hardour", "Qty_Harbours_Connected", "lat", "lon", "region"]]
    result_df.drop_duplicates(
        ["Hardour", "Qty_Harbours_Connected"], keep="last", inplace=True
    )
    result1_df = result_df
    result_df.loc[result_df["Hardour"] == "Virtual Harbour (Central Region)"]

    # Repeating the same for the regions
    arrival_df = trip_df[["Arrival Hardour", "Departure Region"]]
    arrival_df = arrival_df.set_axis(["Hardour", "Region"], axis=1)

    departure_df = trip_df[["Departure Hardour", "Arrival Region"]]
    departure_df = departure_df.set_axis(["Hardour", "Region"], axis=1)

    result_df = pd.concat([arrival_df, departure_df])
    result_df.drop_duplicates(["Hardour", "Region"], keep="last", inplace=True)

    result_df["Qty_Regions_Connected"] = result_df.groupby("Hardour").transform("count")
    result_df = result_df[["Hardour", "Qty_Regions_Connected"]]
    result_df.drop_duplicates(
        ["Hardour", "Qty_Regions_Connected"], keep="last", inplace=True
    )
    # result_df.loc[result_df['Hardour'] == 'Sackets Harbour']

    # Merging Data
    df_connectivity = pd.merge(result1_df, result_df, on=["Hardour"])
    df_overview_data = pd.merge(df_connectivity, df_frequency, on=["Hardour"])
    df_overview_data = pd.merge(df_overview_data, df_tonnage, on=["Hardour"])

    return df_overview_data

def get_overview_top10(df, mode):
    
    # Clean-up Virtual Harbours
    def isvirtual(harbour_name):
        if 'virtual' in harbour_name.lower():
            return True
        else:
            return False
    
    # Filter out Virtual Harbours
    df['isVirtual'] = df['Hardour'].map(isvirtual)
    df = df[df['isVirtual']!=True]
    
    # Column name
    if mode.lower() == 'connectivity':
        columnname = 'Qty_Harbours_Connected'
    elif mode.lower() == 'frequency':
        columnname = 'Frequency'
    else:
        columnname = 'DeadWeight Tonnage'
        
    # Get top 10
    df = df.sort_values(columnname, ascending=False).iloc[0:10]        
    
    # Output
    return df

def get_route_stats(df_trip, select_route):
    """
    Function to prepare the data for the visualization in Per Route View tab
    """

    # Route Name
    df_trip["route_name"] = (
        df_trip["Departure Hardour"] + " to " + df_trip["Arrival Hardour"]
    )

    # Filter dataframe
    df_route = df_trip[df_trip["route_name"] == select_route]

    # Simplify Vessel Type
    #df_route.loc[:, "Vessel Type"] = df_route["Vessel Type"].apply(
    #    lambda x: x.split(" ")[0]
    #)
    #df_route.loc[
    #    df_route["Vessel Type"] == "Tugs", "Vessel Type"
    #] = "Tug"  # Replacing Tugs for Tug

    # Get year
    df_route["year"] = df_route["Arrival Date"].apply(lambda x: int(x[0:4]))

    # Route duration
    df_route.loc[:, "dt_departure"] = df_route["Departure Date"].apply(
        lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
    )
    df_route.loc[:, "dt_arrival"] = df_route["Arrival Date"].apply(
        lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
    )
    df_route.loc[:, "route_duration"] = (
        df_route["dt_arrival"] - df_route["dt_departure"]
    )
    df_route.loc[:, "route_duration_hours"] = df_route["route_duration"].apply(
        lambda x: x.total_seconds() / 3600
    )

    # Quantity of Travel Occurrencies per Year
    df_RouteOccurrences = pd.DataFrame(df_route["year"].value_counts())
    df_RouteOccurrences.columns = ["route_occurrencies"]
    df_RouteOccurrences.sort_index(inplace=True)

    # Average Route duration per Year
    df_route_duration = pd.pivot_table(
        df_route,
        values="route_duration_hours",
        index="year",
        columns="Major Vessel Type",
        aggfunc="mean",
    )

    # Deadweight tonnage per Year
    df_route_merchant = df_route[df_route["Major Vessel Type"] == "Merchant"]

    return df_RouteOccurrences, df_route_duration, df_route_merchant


def load_region_connectivity(df_trip, region):
    region_connectivity_df = df_trip[['Departure Region', 'Arrival Region']]
    region_connectivity_df['Arrival Region'] = 'Arrival ' + region_connectivity_df['Arrival Region'].astype(str)

    region_connectivity_df = region_connectivity_df.groupby(['Departure Region', 'Arrival Region']).size().reset_index(name='Count')

    region_connectivity_df = region_connectivity_df.loc[region_connectivity_df['Departure Region'] == region]
    region_connectivity_df = region_connectivity_df.sort_values('Count', ascending=False)
    return region_connectivity_df

def load_sankey_data(df_trip):
    # Sankey

    departure_df = df_trip[["Departure Region", "Arrival Region"]]
    departure_df["Arrival Region"] = "Arrival " + departure_df["Arrival Region"].astype(
        str
    )

    departure_df = (
        departure_df.groupby(["Departure Region", "Arrival Region"])
        .size()
        .reset_index(name="Count")
    )
    node_df = departure_df[["Departure Region"]].set_axis(["Label"], axis=1)

    node_df = pd.concat(
        [
            node_df[["Label"]],
            departure_df[["Arrival Region"]].rename(
                columns={"Arrival Region": "Label"}
            ),
        ],
        ignore_index=True,
    )
    departure_df = departure_df.set_axis(["Source", "Target", "Value"], axis=1)
    node_df = node_df.drop_duplicates(keep="last").reset_index(drop=True)
    node_df["ID"] = node_df.index.tolist()
    departure_df["Source"] = departure_df["Source"].map(
        node_df.set_index("Label")["ID"]
    )
    departure_df["Target"] = departure_df["Target"].map(
        node_df.set_index("Label")["ID"]
    )

    node_df["Color"] = ["#7CC33C","#46B99D","#C225DA", "#ED9D12", "#31BDCE", "#FF0044", "#4A4EB5", "#4E504F", "#DFE01F",
                    "#DFE01F", "#7CC33C","#46B99D","#C225DA", "#ED9D12", "#31BDCE", "#4A4EB5", "#4E504F", "#FF0044"]

    departure_df["Link Color"] = [node_df["Color"][departure_df["Source"][i] % 9]
                                  for i in range(departure_df["Source"].count())]

    df_nodes = node_df
    df_links = departure_df

    return df_nodes, df_links

# Get seasons
def season_of_date(mydate):
    month = mydate.month
    season = month%12 // 3 + 1
    if season == 1:
        return 'winter'
    elif season == 2:
        return 'spring'
    elif season == 3:
        return 'summer'
    else:
        return 'autumn'

def get_harbour_list(df_trip):
    harbours = df_trip[['Arrival Hardour']].sort_values('Arrival Hardour')
    harbours.drop_duplicates(inplace=True)
    list_harbours = [harbour[0] for harbour in harbours.values.tolist()]
    return list_harbours

            
def harbour_data(df_trip, select_harbour):

    # Selected Harbour in dropdown menu
    #select_harbour = 'Montreal'

    # Filter dataframe
    df_harbour = df_trip[(df_trip['Departure Hardour']==select_harbour)|(df_trip['Arrival Hardour']==select_harbour)]

    # Assuming df has a date column of type `datetime`
    df_harbour['arrival_datetime'] = pd.to_datetime(df_harbour['Arrival Date'])
    df_harbour['season'] = df_harbour['arrival_datetime'].map(season_of_date)

    # To fix tug vs. tugs
    df_harbour.loc[:,'Vessel Type'] = df_harbour['Vessel Type'].apply(lambda x: x.replace('Tugs','Tug'))

    # Get major vessel type (to avoid subcategories of Merchant Vessels)
    for each in df_harbour.index:
        each_vessel = df_harbour.loc[each,'Vessel Type']
        if 'Merchant' in each_vessel:
            df_harbour.loc[each,'Major Vessel Type'] = 'Merchant'
        elif 'Tug' in each_vessel:
            df_harbour.loc[each,'Major Vessel Type'] = 'Tug'
        elif 'Excursion Passenger' in each_vessel:
            df_harbour.loc[each,'Major Vessel Type'] = ' ' 
        elif 'Barge' in each_vessel:
            df_harbour.loc[each,'Major Vessel Type'] = 'Barge' 
        else:
            df_harbour.loc[each,'Major Vessel Type'] = 'Others'      
            
    # Counts
    df_harbour_vessels = df_harbour.groupby(["Major Vessel Type", "Vessel Type"]).size().to_frame(name="Counts").reset_index()

    # Get Major Vessel Type
    i = len(df_harbour_vessels)
    for each in df_harbour_vessels["Major Vessel Type"].unique():
        if ' ' != each:
            i = i+1
            df_harbour_vessels.loc[i,"Vessel Type"] = each
            df_harbour_vessels.loc[i,"Major Vessel Type"] = ' '
            df_harbour_vessels.loc[i,"Counts"] = df_harbour_vessels['Counts'][df_harbour_vessels['Major Vessel Type']==each].sum()

    df_harbour['Major Vessel Type 2'] = df_harbour['Vessel Type'].apply(lambda x: x.split(' ')[0])
    df_harbour_seasons = df_harbour.groupby(["Major Vessel Type 2", "season"]).size().to_frame(name="Counts").reset_index()


    return df_harbour_vessels, df_harbour_seasons

def get_strip_df(df_trip,principal_harbour, depart=True, nb_hardour = 10):
  if depart:
    col_filter = 'Departure Hardour'
    connection_type = 'Arrival Hardour'
    date = 'Departure Date'
  else:
    col_filter = 'Arrival Hardour'
    connection_type = 'Departure Hardour'
    date = 'Arrival Date'

  df = df_trip[['Departure Hardour','Arrival Hardour',date,'Major Vessel Type','DeadWeight Tonnage']][df_trip[col_filter]==principal_harbour]
  top_linked_harbor = df[connection_type].value_counts().head(nb_hardour).keys()
  df = df[df[connection_type].isin(top_linked_harbor)]
  if depart:
    df=df.set_axis(['Hardour', 'Connected Hardour', 'Date', 'Major Vessel Type','DeadWeight Tonnage'], axis=1)
  else:
    df=df.set_axis(['Connected Hardour', 'Hardour', 'Date', 'Major Vessel Type','DeadWeight Tonnage'], axis=1)
  #df.loc[:,'Vessel Type'] = df['Vessel Type'].apply(lambda x: x.split(' ')[0])
  #df.loc[df['Vessel Type']=='Tugs','Vessel Type'] = 'Tug' # Replacing Tugs for Tug

  return df,top_linked_harbor

def get_sunburst_df(df_trip,Harbour_selected:str):
    df_xor = df_trip[['Arrival Hardour', 'Departure Hardour', 'Major Vessel Type', 'Vessel Type']][((df_trip['Departure Hardour']==Harbour_selected)&(df_trip['Arrival Hardour']!=Harbour_selected)|(df_trip['Departure Hardour']!=Harbour_selected)&(df_trip['Arrival Hardour']==Harbour_selected))]
    df_xor = df_xor.groupby(['Major Vessel Type','Vessel Type']).count()
    df_xor = df_xor['Arrival Hardour'].reset_index()#.set_axis(['Vessel Type', 'Frequency'],axis=1)
    df_xor['Frequency'] = df_xor['Arrival Hardour']
    #df_xor.loc[:,'Major Vessel Type'] = df_xor['Major Vessel Type'].apply(lambda x: x.replace('Tugs','Tug'))

    #for each in df_xor.index:
    #  each_vessel = df_xor.loc[each,'Vessel Type']
    #  if 'Merchant' in each_vessel:
    #    df_xor.loc[each,'Major Vessel Type'] = 'Merchant'
    #  elif 'Tug' in each_vessel:
    #    df_xor.loc[each,'Major Vessel Type'] = 'Tug'
    #  elif 'Excursion Passenger' in each_vessel:
    #    df_xor.loc[each,'Major Vessel Type'] = ' ' 
    #  elif 'Barge' in each_vessel:
    #    df_xor.loc[each,'Major Vessel Type'] = 'Barge' 
    #  else:
    #    df_xor.loc[each,'Major Vessel Type'] = 'Others'  
     

    return df_xor

def get_line_df(df_trip,Harbour_selected):
    df_xor = df_trip[['Arrival Hardour', 'Departure Hardour', 'Major Vessel Type','Vessel Type','Arrival Date']][((df_trip['Departure Hardour']==Harbour_selected)&(df_trip['Arrival Hardour']!=Harbour_selected)|(df_trip['Departure Hardour']!=Harbour_selected)&(df_trip['Arrival Hardour']==Harbour_selected))]
    df_xor = df_xor[['Major Vessel Type','Vessel Type','Arrival Date']]
    #df_xor.loc[:,'Major Vessel Type'] = df_xor['Vessel Type'].apply(lambda x: x.replace('Tugs','Tug'))
    #for each in df_xor.index:
    #    each_vessel = df_xor.loc[each,'Vessel Type']
    #    if 'Merchant' in each_vessel:
    #        df_xor.loc[each,'Major Vessel Type'] = 'Merchant'
    #    elif 'Tug' in each_vessel:
    #        df_xor.loc[each,'Major Vessel Type'] = 'Tug'
    #    elif 'Excursion Passenger' in each_vessel:
    #        df_xor.loc[each,'Major Vessel Type'] = ' ' 
    #    elif 'Barge' in each_vessel:
    #        df_xor.loc[each,'Major Vessel Type'] = 'Barge' 
    #    else:
    #        df_xor.loc[each,'Major Vessel Type'] = 'Others' 

    df_xor['Date'] = df_xor['Arrival Date'].apply(lambda x: x[0:7])
    df_xor = df_xor.groupby(by=['Date','Major Vessel Type']).count()
    df_xor = ((df_xor.reset_index())[['Date','Major Vessel Type','Vessel Type']]).set_axis(['Date', 'Major Vessel Type',    'Frequency'],axis=1)
    return df_xor
