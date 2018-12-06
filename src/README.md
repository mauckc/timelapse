# python source files

```
tuned_resized_timelapse.py
```

Jetson tx2 nvcamerasrc command to pass cv2 VideoCapture object
```shell
'nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)2592, height=(int)1944, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! appsink'
```
