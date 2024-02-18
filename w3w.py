import what3words
import pandas as pd

geocoder = what3words.Geocoder("6DPCJIH7")

#uses W3W address to get latitude and longitude
sf_df= pd.read_excel("coord_input.xlsx" )

length_df = len(sf_df['Name'])

southwest_long = [0]*length_df
southwest_lat = [0]*length_df
northeast_long = [0]*length_df
northeast_lat = [0]*length_df

for j in range(length_df):

    result = geocoder.convert_to_coordinates(sf_df['W3W'][j])

    southwest = result['square']['southwest']
    northeast = result['square']['northeast']

    southwest_long[j] = southwest['lng']
    southwest_lat[j] = southwest['lat']

    northeast_long[j] = northeast['lng']
    northeast_lat[j] = northeast['lat']

new_data = {'Southwest Long': southwest_long, 'Southwest  Lat': southwest_lat, 'Northeast Long':northeast_long, 'Northeast Lat':northeast_lat}

sf_df = sf_df.assign(**new_data)

sf_df.to_excel("coord_output.xlsx")
