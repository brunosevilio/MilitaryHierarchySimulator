import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
from pykml import parser
import zipfile
import os
import ast  # To safely evaluate strings as dictionaries
from lxml import etree  # Required for PyKML

# Paths to files
municipality_file = "Data_Pop_Age_Name.ods"
kmz_file = "Polygon.kmz"
kml_extracted_file = "2840_extracted.kml"  # Temporary file for extracted KML

# Step 1: Extract the KMZ file to a KML
with zipfile.ZipFile(kmz_file, 'r') as kmz:
    # Extract the first KML file found in the KMZ
    for file_name in kmz.namelist():
        if file_name.endswith('.kml'):
            kmz.extract(file_name, ".")  # Extract KML in the current directory
            os.rename(file_name, kml_extracted_file)  # Rename for consistent naming
            break

# Step 2: Load municipality data
municipalities = pd.read_excel(municipality_file, sheet_name = 'Municipio', engine = 'odf')

# Extract latitude and longitude from the format {'lat': -23.5475, 'lon': -46.63611}
def extract_coordinates(coord_str):
    try:
        coord_dict = ast.literal_eval(coord_str)  # Convert string to dictionary
        return coord_dict['lat'], coord_dict['lon']
    except (ValueError, KeyError, SyntaxError):
        return None, None

municipalities['Latitude'], municipalities['Longitude'] = zip(
    *municipalities['Coordenadas'].apply(extract_coordinates)
)

# Remove entries with invalid coordinates
municipalities = municipalities.dropna(subset=['Latitude', 'Longitude'])

# Create a GeoDataFrame for municipalities
municipality_gdf = gpd.GeoDataFrame(
    municipalities,
    geometry=[Point(xy) for xy in zip(municipalities['Longitude'], municipalities['Latitude'])],
    crs="EPSG:4326"  # WGS 84 coordinate system
)

# Step 3: Use PyKML to parse the KML and extract the polygon
with open(kml_extracted_file, 'rb') as file:  # Open in binary mode
    kml_content = file.read()

root = parser.fromstring(kml_content)  # Pass bytes to fromstring

# Extract polygon coordinates (assumes simple KML structure)
coordinates = root.Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
coords_list = [
    tuple(map(float, coord.split(',')))
    for coord in coordinates.split()
]

# Convert coordinates to a Shapely Polygon
polygon = Polygon(coords_list)

# Step 4: Filter municipalities within the polygon
filtered_municipalities = municipality_gdf[municipality_gdf.geometry.within(polygon)]

# Print filtered municipalities
print("\n--- Filtered Municipalities ---")
print(filtered_municipalities)

# Save the filtered results to a new file
filtered_municipalities.to_excel("Filtered_Pop_Municipio.ods", sheet_name = 'Main',engine='odf', index=False)

# Clean up the extracted KML file
if os.path.exists(kml_extracted_file):
    os.remove(kml_extracted_file)

print("\n--- Process Completed: Filtered municipalities saved in 'Filtered_Pop_Municipio.ods' ---")


import pandas as pd
import simplekml

# Path to the filtered data file
filtered_municipalities_file = "Filtered_Pop_Municipio.ods"

# Load the data
filtered_municipalities = pd.read_excel(filtered_municipalities_file, engine='odf')

# Ensure columns have the correct format
filtered_municipalities['Latitude'] = filtered_municipalities['Latitude'].apply(
    lambda x: float(str(x).replace(',', '.'))
)
filtered_municipalities['Longitude'] = filtered_municipalities['Longitude'].apply(
    lambda x: float(str(x).replace(',', '.'))
)

# Create a KML object
kml = simplekml.Kml()

# Add a marker for each city
for _, row in filtered_municipalities.iterrows():
    name = row['Nome']
    population = row['Pop']
    latitude = row['Latitude']
    longitude = row['Longitude']

    # Create a marker
    point = kml.newpoint(
        name=name,
        description=f"População: {population:,}",
        coords=[(longitude, latitude)]  # Note: Longitude first, then Latitude
    )

    # Optional: Customize marker style
    point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
    point.style.iconstyle.scale = 1.2  # Adjust marker size

# Save the KML file
output_kml_file = "Filtered_Municipalities.kml"
kml.save(output_kml_file)

print(f"KML file created successfully: {output_kml_file}")
