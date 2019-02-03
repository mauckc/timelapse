from PIL import Image
import time

numChannels = 3

x = eval(raw_input('X-Value:'))
y = eval(raw_input('X-Value:'))

im = Image.open('cat_1.jpg') # Can be many different formats.
pix = im.load()
print im.size  # Get the width and hight of the image for iterating over
# print pix[x,y]  # Get the RGBA Value of the a pixel of an image
#
# print type(pix[x,y])
# print pix[x,y][2]
# print pix[x,y][0]
# im.show()

time.sleep(0.2)

# # Greyscale the image
# for xval in range(im.size[0]):
#     for yval in range(im.size[1]):
#         Rval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
#         Gval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
#         Bval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
#         im.putpixel((xval,yval), (Rval, Gval, Bval))

# Greyscale the image
for xval in range(im.size[0]):
    for yval in range(im.size[1]):
        Rval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
        Gval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
        Bval = int(( pix[xval,yval][0] + pix[xval,yval][1] + pix[xval,yval][2] ) / 3)
        pix[x,y] = (Rval, Gval, Bval)

im.show()
# pix[x,y] = value
