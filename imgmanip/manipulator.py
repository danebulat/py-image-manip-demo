""" manipulator.py

Implements the ImageManipulator class which caches a loaded image in
memory. The class operations process this image, and the image can be
saved to a new file by called ImageManipulator.save_image().
"""

import os
import copy
from PIL import Image, ImageEnhance, ImageFilter


# -------------------------------------------------------------------------
# MODULE: ImageManipulator Class
# -------------------------------------------------------------------------

class ImageManipulator:
    """A class that caches an input image and performs a number of operations
    on it using PIL (Python Imaging Library).
    """

    def __init__(self, image, index):
        self.image = image
        self.original_filename = image.filename
        self.save_flag = False
        self.index = index

    def output_information(self):
        """Sends image properties to standard output."""
        print("{0:<9}: {1}".format("Filename", self.image.filename))
        print("{0:<9}: {1}".format("Size", self.image.size))
        print("{0:<9}: {1}".format("Format", self.image.format))
        print("{0:<9}: {1}\n".format("Bands", self.image.getbands()))

    def _apply_filter(self, filter_string):
        """Apply a PIL filter to an image and return it."""

        return {
            'BLUR':              self.image.filter(ImageFilter.BLUR),
            'CONTOUR':           self.image.filter(ImageFilter.CONTOUR),
            'DETAIL':            self.image.filter(ImageFilter.DETAIL),
            'EDGE_ENHANCE':      self.image.filter(ImageFilter.EDGE_ENHANCE),
            'EMBOSS':            self.image.filter(ImageFilter.EMBOSS),
            'FIND_EDGES':        self.image.filter(ImageFilter.FIND_EDGES),
            'SHARPEN':           self.image.filter(ImageFilter.SHARPEN),
            'SMOOTH':            self.image.filter(ImageFilter.SMOOTH),
            'SMOOTH_MORE':       self.image.filter(ImageFilter.SMOOTH_MORE),
            'EDGE_ENHANCE_MORE':
                self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        }[filter_string]

    def apply_filter_and_save(self, filter_string):
        """Apply a filter to a loaded image and save the new version."""

        self.save_flag = True
        self.image = self._apply_filter(filter_string)
        print(f"{filter_string} filter applied to {self.original_filename}")

    def _apply_enhancer(self, enhancer, enhancer_string, factor):
        """Enhances an image and saves a new file."""

        self.image = enhancer.enhance(factor)
        print("{0} enhancer applied to {1} [factor = {2}]"
              .format(enhancer_string, self.original_filename, factor))

    def apply_enhancer_and_save(self, enhancer_string, factor):
        """Enhances an image and calls apply_enhancer() to save a new file."""

        # Set save flag
        self.save_flag = True

        if enhancer_string == 'BRIGHTNESS':
            enh = ImageEnhance.Brightness(self.image)
            self._apply_enhancer(enh, enhancer_string, factor)

        elif enhancer_string in ['COLOR', 'COLOUR']:
            enh = ImageEnhance.Color(self.image)
            self._apply_enhancer(enh, enhancer_string, factor)

        elif enhancer_string == 'CONTRAST':
            enh = ImageEnhance.Contrast(self.image)
            self._apply_enhancer(enh, enhancer_string, factor)

        elif enhancer_string == 'SHARPNESS':
            enh = ImageEnhance.Sharpness(self.image)
            self._apply_enhancer(enh, enhancer_string, factor)

        elif enhancer_string == 'GREYSCALE':
            self.image = self.image.convert('L')
            print("{0} enhancer applied to {1}".format(
                enhancer_string, self.original_filename))

        elif enhancer_string in ['GAUSSIANBLUR', 'BOXBLUR']:
            if enhancer_string == 'GAUSSIANBLUR':
                self.image = self.image.filter(
                    ImageFilter.GaussianBlur(factor))
            else:
                self.image = self.image.filter(
                    ImageFilter.BoxBlur(factor))

            print("{0} filter applied to {1} [radius = {2}]".format(
                enhancer_string, self.original_filename, factor))

    def generate_thumbnail(self, width):
        """Saves a thumbnail version of the cached image."""

        # Make a deep copy of the image before generating thumbnial
        thumb_image = copy.deepcopy(self.image)

        # Calculate heigt dynamically based on the received width
        size = (width,
                int(((width / self.image.size[0]) * self.image.size[1])))

        # Calculate the output name - name-widthxheight.thumb
        name = os.path.splitext(self.image.filename)[0]
        out_filename = name + '-' +  \
            str(size[0]) + 'x' + str(size[1]) + '-' + str(self.index) \
                         + '.thumb'

        # Generate thumbnail and save
        thumb_image.thumbnail(size)
        thumb_image.save(out_filename, thumb_image.format)

        print("Thumbnail of {0} generated: {1}".format(
            self.original_filename, out_filename))

    def apply_flips(self, flips):
        """Flips the image horizontally or vertically."""

        # Flip internal image
        for flip in flips:
            if flip.upper() == 'HORZ':
                self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                print(f"{self.original_filename} flipped horizontally.")
            elif flip.upper() == 'VERT':
                self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
                print(f"{self.original_filename} flipped vertically.")

        # Save file
        self.save_flag = True

    def resize_image(self, size):
        """Resizes cached image to the X and Y values in the passed tuple.
        """
        self.image = self.image.resize(size)
        print(f"{self.original_filename} resized to: {size}")

        # Save file
        self.save_flag = True

    def rotate_image(self, increment):
        """Rotates the cached image counter-clockwise in a 90 degree
        increment.
        """

        if increment == 90:
            self.image = self.image.transpose(Image.ROTATE_90)
        elif increment == 180:
            self.image = self.image.transpose(Image.ROTATE_180)
        else:
            self.image = self.image.transpose(Image.ROTATE_270)
        print(f"{self.original_filename} rotated {increment} degrees CCW.")

        # Save file
        self.save_flag = True

    def save_image(self):
        """Saves the image to a new file if save flag is set."""

        if self.save_flag is True:
            name, ext = os.path.splitext(self.original_filename)
            out_filename = name + '-manip-' + str(self.index) + ext
            self.image.save(out_filename)
            print(f"New file saved as: {out_filename}")
