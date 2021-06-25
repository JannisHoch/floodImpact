from osgeo import gdal
import flood_impact
import click
import rasterio
from rasterio.plot import show
import Image
import os

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--version/--no-version', default=False)
@click.pass_context

def cli(ctx, debug, version):

    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    if debug: click.echo("Debug mode is on")
    if version: click.echo("flood_impact version {} used".format(flood_impact.__version__))

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

@cli.command()
@click.argument('obs', type=str)
@click.argument('sim', type=str)
@click.option('-ot', '--observation-threshold', default=0.5)
@click.option('-st', '--simulation-threshold', default=0)
@click.option('-out', '--output-directory', type=click.Path(), help='path to output directory', default='./OUT')
@click.option('--plot/--no-plot', default=False, help='show plot of source and warped file')
@click.pass_context

def get_contingency(ctx, obs, sim, observation_threshold, simulation_threshold, output_directory):  

    click.echo('reading observed flood extent from {}'.format(obs))
    bench_d = rasterio.open(obs)
    click.echo('reading simualted flood extent from {}'.format(sim))
    model_d = rasterio.open(sim)
    
    click.echo('computing contingency data')
    hr, far, csi, cont_arr = flood_impact.contingency(bench_d, model_d, observation_threshold, simulation_threshold)

    if ctx.obj['DEBUG']:
        click.echo('hit rate is {}'.format(hr))
        click.echo('false alarm ratio is {}'.format(far))
        click.echo('critical succes index is {}'.format(csi))

    click.echo('saving contingeny map to {}'.format(os.path.join(output_directory, 'contingency_map.tif')))
    im = Image.fromarray(cont_arr)
    im.save(os.path.join(output_directory, 'contingency_map.tif'))