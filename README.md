# timelapse
timelapse with python


## Sample
![sample gif](./img/output_sample_fast.gif)
![sample gif](./img/evergreen_yosemite.gif)


## FFmpeg

An alternative way to convert video to timelapse

```Shell
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -an output.mp4
```
