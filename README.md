# MilitaryHierarchySimulator
This system is a platform for geospatial hierarchical simulation and visualization designed to organize and represent complex military or organizational structures. It processes data from various hierarchical levels (such as forces, armies, divisions, brigades, and regiments) using predefined tables in .ods format, integrating location information, images, and hierarchical relationships. The main goal is to provide a detailed visualization of these structures in KML files, enabling realistic simulations of geographic military organizational management.

The system accommodates the diversity of military organizational models and aims to ensure realism and coherence in its representation. The military hierarchy modeled in the system is divided into two main scopes:

Upper Hierarchy
The upper hierarchy defines the central organizational structure, from the armed forces down to regiments. It is organized as follows:

Force:

Description: The highest unit, distinguishing the scope and function of subordinate units (e.g., Air Force, Navy). It does not have directly assigned geographic coordinates.
Subordinates: Armies.
Army (Level 8):

Description: A unit with a fixed geographic base (headquarters city) defined by the city name. All armies within a single force share the same scope and function.
Subordinates: Divisions (homogeneous in scope and function).
Division (Level 8):

Description: A unit subordinate to an army, inheriting or defining its own coordinates. Divisions are homogeneous and organize heterogeneous brigades.
Subordinates: Brigades.
Brigade (Level 7):

Description: A unit subordinate to a division, inheriting or defining its coordinates. Brigades differ in scope and function, and may be offensive, defensive, or support brigades, depending on their composition.
Subordinates: Regiments.
Regiment (Level 6):

Description: The terminal basic unit in the functional system. Internally homogeneous, composed of troops with specific functions (e.g., Artillery Regiment, Motorized Infantry Regiment).
Subordinates: None within the functional scope of this system.
Lower Hierarchy
The lower hierarchy describes the organizational details of units, expanding the regiment level into smaller structures such as battalions and squads. This scope will be developed in a future system and will be based on:

Regiment (Level 5): Formed by homogeneous battalions.
Battalion (Level 4): Formed by homogeneous companies.
Company (Level 3): Formed by homogeneous platoons.
Platoon (Level 2): Formed by homogeneous squads.
Squad (Level 1): Formed by individuals with diverse roles assigned to different ranks.
This system will allow the assignment of citizens (generated in the Citizen Generation System) to ranks and positions based on individual attributes, complementing the visualization with details of leadership and total troop numbers.

Applications
Games and Simulations: Creating geospatial representations of military or administrative units.
Operational Planning: Visualizing organizational structures for strategic planning.
Core Components of the Functional System
Hierarchical Relationships:

The system organizes units hierarchically, starting from the primary unit (Force) and branching down to terminal levels (Regiments).
Each unit is assigned attributes such as name, level, unique identifier, coordinates (latitude and longitude), associated image, and subordinates, originating from the .ods table.
Coordinates:

Explicit Coordinates: Associated with real cities through tables.
Automatic Generation: For units without defined coordinates, circular formations are created around the superior unit, respecting a determined radius.
Geographical Data Location and Integration:

The system uses a DataFrame containing cities and their geographic coordinates, associating them with units like armies, divisions, and brigades.
Coordinate data is processed and corrected to ensure accuracy and compatibility with geospatial systems.
Generation and Visualization:

Generates KML files with layers organized by hierarchical level, enabling clear and structured navigation.
Each point in the KML includes detailed descriptions with hierarchical information, coordinates, and associated images.
Example Hierarchy
Level: Force

Name: Air Force
Coordinates: None
Subordinates: Armies
Level: Army

Name: Northern Air Force
Coordinates: Associated with a strategic city.
Subordinates: Divisions
Level: Division

Name: Northeast Wing
Coordinates: Defined or automatically generated around the superior unit.
Subordinates: Brigades
Level: Brigade

Name: 4th Fighter Aviation Group
Coordinates: Derived from the division or directly assigned.
Subordinates: Regiments
Level: Regiment

Name: 6th Air Squadron
Coordinates: Generated in a circle around the brigade.
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
