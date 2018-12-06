import numpy as np
import cv2
import time

# time delay between frames
delay = 1.0

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)2592, height=(int)1944, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! appsink")
# Create background subtractor class with specified history
#bgsb = cv2.createBackgroundSubtractorMOG2(history = 5)

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
resize_factor = 1.0
frame_width = int(cap.get(3)*resize_factor)
frame_height = int(cap.get(4)*resize_factor)

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

# For Erosion usage with cv2.exMorphology all the pixels near boundary will be discarded depending upon the size of kernel. So the thickness or size of the foreground object decreases or simply white region decreases in the image. It is useful for removing small white noises
#kernel = np.ones((9,9),np.uint8)


# Iterating count
i=0
# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, image = cap.read()
    if ret == True:
        # Convert image to grayscale
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Process The Image
        # Small blur to reduce noise
        #blur = cv2.GaussianBlur(gray,(11,11),0)
        # Morpholgy Erosion using pre-defined kernel
        #erosion = cv2.erode(blur,kernel,iterations = 1)
        #opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
        # Apply the background subtractor
        #fgmask = bgsb.apply(opening)
        # Get image dimensions
        height, width = image.shape[:2]
        # Resize image before output
        res = cv2.resize(image,(int(0.5*width),int(0.5*height)), interpolation = cv2.INTER_LINEAR)
        #RGB = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB)
        # Display image to screen
        cv2.imshow('Thresholded Image',res)
        # Write the frame into the file 'output.avi'

        cv2.waitKey(1)
        out.write(image)
        cv2.waitKey(1)
        i+=1
        time.sleep(delay)

        # Press Q on keyboard to  exit
        # If live camera replace waitKey(25) to waitKey(1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

# Remove all windows when finished
cv2.destroyAllWindows()
out.release()
