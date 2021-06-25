floodimpact
============

Code to evaluate the impact of floods plus some useful utility scripts to work with spatial data.

installation
-------------

.. code-block:: console

    # clone from GitHub
    $ git clone https://github.com/JannisHoch/floodimpact.git

    # cd to folder with floodimpact code
    $ cd path/to/floodimpact

    # create and activate conda environment
    $ conda env create -f environment.yml
    $ conda activate flood_impact

    # install package
    $ pip install -e .

execution
-----------

Use command line script.

.. code-block:: console

    Usage: floodimpact [OPTIONS] COMMAND [ARGS]...

    Options:
        --debug / --no-debug
        --version / --no-version
        --help                    Show this message and exit.

    Commands:
        get-contingency  "Computes contingency data computed from observed and...
        resample-tiff    Command line script resampling a tiff-file (DR) to the...

The ``get-contingency`` script works as follows.

.. code-block:: console

    Usage: floodimpact get-contingency [OPTIONS] OBS SIM

    Computes contingency data computed from observed and simulated flood
    extent.

    Returns hit rate, false alarm ratio, and critical succes index. Also a
    tiff-file with contingency map.

    OBS: path to observed flood extent.

    SIM: path to simualted flood extent.

    Options:
        -ot, --observation-threshold FLOAT
        -st, --simulation-threshold INTEGER
        -out, --output-directory PATH   path to output directory
        --plot / --no-plot              show plot of source and warped file
        --help                          Show this message and exit.

The ``resample-tiff`` script works as follows.

.. code-block:: console

    Usage: floodimpact resample-tiff [OPTIONS] DR SR

    Command line script resampling a tiff-file (DR) to the spatial extent and
    spatial resolution of another tiff-file (SR).

    Returns a resampled tiff-file.

    DR: file that will be resampled.

    SR: file whose spatial properties will be used for resampling.

    Options:
        -out, --output-name TEXT  output name, can include relative path
        --plot / --no-plot        show plot of source and warped file
        --help                    Show this message and exit.

Examples can be run with:

.. code-block:: console

    $ sh run_get_contingency.sh
    $ sh run_resample_tiff.sh

contact
-------------

Jannis Hoch (j.m.hoch@uu.nl)
