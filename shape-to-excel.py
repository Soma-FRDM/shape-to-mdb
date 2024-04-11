import geopandas as gpd
import pyodbc
from shapely import wkt
from shapely.geometry import LineString
import re

def insert_elementnames(conn):
    cursor = conn.cursor()

def calculate_length(line_string):
    # Parse the WKT representation into a LineString object
    #linestring_obj = wkt.loads(line_string)
    
    # Calculate the length of the LineString in meters
    length_meters = line_string.length
    
    return length_meters

def extract_number_before_mm(text):
    # Define the regex pattern to match the numerical part before "mm"
    pattern = r'(\d+(\.\d+)?)mm'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    # If the pattern is found, extract the numerical part before "mm"
    if match:
        return float(match.group(1))
    else:
        return 0  # If "mm" is not found, return 0
    
def insert_elements(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Element")
    element_columns = [column[0] for column in cursor.description]
    print("Column names for Element table:", element_columns)
    # Iterate through each row in the GeoDataFrame and insert data into the database
    for idx, row in gdf.iterrows():
        # Assuming the column names in the shapefile match the column names in the Access database
        # Change the column names as per your database schema
        element_id = idx  # ElementId starting at 1
        element_type = 1  # Assuming ElementType is always 1
        
        # Inserting into Element table
        query = "INSERT INTO Element ( ElementType, FromNodeId, ToNodeId) VALUES (?, ?, ?)"
        cursor.execute(query, ( element_type,0,0))

        # Inserting into ElementNameIdMap table
        element_name_id_query = "INSERT INTO ElementNameIdMap (idval, stringval) VALUES (?, ?)"
        cursor.execute(element_name_id_query, (element_id, 'Pi' + str(element_id+1)))

        efficiency = 1
        roughness = 6E-05
        friction_factor = 0.015
        gas_gravity = 0.600000024
        gas_flowing_temperature = 59.99996948
        number_parallel_pipes = 0
        heat_transfer_coeff = 0.22
        ambient_temperature = 59.99996948
        is_loop_switch_on = False
        material = 'Coated Steel'

        gas_pipe_query = """
        INSERT INTO GasPipe (
            ElementId, EquationTypeId, Length, Efficiency, Roughness, 
            FrictionFactor, GasGravity, GasFlowingTemperature, HeatTransferCoeff, 
            AmbientTemperature, OutsideDiameter, Material , UseODWallThickness
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(gas_pipe_query, (element_id, 0, row['geometry'].length, efficiency, roughness, friction_factor,
                                                gas_gravity, gas_flowing_temperature, heat_transfer_coeff, ambient_temperature,
                                                extract_number_before_mm(row['Diameter']), row['Material'], True))

        
    
    conn.commit()
    # Close the connection
    conn.close()


# Load the shapefile
shapefile_path = 'FSJ-Export/Distribution_Pipe_FSJ.shp'
gdf = gpd.read_file(shapefile_path)

# Get the list of column names
column_names = gdf.columns.tolist()

print(column_names)

conn1 = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Hydraulic Operating Manual\\FSJ\\Table Analysis\\Sandbox\\Trans-pipes.MDB')
insert_elements(conn1)



