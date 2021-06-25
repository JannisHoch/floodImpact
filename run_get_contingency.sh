output_dir=./data/contingency
obs=./data/MODIS_clipped_boolean.tiff
sim=./data/PCR_clipped_reprojected_boolean.tiff

floodimpact --debug --version get-contingency --plot -out $output_dir $obs $sim