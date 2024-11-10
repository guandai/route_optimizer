import googlemaps
import polyline
import folium

# Replace with your actual Google Maps API Key
API_KEY = "AIzaSyCkzIG1-kS8qV2Wv8u56MWMStbYiMZ7pHU"

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Define the origin, destination, and waypoints
origin = '11350 NW 25th St Ste 100, Sweetwater, FL 33172-1870, US'
destination = '10813 NW 30th St WEB 36503, Doral, FL 33172-5068, US'
waypoints = [
    '10000 NW 17th St Bays 11-17 CAL42967, Doral, FL 33172-2229, US',
    '10000 NW 17 St Ste 103, Bays 11-17 CAL483357, Doral, FL 33172, US',
    '1345 NW 98th Ct, Unit 2 RNB BGA 14391, Miami, FL 33172-3049, US',
    '1345 NW 98TH CT UNITZ FBC71086, Doral, FL 33172-2779, US',
    '1345 NW 98TH CT UNIT 2 AEL, Doral, FL 33172, US'
]

# Request directions with optimized waypoints
directions_result = gmaps.directions(
    origin=origin,
    destination=destination,
    waypoints=waypoints,
    optimize_waypoints=True,
    mode='driving'
)

# Check if the response is valid
if not directions_result:
    print("No route found.")
    exit(1)

# Get the optimized waypoint order
optimized_order = directions_result[0]['waypoint_order']
print("Optimized waypoint order:", optimized_order)

# Reorder waypoints based on optimized order
optimized_waypoints = [waypoints[i] for i in optimized_order]
print("Visit waypoints in this order:")
for address in optimized_waypoints:
    print(address)

# Extract the polyline from the response
overview_polyline = directions_result[0]['overview_polyline']['points']

# Decode the polyline into latitude and longitude coordinates
route_coordinates = polyline.decode(overview_polyline)

# Create a map centered around the starting point
start_location = directions_result[0]['legs'][0]['start_location']
map_center = [start_location['lat'], start_location['lng']]
route_map = folium.Map(location=map_center, zoom_start=13)

# Add the route to the map
folium.PolyLine(route_coordinates, color='blue', weight=5, opacity=0.8).add_to(route_map)

# Add markers for origin, destination, and waypoints
# Origin marker
folium.Marker(
    location=[start_location['lat'], start_location['lng']],
    popup='Origin',
    icon=folium.Icon(color='green')
).add_to(route_map)

# Waypoint markers
for idx, leg in enumerate(directions_result[0]['legs']):
    # Skip the last leg to avoid adding the destination twice
    if idx == len(directions_result[0]['legs']) - 1:
        break
    waypoint_location = leg['end_location']
    waypoint_address = optimized_waypoints[idx]
    folium.Marker(
        location=[waypoint_location['lat'], waypoint_location['lng']],
        popup=waypoint_address,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(route_map)

# Destination marker
end_location = directions_result[0]['legs'][-1]['end_location']
folium.Marker(
    location=[end_location['lat'], end_location['lng']],
    popup='Destination',
    icon=folium.Icon(color='red')
).add_to(route_map)

# Save the map to an HTML file
route_map.save('optimized_route_map.html')

print("Map has been saved to 'optimized_route_map.html'")
