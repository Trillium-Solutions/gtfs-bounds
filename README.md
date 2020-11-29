# gtfs-bounds

Find the geographic bounds of a GTFS (https://gtfs.org) file.

Optionally, run `osmconvert` (https://gitlab.com/osm-c-tools/osmctools) to
create a trimmed version of an Open Street Map (https://openstreetmap.org/)
file.

## Usage

```
./gtfs_bounds.py  --help
usage: gtfs_bounds.py [-h] [--buffer-degrees BUFFER_DEGREES] [-i OSM_INPUT] [-o OSM_OUTPUT] [--force] gtfs_file

Find the lat/lon bounds of a GTFS file. If OSM files are provided, create an output file which is a trimmed version of the input file.

positional arguments:
  gtfs_file             Input GTFS file.

optional arguments:
  -h, --help            show this help message and exit
  --buffer-degrees BUFFER_DEGREES
                        Increase the bounds by a Buffer of this many degrees.
  -i OSM_INPUT, --osm-input OSM_INPUT
                        Input OSM file, used by osmconvert.
  -o OSM_OUTPUT, --osm-output OSM_OUTPUT
                        Output OSM file, will be overwritten.
  --force               Force overwrite of output OSM file.
```
