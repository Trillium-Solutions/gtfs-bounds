# gtfs-bounds

Find the geographic bounds of a GTFS (https://gtfs.org) file.

Optionally, create an Open Street Map (https://openstreetmap.org/) file trimmed
to the size of your GTFS.  Either by downloading from the Overpass API, or
by running `osmconvert` (https://gitlab.com/osm-c-tools/osmctools) starting with a larger
input OSM file.

If multiple GTFS files are provided, find geographic bounds which would contain
all the GTFS files.

## Usage

```
usage: gtfs_bounds.py [-h] [-i OSM_INPUT | -d] [-o OSM_OUTPUT] [--force] [--buffer-degrees BUFFER_DEGREES] [gtfs_file [gtfs_file ...]]

Find the lat/lon bounds of a GTFS file. If an OSM input file is provided, create an output file which is a trimmed version of the input
file. Alternatively, OSM may be downloaded from the Overpass API (https://wiki.openstreetmap.org/wiki/Overpass_API) and written to an
output file in OSM XML format.

positional arguments:
  gtfs_file             Input GTFS file. Multiple files may be provided.

optional arguments:
  -h, --help            show this help message and exit
  -i OSM_INPUT, --osm-input OSM_INPUT
                        Input OSM file, used by osmconvert.
  -d, --download-from-overpass
                        Download OSM from Overpass API, and save to the OSM_OUTPUT file. Uses the wget program.
  -o OSM_OUTPUT, --osm-output OSM_OUTPUT
                        Output OSM file, will be overwritten.
  --force               Force overwrite of the OSM_OUTPUT file.
  --buffer-degrees BUFFER_DEGREES
                        Increase the bounds by a Buffer of this many degrees.
```
