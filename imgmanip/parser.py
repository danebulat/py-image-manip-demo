""" parser.py

This module parses arguments received from the command line and attaches
attributes to a namespace object. This namespace object is returned to
the application for handling.

The application's version number is  also defined at the top of this module.
These constants are displayed when the --version option is parsed on the
command line.
"""

import argparse
import textwrap

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0


def get_version_string():
    """Returns the version number as a string."""
    version = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR)
    if VERSION_PATCH != 0:
        version += '.' + str(VERSION_PATCH)
    return version


def set_parser_titles(parser):
    """Sets custom titles for the parser options headers in help text."""
    parser._positionals.title = 'Positional arguments'
    parser._optionals.title = 'Optional arguments'


def parse_arguments():
    """Parses command line-arguments and creates objects handled by the
    application.
    """

    parser = argparse.ArgumentParser(
        prog='imgmanip',
        usage='%(prog)s FILES [-e ENHANCERS] [-f FILTERS] [--thumbnail] ...',
        description=textwrap.dedent("""\
        Perform a range of manipulations on images files.

            Available Enhancers (-e, --enhance):

                BRIGHTNESS    COLOR    CONTRAST    SHARPNESS    GREYSCALE
                GAUSSIANBLUR  BOXBLUR

            Control the strength of an enhancer with the --factor option:

                --factor 1.0    No change to the image.
                --factor 1.2    Subtle change, a good starting point.

            Available Filters (-f, --filter):

                BLUR    CONTOUR     DETAIL   EDGE_ENHANCE  EDGE_ENHANCE_MORE
                EMBOSS  FIND_EDGES  SHARPEN  SMOOTH        SMOOTH_MORE

            Example usages:
                $ ./imgmanip file.jpg -e greyscale brightness --factor 1.25
                $ ./imgmanip file.jpg -f contour detail smooth -e greyscale
                $ ./imgmanip file.jpg --resize-width-proportional 512
                $ ./imgmanip file.jpg --flip horz --rotate 180
                $ ./imgmanip file.jpg --thumbnail --thumbnail-width 256

                * All options can be combined in a single command to
                  customise final output.
        """),
        epilog='Part of the PIL tutorial at: https://dane-bulat.medium.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        allow_abbrev=False,
        exit_on_error=True)

    # Set help text options headers
    set_parser_titles(parser)

    # Manually add -h, --help option to format help message
    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help="Show this help message and exit.")

    parser.add_argument('inputs', action='store', nargs='+',
                        help='A list of image files to process.')

    parser.add_argument('-i', '--info', action='store_true',
                        help='Display image properties.')

    parser.add_argument('-f', '--filter', action='store', nargs='+',
                        help='Apply filters to an images.',
                        dest='filters')

    parser.add_argument('-e', '--enhance', action='store', nargs='+',
                        help='Apply enhancers to an images.',
                        dest='enhancers')

    parser.add_argument('--factor', action='store', default=1.2, type=float,
                        help='Float to specify the strength of enhancers.')

    # Thumbnail generation
    parser.add_argument('--thumbnail', action='store_true',
                        help='A thumbnail is generated.')

    parser.add_argument('--thumbnail-width', action='store', type=int,
                        default=128,
                        help='Specify a width for the generated thumbnail.')

    # Flipping arguments
    parser.add_argument('--flip', action='store', nargs='+',
                        choices=['horz', 'vert'],
                        help='Flip an image vertically or horizontally.')

    # Rotating arguments
    parser.add_argument('--rotate', action='store', choices=[90, 180, 270],
                        type=int,
                        help="Rotate an image in a 90 degree increment.")

    # Resizing options are mutually exclusive
    resize_group = parser.add_mutually_exclusive_group()

    resize_group.add_argument(
        '--resize', action='store', nargs=2, type=int,
        help='Pass a width and height value to resize image.')

    resize_group.add_argument(
        '--resize-width-proportional', action='store',
        type=int, help='Resize image proportionally based on passed width.')

    resize_group.add_argument(
        '--resize-height-proportional', action='store',
        type=int, help='Resize image proportionally based on passed height')

    resize_group.add_argument(
        '--resize-width', action='store', type=int,
        help='Resize width only.')

    resize_group.add_argument(
        '--resize-height', action='store', type=int,
        help='Resize height only.')

    # Version number
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + get_version_string(),
                        help="Show program's version number and exit.")

    args = parser.parse_args()
    return args
