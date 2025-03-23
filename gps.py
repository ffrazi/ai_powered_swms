import pandas as pd
from geopy.distance import geodesic
import geocoder


# Function to get the closest phone number based on current GPS location
def get_closest_phone_number(current_location, excel_file):
    # Load the Excel file
    df = pd.read_excel(excel_file)

    # Assuming the Excel has 'Phone' and 'GPS_Location' columns
    # GPS_Location is expected to be a string in the format 'lat, lon'
    phone_numbers = df['phone no.'].tolist()
    gps_locations = df['gps location'].tolist()

    closest_phone = None
    min_distance = float('inf')  # Initialize with a very large number

    for phone, location in zip(phone_numbers, gps_locations):
        # Convert the GPS location string to a tuple of floats (latitude, longitude)
        location = location.replace('(', '').replace(')', '').replace(' ', '')
        lat, lon = map(float,location.split(','))
        gps_coords = (lat, lon)
        
        # Calculate the distance between the current location and the entry's location
        distance = geodesic(current_location, gps_coords).meters
        
        if distance < min_distance:
            min_distance = distance
            closest_phone = phone
    
    return closest_phone, min_distance

# Function to get the current location of the device
def get_current_location():
    # Get the current location using geocoder
    g = geocoder.ip('me')  # Uses the public IP to get approximate location
    return (g.latlng[0], g.latlng[1])  # Returns (lat, lon)

# Example usage
#  # Example: Bengaluru, India (lat, lon)
current_location=get_current_location()
excel_file = 'image_data.xlsx'

phone_number, distance = get_closest_phone_number(current_location, excel_file)

if phone_number:
    print(f"The closest phone number is {phone_number}, located {distance:.2f} meters away.")
else:
    print("No phone number found.")