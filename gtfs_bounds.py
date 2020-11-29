#!/usr/bin/env python3
#
#    Copyright (C) 2020 Trillium Solutions <ed@trilliumtransit.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this program except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import zipfile
import csv
import argparse
import subprocess

from sys import argv, stderr, stdout
from io import TextIOWrapper
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description="""
            Find the lat/lon bounds of a GTFS file.

            If an OSM input file is provided, create an output file which is a
            trimmed version of the input file.

            Alternatively, OSM may be downloaded from the Overpass API
            (https://wiki.openstreetmap.org/wiki/Overpass_API) and written to
            an output file in OSM XML format.
        """)

    input_group = parser.add_mutually_exclusive_group()

    input_group.add_argument('-i', '--osm-input',
            type=argparse.FileType(),
            help="Input OSM file, used by osmconvert.")

    input_group.add_argument('-d', '--download-from-overpass',
            action='store_true', 
            help="Download OSM from Overpass API, and save to the OSM_OUTPUT file. Uses the wget program.")

    parser.add_argument('-o',
            '--osm-output', 
            help="Output OSM file, will be overwritten.")

    parser.add_argument('--force',
            action='store_true', 
            help="Force overwrite of the OSM_OUTPUT file.")

    parser.add_argument('--buffer-degrees',
            type=float,
            help="Increase the bounds by a Buffer of this many degrees.")

    parser.add_argument('gtfs_file', nargs='*', help="Input GTFS file. Multiple files may be provided.")

    args = parser.parse_args()
    
    for g in args.gtfs_file:
        if not zipfile.is_zipfile(g):
            parser.print_help()
            print ("\nERROR, the GTFS file '%s' doesn't appear to be a zip archive." % g, file=stderr)
            exit(1)

    if args.osm_output:
        o = Path(args.osm_output)
        if o.exists() and not args.force:
            parser.print_help()
            print ("\nERROR, output osm file '%s' exists and --force was not used." % args.osm_output)
            exit(1)

    return args

def main():
    min_lat = 1000
    max_lat = -1000
    min_lon = 1000
    max_lon = -1000
    args = parse_args()

    for g in args.gtfs_file:
        with zipfile.ZipFile(g) as z:
            #print ('z is: %s' % z, file=stderr)
            stopsfile = TextIOWrapper(z.open('stops.txt'))
            #print ('stops is: %s' % stopsfile, file=stderr)
            stops = csv.DictReader(stopsfile)

            for stop in stops:
                try:
                    min_lat = min(min_lat, float(stop['stop_lat']))
                    max_lat = max(max_lat, float(stop['stop_lat']))
                    min_lon = min(min_lon, float(stop['stop_lon']))
                    max_lon = max(max_lon, float(stop['stop_lon']))
                except e:
                    pass

    if 1000 in (min_lat, min_lon) or -1000 in (max_lat, max_lon):
        print('Sorry, bounds not found.')
        exit(1)
    
    print('Note: please use caution when intepreting these results near longitude +180/-180!', file=stderr)
    print('Bounds are lat: [%s, %s] lon: [%s, %s]' %(min_lat, max_lat, min_lon, max_lon))
    if args.buffer_degrees:
        min_lat -= args.buffer_degrees
        min_lon -= args.buffer_degrees
        max_lat += args.buffer_degrees
        max_lon += args.buffer_degrees
        print('Buffered Bounds are lat: [%s, %s] lon: [%s, %s]' %(min_lat, max_lat, min_lon, max_lon))

    # print ('osmconvert -b=%s,%s,%s,%s --complete-ways ' % (min_lon,min_lat,max_lon,max_lat))
    if args.osm_input and args.osm_output:
        run_arguments = [ 
            'osmconvert', 
            args.osm_input.name,  
            '-b=%s,%s,%s,%s' % (min_lon, min_lat, max_lon, max_lat),
            '--complete-ways',
            '-o=%s' % args.osm_output,
            ]
        # print('Running:', ' '.join(run_arguments), file=stderr)
        subprocess.run(run_arguments)

    if args.osm_output and args.download_from_overpass:
        url = 'https://overpass-api.de/api/map?bbox=%s,%s,%s,%s' % (min_lon,min_lat,max_lon,max_lat)
        print('Downloading from the Overpass URL: %s' % url)
        run_arguments = [ 'wget', url, '--compression=gzip', '-O', args.osm_output ]
        subprocess.run(run_arguments)
 
if __name__ == '__main__':
    main()


