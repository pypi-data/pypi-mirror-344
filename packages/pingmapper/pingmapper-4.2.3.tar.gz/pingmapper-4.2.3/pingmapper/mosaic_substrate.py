


from osgeo import gdal



resampleAlg = 'nearest'
overview = False
inVrt = r'D:\redbo_science\projects\GulfSturgeonProject_2025\ProcessedData\Raw\PRL_438_395_20210304_FWSB1_Rec00008_2025\substrate\map_substrate_mosaic\PRL_438_395_20210304_FWSB1_Rec00008_2025_map_substrate_raster_mosaic_0_copy.vrt'
outRast = r'D:\redbo_science\projects\GulfSturgeonProject_2025\ProcessedData\Raw\PRL_438_395_20210304_FWSB1_Rec00008_2025\substrate\map_substrate_mosaic\PRL_438_395_20210304_FWSB1_Rec00008_2025_map_substrate.tif'

 # Create GeoTiff from vrt
ds = gdal.Open(inVrt)

kwargs = {'format': 'GTiff',
            'creationOptions': ['NUM_THREADS=ALL_CPUS', 'COMPRESS=LZW', 'TILED=YES']
            }

# Create geotiff
gdal.Translate(outRast, ds, **kwargs)

# Generate overviews
if overview:
    dest = gdal.Open(outRast, 1)
    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    dest.BuildOverviews('nearest', [2 ** j for j in range(1,10)])