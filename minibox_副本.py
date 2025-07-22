import geopandas as gpd
import pandas as pd
import ee

# Finding the Minimum Bounding Boxes
# Load the GeoJSON file
#file_path = 'data/sample_geojson_file.geojson'
#gdf = gpd.read_file(file_path)

# Calculate the minimum bounding box (envelope) for each parcel
#gdf['bbox'] = gdf.geometry.envelope
#gdf['center'] = gdf.geometry.centroid


# Calculate the bounding box points and center points
#gdf['minx'] = gdf.geometry.bounds.minx
#gdf['maxx'] = gdf.geometry.bounds.maxx
#gdf['miny'] = gdf.geometry.bounds.miny
#gdf['maxy'] = gdf.geometry.bounds.maxy
#gdf['center_x'] = gdf.geometry.centroid.x
#gdf['center_y'] = gdf.geometry.centroid.y

# Define the output CSV file path
#output_csv_path = 'data/sample.csv'

# Save the GeoDataFrame as a CSV file, excluding the index
#gdf.to_csv(output_csv_path, index=False)

# Load the CSV file
csv_file_path = 'data/sample1.csv'
df = pd.read_csv(csv_file_path)
geometry_coordinates_list = df['geometry_coordinates'].tolist()
# Fetching the images from GEE
ee.Authenticate()
ee.Initialize(project='baxsxasd')

def get_image_download_url(polygon_coords, start_date, end_date, vis_params, scale=0.5):
    """
    Generate a direct download URL for an image with visualization parameters.
    
    :param polygon_coords: Coordinates for the polygon defining the area of interest.
    :param start_date: Start date for the image collection filter.
    :param end_date: End date for the image collection filter.
    :param vis_params: Visualization parameters including 'min', 'max', and bands 'palette' if needed.
    :param scale: Scale in meters; 1 meter is typical for NAIP imagery.
    :return: A URL from which the image can be directly downloaded.
    """
    roi = ee.Geometry.Polygon([polygon_coords])
    
    # Filter the NAIP ImageCollection
    naip_collection = ee.ImageCollection('USDA/NAIP/DOQQ') \
                        .filterBounds(roi) \
                        .filterDate(start_date, end_date)
    
    # Get the median image, clip to the ROI, and select RGB bands
    median_image = naip_collection.median().clip(roi).select(['R', 'G', 'B'])
    
    # Generate the download URL with visualization parameters
    url = median_image.getThumbURL({
        'region': roi.getInfo()['coordinates'],
        'scale': scale,
        **vis_params  # Unpack visualization parameters
    })
    
    return url

# Visualization parameters for floating-point data
vis_params = {
    'min': 0.0,
    'max': 255.0,
    'format': 'png'
}

for polygon_coords_str in geometry_coordinates_list:
    # Convert the string representation to a list (assuming it's safely formatted)
    polygon_coords = eval(polygon_coords_str)
    
    # Generate the download URL
    download_url = get_image_download_url(polygon_coords, '2022-01-01', '2022-02-15', vis_params, scale=0.5)
    print(download_url)