#!/usr/bin/env python

from dspr.sites import * 


def main(json_file):
    res = read_jgoogle(json_file, verbose=True)


if __name__ == '__main__':
    import argparse

    # functions to read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', metavar='JSON_FILE', nargs=1, 
            help='Read a google json file and dump the spot_signature')
    args = parser.parse_args()
    json_file = args.json_file[0]
    #pickle_spot_signature()
    main(json_file)
