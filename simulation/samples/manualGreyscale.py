from PIL import Image
import time

im = Image.open('cat_1.jpg') # Can be many different formats.
pix = im.load()
print im.size  # Get the width and hight of the image for iterating over

# Greyscale the image
for xval in range(im.size[0]):
    for yval in range(im.size[1]):
        Rval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
        Gval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
        Bval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
        pix[xval,yval] = (Rval, Gval, Bval)
        # Slower version pre v1.1.6 -> im.putpixel((xval,yval), (Rval, Gval, Bval))

im.show()
