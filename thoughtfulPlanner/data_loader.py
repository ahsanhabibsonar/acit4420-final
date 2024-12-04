#data_loader.py
import csv

def load_streets(file_path):
    streets = {}
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Street_Name']
                latitude = float(row['Latitude'])
                longitude = float(row['Longitude'])  # Note: 'Longtitude' matches your data
                streets[name] = (latitude, longitude)
        return streets
    except FileNotFoundError:
        print("Error: The file was not found. Please provide the correct path.")
    except PermissionError:
        print("Error: Insufficient permissions to read the file.")

#######################################


class InvalidTransportModeError(Exception):
    pass

def validate_mode(mode):
    valid_modes = ["Bus", "Train", "Bicycle", "Walking"]
    if mode not in valid_modes:
        raise InvalidTransportModeError(f"Invalid transport mode: {mode}")


def load_transport_modes(file_path):
    transport_modes = {}
    default_colors = {
        "Bus": "blue",
        "Train": "green",
        "Bicycle": "goldenrod",
        "Walking": "red"
    }
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mode = row["Modes of Transport"]
            validate_mode(mode)  # Validate globally defined modes
            transport_modes[mode] = {
                "Speed_kmh": float(row["Speed_kmh"]),
                "Cost_per_km": float(row["Cost_per_km"]),
                "Transfer_Time_min": int(row["Transfer_Time_min"]),
                "Color": default_colors.get(mode, "gray")
            }
    return transport_modes

#Defining add cooordiantes using decorator 
from geopy.distance import geodesic

def load_streets_decorator(file_path):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Load the street data
            try:
                address_data = load_streets(file_path)
            except FileNotFoundError:
                print(f"File {file_path} not found. Proceeding with default data.")
                address_data = {}

            # Ensure Yeouido is included
            address_data["Yeouido"] = (37.526, 126.929)
            # Yangae-daero 37.4833,127.0322
            #Hannam-daero,37.5340(x axis),127.0026
           
           #New Yeouido coordinates
            #address_data["Yeouido"] = (37.4979, 127.0026)
            

            # Pass the loaded address_data to the decorated function
            return func(address_data, *args, **kwargs)
        return wrapper
    return decorator


@load_streets_decorator("address_data.csv")
def add_coordinates(address_data, max_distance_km=20):
    """
    Adds user-provided coordinates to the in-memory address data.
    """
    yeouido = address_data.get("Yeouido")
    print("\n--- Add New Coordinates ---")
    print("Sample input for guidance:")
    print("Latitude: 37.5450, 37.5290 (Example for Seoul)")
    print("Longitude: 127.0400, 127.0500 (Example for Seoul)")
    print("Streets Name: Teheran-ro, Seongdong-gu\n")

    while True:
        start = input("Do you want to add a new coordinate? (y/n): ").strip().lower()
        if start != "y":
            break
        try:
            latitude = float(input("Enter latitude (e.g., 37.5450, 37.5290): "))
            longitude = float(input("Enter longitude (e.g., 127.0400, 127.0500): "))
            street_name = input("Enter street name (leave blank for default): ").strip()

            # Validate coordinates
            distance = geodesic((latitude, longitude), yeouido).km
            if distance > max_distance_km:
                print(f"Error: Coordinates are {distance:.2f} km away from Yeouido, exceeding the limit of {max_distance_km} km.")
                continue

            # Generate default names
            street_id = len(address_data) - 1
            street_name = street_name or f"Street_{street_id + 1}"

            # Update address_data
            address_data[street_name] = (latitude, longitude)
            print(f"Success: Added {street_name} at ({latitude}, {longitude}) within {distance:.2f} km of Yeouido.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    return address_data



