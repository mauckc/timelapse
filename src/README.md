# python source files

```
tuned_resized_timelapse.py
```

Jetson tx2 nvcamerasrc command to pass cv2 VideoCapture object
```
'nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)2592, height=(int)1944, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! appsink'
```

How to drop frames and speed up a video to match 20 fps and be 4 times faster
```bash
ffmpeg -i sample.mp4 -r 20 -filter:v "setpts=0.25*PTS" output_fast.mp4
```

How to interpolate a higher fps
```bash
ffmpeg -i sample.mp4 -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120'" output.mp4
```
