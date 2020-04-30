In [1]: from osgeo import gdal

In [2]: pop_fo = 'bgd_ppp_2020.tif'

In [3]: pop_ds = gdal.Open(pop_fo)

In [4]: pop_gt = pop_ds.GetGeoTransform()

In [5]: pop_gt
Out[5]:
(88.01041633,
 0.0008333333300571842,
 0.0,
 26.634583428,
 0.0,
 -0.0008333333300330033)

In [6]: import rasterio

In [7]: pcr_fo = 'PCR_clipped_reprojected_boolean.tiff'

In [8]: pcr_ds = rasterio.open(pcr_fo)

In [11]: xmin, ymin, xmax, ymax = pcr_ds.bounds

In [13]: gdal.Warp?
Signature: gdal.Warp(destNameOrDestDS, srcDSOrSrcDSTab, **kwargs)
Docstring:
Warp one or several datasets.
Arguments are :
  destNameOrDestDS --- Output dataset name or object
  srcDSOrSrcDSTab --- an array of Dataset objects or filenames, or a Dataset object or a filename
Keyword arguments are :
  options --- return of gdal.WarpOptions(), string or array of strings
  other keywords arguments of gdal.WarpOptions()
If options is provided as a gdal.WarpOptions() object, other keywords are ignored.
File:      c:\users\hoch0001\appdata\local\continuum\anaconda3\lib\site-packages\osgeo\gdal.py
Type:      function

In [14]: test = gdal.WarpOptions?
Signature:
gdal.WarpOptions(
    options=[],
    format=None,
    outputBounds=None,
    outputBoundsSRS=None,
    xRes=None,
    yRes=None,
    targetAlignedPixels=False,
    width=0,
    height=0,
    srcSRS=None,
    dstSRS=None,
    srcAlpha=False,
    dstAlpha=False,
    warpOptions=None,
    errorThreshold=None,
    warpMemoryLimit=None,
    creationOptions=None,
    outputType=0,
    workingType=0,
    resampleAlg=None,
    srcNodata=None,
    dstNodata=None,
    multithread=False,
    tps=False,
    rpc=False,
    geoloc=False,
    polynomialOrder=None,
    transformerOptions=None,
    cutlineDSName=None,
    cutlineLayer=None,
    cutlineWhere=None,
    cutlineSQL=None,
    cutlineBlend=None,
    cropToCutline=False,
    copyMetadata=True,
    metadataConflictValue=None,
    setColorInterpretation=False,
    callback=None,
    callback_data=None,
)
Docstring:
Create a WarpOptions() object that can be passed to gdal.Warp()
Keyword arguments are :
  options --- can be be an array of strings, a string or let empty and filled from other keywords.
  format --- output format ("GTiff", etc...)
  outputBounds --- output bounds as (minX, minY, maxX, maxY) in target SRS
  outputBoundsSRS --- SRS in which output bounds are expressed, in the case they are not expressed in dstSRS
  xRes, yRes --- output resolution in target SRS
  targetAlignedPixels --- whether to force output bounds to be multiple of output resolution
  width --- width of the output raster in pixel
  height --- height of the output raster in pixel
  srcSRS --- source SRS
  dstSRS --- output SRS
  srcAlpha --- whether to force the last band of the input dataset to be considered as an alpha band
  dstAlpha --- whether to force the creation of an output alpha band
  outputType --- output type (gdal.GDT_Byte, etc...)
  workingType --- working type (gdal.GDT_Byte, etc...)
  warpOptions --- list of warping options
  errorThreshold --- error threshold for approximation transformer (in pixels)
  warpMemoryLimit --- size of working buffer in bytes
  resampleAlg --- resampling mode
  creationOptions --- list of creation options
  srcNodata --- source nodata value(s)
  dstNodata --- output nodata value(s)
  multithread --- whether to multithread computation and I/O operations
  tps --- whether to use Thin Plate Spline GCP transformer
  rpc --- whether to use RPC transformer
  geoloc --- whether to use GeoLocation array transformer
  polynomialOrder --- order of polynomial GCP interpolation
  transformerOptions --- list of transformer options
  cutlineDSName --- cutline dataset name
  cutlineLayer --- cutline layer name
  cutlineWhere --- cutline WHERE clause
  cutlineSQL --- cutline SQL statement
  cutlineBlend --- cutline blend distance in pixels
  cropToCutline --- whether to use cutline extent for output bounds
  copyMetadata --- whether to copy source metadata
  metadataConflictValue --- metadata data conflict value
  setColorInterpretation --- whether to force color interpretation of input bands to output bands
  callback --- callback method
  callback_data --- user data for callback
File:      c:\users\hoch0001\appdata\local\continuum\anaconda3\lib\site-packages\osgeo\gdal.py
Type:      function

In [15]: warp_options = gdal.WarpOptions(outputBounds=(xmin, ymin, xmax, ymax))

In [23]: pop_ds_warped = gdal.Warp('test.tiff', ds, options=warp_options)

In [26]: pop_ds_warped.GetGeoTransform()
Out[26]: (89.435, 0.0008333333333333286, 0.0, 24.0, 0.0, -0.0008333333333333328)

In [28]: pcr_ds.transform
Out[28]:
Affine(0.0049999999999999715, 0.0, 89.435,
       0.0, -0.0049999999999999975, 24.0)

In [29]: xRes_dest = pcr_ds.transform[0]

In [30]: xRes_dest
Out[30]: 0.0049999999999999715

In [35]: yRes_dest = pcr_ds.transform[4]

In [36]: yRes_dest
Out[36]: -0.0049999999999999975

In [37]: warp_options = gdal.WarpOptions(xRes=xRes_dest, yRes=yRes_dest, outputBounds=(xmin, ymin, xmax, ymax))

In [39]: ds_warped = gdal.Warp('test2.tiff', ds, options=warp_options)

In [40]: ds_warped.GetGeoTransform()
Out[40]: (89.435, 0.0049999999999999715, 0.0, 24.0, 0.0, -0.0049999999999999975)

In [43]: pcr_ds.transform
Out[43]:
Affine(0.0049999999999999715, 0.0, 89.435,
       0.0, -0.0049999999999999975, 24.0)