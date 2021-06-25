from osgeo import gdal
import click
import rasterio
from rasterio.plot import show
import os

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context

def cli(ctx, debug):

    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    if debug: click.echo("Debug mode is on")

@cli.command()
@click.argument('dr', type=str)
@click.argument('sr', type=str)
@click.option('-out', '--output-name', type=str, help='output name, can include relative path', default='./resample_tiff_out.tiff')
@click.option('--plot/--no-plot', default=False, help='show plot of source and warped file')
@click.pass_context

def resample_tiff(ctx, dr, sr, output_name, plot):  
    """Command line script resampling a tiff-file (DR) to the spatial extent and spatial resolution of another tiff-file (SR).
    
    DR: file that will be resampled.

    SR: file whose spatial properties will be used for resampling.

    """ 

    click.echo('reading source raster {}'.format(sr))
    source_ds = rasterio.open(sr)
    
    xmin, ymin, xmax, ymax = source_ds.bounds
    if ctx.obj['DEBUG']: click.echo('getting source bounds xmin={}, ymin={}, xmax={}, ymax{}'.format(xmin, ymin, xmax, ymax))
    xRes_dest = source_ds.transform[0]
    yRes_dest = source_ds.transform[4]
    if ctx.obj['DEBUG']: click.echo('getting source resolutions x={}, y={}'.format(xRes_dest, yRes_dest))
    
    click.echo('reading destination raster {}'.format(dr))
    dr_ds = gdal.Open(dr)
    dr_gt = dr_ds.GetGeoTransform()

    click.echo('defining GDAL WarpOptions')
    warp_options = gdal.WarpOptions(xRes=xRes_dest, yRes=yRes_dest, outputBounds=(xmin, ymin, xmax, ymax))

    output_name = os.path.abspath(output_name)
    click.echo('saving warped file to {}'.format(output_name))
    warped_ds = gdal.Warp(output_name, dr_ds, options=warp_options)

    if ctx.obj['DEBUG']: click.echo('geo-transform of warped file {}'.format(warped_ds.GetGeoTransform()))

    if plot:
        show(source_ds.read(), transform=source_ds.transform)
        out = rasterio.open(output_name)
        show(out.read(), transform=out.transform)