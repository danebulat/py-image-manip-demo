#!/path/to/python

"""Module for performing a range of image manipulations.

Uses Pillow and the standard argparse library.
"""

import parser
from PIL import Image
from handler import handle_arguments

# -------------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------------

if __name__ == '__main__':

    # Load objects from command-line input
    namespace = parser.parse_arguments()

    # Iterate received filenames
    for index, filename in enumerate(namespace.inputs):
        try:
            # Load image into memory and handle arguments
            with Image.open(filename) as opened_image:
                handle_arguments(namespace, opened_image, index)

        except FileNotFoundError as err:
            print(f"WARNING: {err.filename} not found. Skipping...")
