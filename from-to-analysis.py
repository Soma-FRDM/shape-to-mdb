import geopandas as gpd
from shapely.geometry import LineString, Point

# Define a function to extract the start and end points from the geometry
def extract_start_end_points(geometry):
    if isinstance(geometry, LineString):
        start_point = Point(geometry.coords[0])
        end_point = Point(geometry.coords[-1])
        return start_point, end_point
    else:
        return None, None

# Define a function to link "from" and "to" nodes to other rows with a tolerance of 5 meters
def link_nodes(row, df):
    tolerance = 5  # Tolerance in meters
    for index, other_row in df.iterrows():
        if index == row.name:  # Skip the current row being passed as parameter
            continue
        if row['from'].distance(other_row['to']) <= tolerance:
            return index
        elif row['to'].distance(other_row['from']) <= tolerance:
            return index
    return None

shapefile_path = 'FSJ-Export/Distribution_Pipe_FSJ.shp'
df = gpd.read_file(shapefile_path)

# Apply the function to each row in the dataframe to extract start and end points
df['from'], df['to'] = zip(*df['geometry'].apply(extract_start_end_points))

# Create a new column "from_node" to store the linked row number for "from" nodes
df['from_node'] = df.apply(lambda row: link_nodes(row, df), axis=1)

# Create a new column "to_node" to store the linked row number for "to" nodes
df['to_node'] = df.apply(lambda row: link_nodes(row, df), axis=1)

# Display the dataframe to verify the new columns
print(df[['geometry', 'from', 'to', 'from_node', 'to_node']])
