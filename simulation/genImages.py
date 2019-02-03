from PIL import Image
import time
import os

datetimestr = time.strftime("%Y-%m-%d")
datehourtimestr = time.strftime("%Y-%m-%d_%H")
filetimestr = time.strftime("%Y-%m-%d_%H%M%S")

image_path = 'R03'

if not os.path.exists("./"+ image_path):
    # Create path to store images
    os.mkdir(image_path)
    print("created directory: "+ image_path)

if not os.path.exists("./"+ image_path +"/"+ datetimestr +"/"+ datehourtimestr):
    # Create path to store images
    os.mkdir("./"+ image_path +"/"+ datetimestr)
    os.mkdir("./"+ image_path +"/"+ datetimestr +"/"+ datehourtimestr)

    print("created directory: "+ image_path +"/"+ datetimestr +"/"+ datehourtimestr)

print filetimestr

def getTimeStr():
    datetimestr = time.strftime("%Y-%m-%d")
    datehourtimestr = time.strftime("%Y-%m-%d_%H")
    filetimestr = time.strftime("%Y-%m-%d_%H%M%S")

    if not os.path.exists(image_path):
        # Create path to store images
        os.mkdir(image_path)
        print("created directory: "+ image_path)

    if not os.path.exists(image_path +"/"+ datetimestr +"/"+ datehourtimestr):
        # Create path to store images
        os.mkdir(image_path +"/"+ datetimestr)
        os.mkdir(image_path +"/"+ datetimestr +"/"+ datehourtimestr)

        print("created directory: "+ image_path +"/"+ datetimestr +"/"+ datehourtimestr)

    timestr = image_path +"/"+ datetimestr +"/"+ datehourtimestr + "/"+ filetimestr +".jpg"

    return timestr

def loadImage(input_image_filename):
    im = Image.open(input_image_filename)
    return im

def main():
    input_image_filename = "cat_1.jpg"
    im = loadImage(input_image_filename)
    pix = im.load()
    print("[SETUP]: loaded "+ input_image_filename)

    im.save(getTimeStr())

    return


def blur(im):
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
    

for i in range(60):
    timestr = getTimeStr()

    print("[INFO]: Saving fileName: "+timestr+".jpg")

    main()

    time.sleep(3.334)

# im = Image.open('cat_1.jpg') # Can be many different formats.
# pix = im.load()
# print im.size  # Get the width and hight of the image for iterating over
#
# # Blur the image
# for xval in range(1,im.size[0]-1):
#     for yval in range(1,im.size[1]-1):
#         Rval = int((( pix[xval-1,yval][0] + pix[xval,yval][0] + pix[xval+1,yval][0] ) / 3) + (( pix[xval,yval-1][0] + pix[xval,yval][0] + pix[xval,yval+1][0] )/3)/2 )
#         Gval = int((( pix[xval-1,yval][1] + pix[xval,yval][1] + pix[xval+1,yval][1] ) / 3) + (( pix[xval,yval-1][1] + pix[xval,yval][1] + pix[xval,yval+1][1] )/3) /2 )
#         Bval = int((( pix[xval-1,yval][2] + pix[xval,yval][2] + pix[xval+1,yval][2] )/3) + (( pix[xval,yval-1][2] + pix[xval,yval][2] + pix[xval,yval+1][2] )/3) /2 )
#         pix[xval,yval] = (Rval, Gval, Bval)
#         # Slower version pre v1.1.6 -> im.putpixel((xval,yval), (Rval, Gval, Bval))
#
# # Show processed image
# im.show()
