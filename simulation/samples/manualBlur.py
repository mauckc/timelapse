from PIL import Image
import time

im = Image.open('cat_1.jpg') # Can be many different formats.
pix = im.load()
print im.size  # Get the width and hight of the image for iterating over

# Blur the image
for xval in range(1,im.size[0]-1):
    for yval in range(1,im.size[1]-1):
        Rval = int((( pix[xval-1,yval][0] + pix[xval,yval][0] + pix[xval+1,yval][0] ) / 3) + (( pix[xval,yval-1][0] + pix[xval,yval][0] + pix[xval,yval+1][0] )/3)/2 )
        Gval = int((( pix[xval-1,yval][1] + pix[xval,yval][1] + pix[xval+1,yval][1] ) / 3) + (( pix[xval,yval-1][1] + pix[xval,yval][1] + pix[xval,yval+1][1] )/3) /2 )
        Bval = int((( pix[xval-1,yval][2] + pix[xval,yval][2] + pix[xval+1,yval][2] )/3) + (( pix[xval,yval-1][2] + pix[xval,yval][2] + pix[xval,yval+1][2] )/3) /2 )
        pix[xval,yval] = (Rval, Gval, Bval)
        # Slower version pre v1.1.6 -> im.putpixel((xval,yval), (Rval, Gval, Bval))

# Show processed image
im.show()
