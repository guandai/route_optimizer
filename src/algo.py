import googlemaps
import polyline
import folium
import os

# Replace with your actual Google Maps API Key
API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

def process_algo(addresses):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=API_KEY)

    # Define the origin, destination, and waypoints
    origin = addresses[0]
    destination = addresses[-1]
    waypoints = addresses[1:-1]

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
        raise ValueError("No route found.")

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
        waypoint_location = leg['end_location']
        if idx < len(optimized_waypoints):
            waypoint_address = optimized_waypoints[idx]
            folium.Marker(
                location=[waypoint_location['lat'], waypoint_location['lng']],
                popup=waypoint_address,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(route_map)
        else:
            # Destination marker
            folium.Marker(
                location=[waypoint_location['lat'], waypoint_location['lng']],
                popup='Destination',
                icon=folium.Icon(color='red')
            ).add_to(route_map)

    # Save the map to an HTML file in the static folder
    output_file = 'static/optimized_route_map.html'
    route_map.save(output_file)

    print("Map has been saved to 'optimized_route_map.html'")
    return 'optimized_route_map.html'
