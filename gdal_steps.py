from osgeo import gdal
import rasterio

pop_fo = 'bgd_ppp_2020.tif'

pop_ds = gdal.Open(pop_fo)

pop_gt = pop_ds.GetGeoTransform()

pcr_fo = 'PCR_clipped_reprojected_boolean.tiff'

pcr_ds = rasterio.open(pcr_fo)

xmin, ymin, xmax, ymax = pcr_ds.bounds

warp_options = gdal.WarpOptions(outputBounds=(xmin, ymin, xmax, ymax))

pop_ds_warped = gdal.Warp('test.tiff', pop_ds, options=warp_options)

print(pop_ds_warped.GetGeoTransform())

print(pcr_ds.transform)

xRes_dest = pcr_ds.transform[0]
yRes_dest = pcr_ds.transform[4]

print(xRes_dest, yRes_dest)

warp_options = gdal.WarpOptions(xRes=xRes_dest, yRes=yRes_dest, outputBounds=(xmin, ymin, xmax, ymax))

ds_warped = gdal.Warp('test2.tiff', pop_ds, options=warp_options)

print(ds_warped.GetGeoTransform())

print(pcr_ds.transform)