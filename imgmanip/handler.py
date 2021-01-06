""" handler.py

This module processes objects created by argparse and calls appropriate
image manipulation functions defined in a ImageManipulator class
instance.
"""

from manipulator import ImageManipulator


def _is_valid_filter(filter_string):
    """Validates a passed filter string."""
    if filter_string in [
            'BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE',
            'EMBOSS', 'FIND_EDGES', 'SHARPEN', 'SMOOTH', 'SMOOTH_MORE']:
        return True
    return False


def _is_valid_enhancer(enhancer_string):
    """Validates a passed enhancer string."""
    if enhancer_string in [
            'BRIGHTNESS', 'COLOR', 'COLOUR', 'CONTRAST', 'SHARPNESS',
            'GREYSCALE', 'GAUSSIANBLUR', 'BOXBLUR']:
        return True
    return False


def _handle_filters(namespace, manip):
    """Handles filter arguments."""

    # Handle the received filters strings
    for filter_string in namespace.filters:
        filter_string = filter_string.upper()

        # Handle invalid filter names
        if not _is_valid_filter(filter_string):
            print("'{0}' not a valid filter name. Skipping..."
                  .format(filter_string))
            continue

        # Apply filter
        manip.apply_filter_and_save(filter_string)


def _handle_enhancers(namespace, manip):
    """Handles enhancement arguments"""

    # Handle the received enhancer strings
    for enhancer_string in namespace.enhancers:
        enhancer_string = enhancer_string.upper()

        # Handle invalid enhancer names
        if not _is_valid_enhancer(enhancer_string):
            print("'{0}' not a valid enhancer name. Skipping..."
                  .format(enhancer_string))
            continue

        # Apply enhancer
        manip.apply_enhancer_and_save(enhancer_string, namespace.factor)


def _handle_resizing(namespace, manip):
    """Handle any resizing arguments."""

    if namespace.resize:
        manip.resize_image(namespace.resize)

    elif namespace.resize_width:
        manip.resize_image((namespace.resize_width, manip.image.size[1]))

    elif namespace.resize_height:
        manip.resize_image((manip.image.size[0], namespace.resize_height))

    elif namespace.resize_width_proportional:
        width = namespace.resize_width_proportional
        manip.resize_image((
            width,
            int((width / manip.image.size[0]) * manip.image.size[1])))

    elif namespace.resize_height_proportional:
        height = namespace.resize_height_proportional
        manip.resize_image((
            int((height / manip.image.size[1]) * manip.image.size[0]),
            height))


def handle_arguments(namespace, image, index):
    """Function to handle command line arguments."""

    # Cache image in ImageManipulator object
    manip = ImageManipulator(image, index)

    # Output image information
    if namespace.info:
        manip.output_information()

    # Handle thumbnail generation
    if namespace.thumbnail:
        manip.generate_thumbnail(namespace.thumbnail_width)

    # Handle filters
    if namespace.filters is not None:
        _handle_filters(namespace, manip)

    # Handler enhancers
    if namespace.enhancers is not None:
        _handle_enhancers(namespace, manip)

    # Handle flipping
    if namespace.flip:
        manip.apply_flips(namespace.flip)

    # Handle resizing
    _handle_resizing(namespace, manip)

    # Handle rotation
    if namespace.rotate:
        manip.rotate_image(namespace.rotate)

    # Save the new file if necessary
    manip.save_image()
