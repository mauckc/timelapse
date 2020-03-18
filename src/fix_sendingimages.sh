#!/bin/sh
# PIDFILE="/run/uploadclean.pid"
SENDINGIMAGES_CONF="/system/sdcard/config/sendingimages.conf"
BASE_SAVE_DIR="/system/sdcard/DCIM/local/precloud"
CLOUD_SAVE_DIR="/system/sdcard/DCIM/local/cloud"

# if [ -f "$SENDINGIMAGES_CONF" ]; then
. "$SENDINGIMAGES_CONF" 2>/dev/null
# fi

function cleanUploads3
{
  fileName=$1
  capture_date="$(echo $fileName | cut -c 1-10)"
  capture_date_hour="$(echo $fileName | cut -c 1-13)"
  SAVE_DIR="$BASE_SAVE_DIR/$capture_date"
  CLOUD_DIR="$CLOUD_SAVE_DIR/$capture_date"
  aws_path="/${CAMERAID}/${capture_date}/${capture_date_hour}/"
  bucket=$S3BUCKET
  date=$(date +"%a, %d %b %Y %T %z")
  content_type="application/octet-stream"
  string="PUT\n\n$content_type\n$date\n/$bucket$aws_path$fileName"
  signature=$(echo -en "${string}" | /system/sdcard/bin/openssl sha1 -hmac "${S3SECRETKEY}" -binary | /system/sdcard/bin/openssl enc -base64)
  /system/sdcard/bin/curl --max-time 10 -X PUT -T "$CLOUD_DIR/$fileName" \
    -H "Host: $bucket.s3.amazonaws.com" \
    -H "Date: $date" \
    -H "Content-Type: $content_type" \
    -H "Authorization: AWS ${S3ACCESSKEY}:$signature" \
    "https://$bucket.s3.amazonaws.com$aws_path$fileName" &&

  res=$?

  if test "$res" != "0"; then
    echo "the curl command failed with: $res"
  else
    echo "Success"
    # mv "${SAVE_DIR}/${fileName}" "${CLOUD_DIR}/${fileName}"
  fi
}

input="/system/sdcard/missing-files.txt"

while IFS= read -r line
do
  echo "$line"
  old_capture_date="$(echo $line | cut -c 1-10)"
  for f in $(ls $CLOUD_SAVE_DIR/$old_capture_date/$line*)
  do
    echo $f
    echo $(basename --"$f")
    cleanUploads3 $(basename --"$f")
  done
done < "$input"
