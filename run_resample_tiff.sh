source_raster=./data/PCR_clipped_reprojected_boolean.tiff

destination_raster=./data/original/population_SSP2_5min_bc_2018.tiff
output_file=./data/population_SSP2_5min_bc_2018_resampled.tiff

floodimpact --debug --version resample-tiff -out $output_file $destination_raster $source_raster

destination_raster=./data/original/population_SSP2_5min_bc_2030.tiff
output_file=./data/population_SSP2_5min_bc_2030_resampled.tiff

floodimpact --debug --version resample-tiff -out $output_file $destination_raster $source_raster

destination_raster=./data/original/population_SSP2_5min_bc_2040.tiff
output_file=./data/population_SSP2_5min_bc_2040_resampled.tiff

floodimpact --debug --version resample-tiff -out $output_file $destination_raster $source_raster

destination_raster=./data/original/population_SSP2_5min_bc_2050.tiff
output_file=./data/population_SSP2_5min_bc_2050_resampled.tiff

floodimpact --debug --version resample-tiff -out $output_file $destination_raster $source_raster