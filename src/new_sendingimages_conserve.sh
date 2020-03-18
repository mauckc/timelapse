#!/bin/sh
PIDFILE="/run/sendingimages.pid"
SENDINGIMAGES_CONF="/system/sdcard/config/sendingimages.conf"
BASE_SAVE_DIR="/system/sdcard/DCIM/local/precloud"
CLOUD_SAVE_DIR="/system/sdcard/DCIM/local/cloud"
COMMON_FUNCTIONS_PATH="/system/sdcard/scripts/common_functions.sh"

if [ -f "$SENDINGIMAGES_CONF" ]; then
    . "$SENDINGIMAGES_CONF" 2>/dev/null
fi

if [ -f "$COMMON_FUNCTIONS_PATH" ]; then
    . "$COMMON_FUNCTIONS_PATH" 2>/dev/null
fi

# CONFIGURATION IR turns on after day_end_time and before
# day_end_time=20
# day_start_time=5
# TO DO configure into a config file named
day_end_time=$IR_DAY_END_TIME
day_start_time=$IR_DAY_START_TIME

function capturePutS3IR
{
  # Choose fileName by date and time down to second and per second counter
  SAVE_DIR=$BASE_SAVE_DIR
  if [ $SAVE_DIR_PER_DAY -eq 1 ]; then
      SAVE_DIR="$BASE_SAVE_DIR/$(date +%Y-%m-%d)"
  fi

  CLOUD_DIR=$CLOUD_SAVE_DIR
  if [ $SAVE_DIR_PER_DAY -eq 1 ]; then
      CLOUD_DIR="$CLOUD_SAVE_DIR/$(date +%Y-%m-%d)"
  fi

  if [ ! -d "$SAVE_DIR" ]; then
      mkdir -p $SAVE_DIR
  fi
  if [ ! -d "$CLOUD_DIR" ]; then
      mkdir -p $CLOUD_DIR
  fi

  filename_prefix="$(date +%Y-%m-%d_%H%M%S)"
  capture_date="$(date +%Y-%m-%d)"
  capture_date_hour="$(date +%Y-%m-%d_%H)"
  current_time="$(date +%H:%M)"
  current_time_hour=$(date -d $current_time "+%k")

  # Configure IR led and IR cut based on times of day
  IR_LED_STATUS=$(ir_led status)
  IR_CUT_STATUS=$(ir_cut status)
  RTSP_SERVER_STATUS=$(rtsp_h264_server status)
  # echo "[STATUS]: IR CUT: $IR_CUT_STATUS at $filename_prefix"
  # echo "[STATUS]: IR LED: $IR_LED_STATUS at $filename_prefix"
  # echo "[STATUS]: Current time hour: $current_time_hour at $filename_prefix"

  if [[ $RTSP_SERVER_STATUS == "OFF" ]]; then
      rtsp_h264_server on
      # echo "[STATUS]: RTSP server turned ON"
  fi

  if [[ $current_time_hour -lt $day_end_time && $current_time_hour -gt $day_start_time ]]; then
    # echo "[STATUS]: it is currently daytime."
    if [[ $IR_LED_STATUS == "ON" ]]; then
        ir_led off &&
        echo "Toggled IR LED off: {$IR_LED_STATUS} at {$filename_prefix}"
    fi
    if [[ $IR_CUT_STATUS == "OFF" ]]; then
        ir_cut on &&
        sleep 5
        echo "Toggled IR CUT on: {$IR_CUT_STATUS} at {$filename_prefix}"
    fi
  else
    # echo "[STATUS]: it is currently nighttime."
    if [[ $IR_LED_STATUS == "OFF" ]]; then
        ir_led on &&
        echo "Toggled IR LED on: {$IR_LED_STATUS} at {$filename_prefix}"
    fi
    if [[ $IR_CUT_STATUS == "ON" ]]; then
        ir_cut off &
        sleep 2
        echo "Toggled IR CUT off: {$IR_CUT_STATUS} at {$filename_prefix}"
    fi
  fi
  # wait for modules to change
  sleep 5

  if [ "$filename_prefix" = "$last_prefix" ]; then
      counter=$(($counter + 1))
  else
      counter=1
      last_prefix="$filename_prefix"
  fi
  counter_formatted=$(printf "%03d" $counter)
  fileName="${filename_prefix}_${counter_formatted}.jpg"

  # get the image
  /system/sdcard/bin/getimage > "$SAVE_DIR/$fileName" &&

  # turn off the rtsp server
  rtsp_h264_server off

  image="$SAVE_DIR/$fileName"
  image_size=`du -s  ${image} | cut -c1`

  if [[ $image_size -gt 0 ]]; then
      # echo "image size greater than 0"
      # Added --max-time 20 to command to end the process in order to try again
      # Construct header http put request to aws s3
      aws_path="/${CAMERAID}/${capture_date}/${capture_date_hour}/"
      bucket=$S3BUCKET
      date=$(date +"%a, %d %b %Y %T %z")
      content_type="application/octet-stream"
      string="PUT\n\n$content_type\n$date\n/$bucket$aws_path$fileName"
      signature=$(echo -en "${string}" | /system/sdcard/bin/openssl sha1 -hmac "${S3SECRETKEY}" -binary | /system/sdcard/bin/openssl enc -base64)
      /system/sdcard/bin/curl --max-time 15 -X PUT -T "$SAVE_DIR/$fileName" \
        -H "Host: $bucket.s3.amazonaws.com" \
        -H "Date: $date" \
        -H "Content-Type: $content_type" \
        -H "Authorization: AWS ${S3ACCESSKEY}:$signature" \
        "https://$bucket.s3.amazonaws.com$aws_path$fileName"

      res=$?

      if test "$res" != "0"; then
        echo "the curl command failed with: $res"
        echo "Trying again"
        # Construct header http put request to aws s3
        aws_path="/${CAMERAID}/${capture_date}/${capture_date_hour}/"
        bucket=$S3BUCKET
        date=$(date +"%a, %d %b %Y %T %z")
        content_type="application/octet-stream"
        string="PUT\n\n$content_type\n$date\n/$bucket$aws_path$fileName"
        signature=$(echo -en "${string}" | /system/sdcard/bin/openssl sha1 -hmac "${S3SECRETKEY}" -binary | /system/sdcard/bin/openssl enc -base64)
        /system/sdcard/bin/curl --max-time 10 -X PUT -T "$SAVE_DIR/$fileName" \
            -H "Host: $bucket.s3.amazonaws.com" \
            -H "Date: $date" \
            -H "Content-Type: $content_type" \
            -H "Authorization: AWS ${S3ACCESSKEY}:$signature" \
            "https://$bucket.s3.amazonaws.com$aws_path$fileName"
        res2=$?
        if test "$res2" != "0"; then
          echo "the curl command failed with: $fileName and $res2"
        fi
      else
        mv "${SAVE_DIR}/${fileName}" "${CLOUD_DIR}/${fileName}"
      fi

      if [ -f "${SAVE_DIR}/${fileName}" ]; then
        aws_path="/${CAMERAID}/${capture_date}/${capture_date_hour}/"
        bucket=$S3BUCKET
        date=$(date +"%a, %d %b %Y %T %z")
        content_type="application/octet-stream"
        string="PUT\n\n$content_type\n$date\n/$bucket$aws_path$fileName"
        signature=$(echo -en "${string}" | /system/sdcard/bin/openssl sha1 -hmac "${S3SECRETKEY}" -binary | /system/sdcard/bin/openssl enc -base64)
        /system/sdcard/bin/curl --max-time 5 -X PUT -T "$SAVE_DIR/$fileName" \
            -H "Host: $bucket.s3.amazonaws.com" \
            -H "Date: $date" \
            -H "Content-Type: $content_type" \
            -H "Authorization: AWS ${S3ACCESSKEY}:$signature" \
            "https://$bucket.s3.amazonaws.com$aws_path$fileName" &&

        res=$?
        if test "$res" != "0"; then
          echo "the curl command failed with: $res"
        else
          mv "${SAVE_DIR}/${fileName}" "${CLOUD_DIR}/${fileName}"
        fi

      fi
    else
      echo "image size not greater than 0"
      mv "${SAVE_DIR}/${fileName}" "${CLOUD_DIR}/${fileName}"
  fi

  # Turn off IR led inbetween camera capture based on times of day
  IR_LED_STATUS=$(ir_led status)
  if [ $IR_LED_STATUS == "ON" ]; then
    ir_led off
  fi
}

while true; do
    capturePutS3IR &
    # wait for the specified interval
    sleep $SENDINGIMAGES_INTERVAL
done
