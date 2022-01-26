"""
Tool to resolve a wheel file from an index given a package name
"""

import logging
import urllib.request
import os
import sys
import tools.wheel_resolver.src.wheel_tags.tags as tg
import argparse as argparse


def download(url):
    output = os.environ.get("OUTS")
    if output is None:
        logging.critical("No output directory found")

    urllib.request.urlretrieve(url, output)


def main():
    """
    Parse command line arguments
    Get all download urls for a given package/version combo
    Figure out which ones are compatible with our system (whether
    that's our actual system or a system we've specified that we
    are maybe cross-compiling for.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--package',
            type=str,
            help='the package to resolve')
    parser.add_argument(
            '--version',
            type=str,
            help='the version of the package to be resolved')
    parser.add_argument(
            '--arch',
            nargs="*",
            type=str,
            default=[],
            help='specify architecture')

    args = parser.parse_args()

    # Require a package to be specified
    if args.package is None:
        sys.exit("Wheel resolver tool requires a package to be passed")

    # Fetch all available wheel urls from index
    urls = tg.get_download_urls(args.package, args.version)

    result = tg.get_url(urls, args.arch)

    if result is None:
        logging.critical("Found", len(urls), "urls but none are "
                         "compatible with the specified architecture")

    download(result)


main()
