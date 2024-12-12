# MilitaryHierarchySimulator
It processes a military hierarchy and generates a KML file for visualizing the structure on a map (e.g., Google Earth). The hierarchy is structured into multiple levels (Force, Army, Division, Brigade, and Regiment), and geographic coordinates (latitude and longitude) are assigned to each unit. Here's a detailed breakdown of the code:

1. Hierarchical Structure
The hierarchy is built using classes, representing different levels:

Unidade:

A base class for units with attributes like name, level, unique ID, coordinates (latitude and longitude), image link, and subordinates.
Includes methods like adicionar_subordinado (to add subordinates) and gerar_coordenadas (to distribute subordinates in a circular pattern around a base unit).
Subclasses:

Specific classes for each level:
Forca (Force): Topmost level.
Exercito (Army), Divisao (Division), Brigada (Brigade), Regimento (Regiment): Represent progressively lower levels in the hierarchy.
Each level can recursively have subordinates, enabling the creation of a deep hierarchical structure.

2. Helper Functions
gerar_coordenadas_circulo
Generates geographic coordinates arranged in a circular pattern around a base coordinate.
Uses trigonometric functions (sin and cos) to compute positions, distributing them evenly in a circle with a given radius.
buscar_coordenadas
Fetches coordinates (latitude and longitude) for a city from the cidades_df DataFrame based on its name.
3. Data Processing
processar_hierarquia
Constructs the hierarchical structure based on two input DataFrames:

df_ativas: Contains details about military units (e.g., names, associated cities, and image links).
cidades_df: Contains city names and their geographic coordinates.
Steps:

Reads unit names for each hierarchical level (Force, Army, Division, Brigade, Regiment).
Fetches coordinates for the cities associated with each unit.
Builds the hierarchy recursively, adding subordinates and adjusting coordinates:
Lower-level units inherit coordinates from higher levels if not explicitly defined.
Coordinate Adjustment
Coordinates in the city DataFrame are fixed to ensure they are in the correct floating-point format (replacing commas with dots).
4. Generating Coordinates
gerar_coordenadas_todos_niveis
Assigns geographic coordinates to all units at all hierarchical levels.
Starts from the top level (Force) and distributes subordinates in circles, progressively reducing the radius for lower levels.
5. Generating the KML File
gerar_kml_com_camadas
Creates a KML file with separate layers (folders) for each hierarchical level (Army, Division, Brigade, Regiment).

For each unit:

Adds a KML point with its coordinates, name, level, and description (including its subordinates and an optional image link).
Groups points into layers based on the level.
Point Description:

Contains details like:
Unit name.
Level and unique ID.
Coordinates (latitude and longitude).
Higher-level hierarchy and subordinates.
Image (if available).
6. DataFrame Integration
The DataFrames are loaded from ODS files (spreadsheets).
df_ativas: Contains hierarchical information about military units.
cidades_df: Contains geographic coordinates of cities.
Data Correction
Coordinates in the city DataFrame are fixed to ensure consistent formatting (converted from strings with commas to floats with dots).
7. Main Execution Flow
Loads the data from the spreadsheets into DataFrames.
Processes the military hierarchy using processar_hierarquia.
Assigns geographic coordinates to all hierarchical levels using gerar_coordenadas_todos_niveis.
Generates a KML file with hierarchical layers using gerar_kml_com_camadas.
Prints debug information about the DataFrames for validation.
Outputs
KML File (unidades.kml):
Can be opened in Google Earth to visualize the military hierarchy geographically.
Debug Messages:
Includes details about the creation of units and the coordinates assigned to them.
Applications
Geographic visualization of hierarchical structures (e.g., military organizations).
Strategic planning and geographic analysis.
Integration with GIS (Geographic Information Systems) tools for advanced mapping.
