#!/usr/local/bin/python3
from pathlib import Path
import argparse
import logging
import json


logger = logging.getLogger(__name__)


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="wheel inputfile")
    parser.add_argument("--version", required=True, help="wheel output file")
    parser.add_argument("--filename", required=True, help="version of the language file")
    args = parser.parse_args()
    return args


def main(*argv):

    from wowool.build.git import download_raw

    args = parse_arguments(*argv)
    filename = Path(args.filename)
    download_raw(repo=args.repo, version=args.version, file_name=filename.name, output_path=filename)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
