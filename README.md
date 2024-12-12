# Military Hierarchy Simulator: Geospatial Visualization

The Military Hierarchy Simulator is a platform designed for geospatial hierarchical simulation and visualization, enabling the organization and representation of complex military or organizational structures. By processing data from predefined .ods tables, the system integrates hierarchical relationships, location information, and images to provide detailed visualizations in KML files. These files facilitate realistic simulations of geographic military organizational management.

System Overview
Key Features
Hierarchical Representation: Models military or organizational hierarchies from forces to regiments, with plans to expand into finer details like battalions and squads.
Data Integration: Processes data from spreadsheets (.ods) for geographic and hierarchical information.
Geospatial Visualization: Generates KML files to visualize hierarchical structures in tools like Google Earth.
Automatic and Manual Coordinates: Assigns geographic coordinates explicitly (based on city data) or generates them automatically for realistic positioning.
Applications
Games and Simulations: Create geospatial representations of military or administrative units.
Operational Planning: Visualize organizational structures for strategic decision-making.
Geospatial Analysis: Integrate with GIS tools for advanced mapping and planning.
Hierarchical Scope
Upper Hierarchy
The upper hierarchy models central organizational structures from the armed forces down to regiments.

1. Force
Description: The highest unit, defining the scope and function of subordinate units (e.g., Air Force, Navy).
Coordinates: None directly assigned.
Subordinates: Armies.
2. Army (Level 8)
Description: Units with fixed geographic bases (headquarters city). All armies within a force share the same scope and function.
Coordinates: Based on a designated city.
Subordinates: Divisions (homogeneous in scope and function).
3. Division (Level 8)
Description: Subordinate to an army, inheriting or defining its own coordinates. Divisions are homogeneous and manage heterogeneous brigades.
Coordinates: Explicit or inherited.
Subordinates: Brigades.
4. Brigade (Level 7)
Description: Subordinate to a division, inheriting or defining its coordinates. Brigades may differ in scope (offensive, defensive, or support).
Coordinates: Derived from the division or explicitly assigned.
Subordinates: Regiments.
5. Regiment (Level 6)
Description: The terminal unit in the upper hierarchy, composed of troops with specific functions (e.g., Artillery, Infantry).
Coordinates: Generated in circular formations around the brigade.
Subordinates: None in this system.
Lower Hierarchy (Future Scope)
The lower hierarchy expands on regiments, breaking them into smaller units like battalions and squads:

Regiment (Level 5): Formed by battalions.
Battalion (Level 4): Formed by companies.
Company (Level 3): Formed by platoons.
Platoon (Level 2): Formed by squads.
Squad (Level 1): Composed of individuals with diverse roles.
This future system will integrate citizen data, assigning individuals to roles based on attributes and detailing leadership and troop composition.

Core Components
1. Hierarchical Relationships
The system organizes units hierarchically:

Begins with the Force and branches down to Regiments.
Attributes assigned to each unit include:
Name.
Level.
Unique Identifier.
Coordinates (Latitude/Longitude).
Image Link.
Subordinates.
2. Coordinate Management
Coordinates can be:

Explicit: Linked to real cities from the city dataset.
Automatically Generated: Circular formations around superior units, adhering to a defined radius for realism.
3. Data Integration
The system uses two primary DataFrames:

df_ativas: Contains hierarchical unit information (names, associated cities, images).
cidades_df: Contains city names and geographic coordinates.
Data corrections include:

Formatting coordinates (e.g., converting commas to dots for consistency).
4. Geospatial Visualization
The system generates KML files organized by hierarchical levels, with structured navigation and detailed descriptions for each unit.

KML Point Features
Unit name, level, and unique ID.
Coordinates (latitude and longitude).
Description of higher-level units and subordinates.
Optional image link.
Functional Workflow
1. Hierarchy Construction
Class Structure
Unidade: Base class for all units, with attributes like name, level, unique ID, coordinates, and subordinates.
Subclasses: Specialized classes for each level:
Forca (Force).
Exercito (Army).
Divisao (Division).
Brigada (Brigade).
Regimento (Regiment).
2. Helper Functions
gerar_coordenadas_circulo
Generates coordinates in a circular pattern using trigonometric functions (sin, cos).
buscar_coordenadas
Retrieves coordinates for a city from the cidades_df DataFrame.
3. Hierarchy Processing
processar_hierarquia
Builds the hierarchical structure from df_ativas and cidades_df.
Steps:
Reads unit names and hierarchical levels.
Fetches associated city coordinates.
Constructs the hierarchy, adding subordinates and inheriting coordinates as needed.
4. Coordinate Assignment
gerar_coordenadas_todos_niveis
Assigns geographic coordinates to all levels:
Starts from the top level (Force).
Distributes subordinates in circular formations, reducing the radius for each lower level.
5. KML File Generation
gerar_kml_com_camadas
Creates a KML file with layers for each hierarchical level (e.g., Army, Division, Brigade).
Steps:
Adds KML points with attributes and descriptions.
Groups points into layers by level.
Execution and Outputs
Execution Flow
Load data from .ods spreadsheets into DataFrames.
Process the hierarchy using processar_hierarquia.
Assign coordinates to all units using gerar_coordenadas_todos_niveis.
Generate the KML file with gerar_kml_com_camadas.
Debug and validate outputs.
Outputs
KML File (unidades.kml):

Visualizes the military hierarchy geographically.
Compatible with Google Earth for detailed exploration.
Debug Information:

Logs details about unit creation and coordinate assignment.
Example Hierarchy
Force
Name: Air Force.
Coordinates: None.
Subordinates: Armies.
Army
Name: Northern Air Force.
Coordinates: Strategic city.
Subordinates: Divisions.
Division
Name: Northeast Wing.
Coordinates: Defined or generated automatically.
Subordinates: Brigades.
Brigade
Name: 4th Fighter Aviation Group.
Coordinates: Derived from the division or explicitly assigned.
Subordinates: Regiments.
Regiment
Name: 6th Air Squadron.
Coordinates: Circularly generated around the brigade.
This organized, optimized text provides a structured and detailed description of the Military Hierarchy Simulator, highlighting its functionality, components, and execution process.
