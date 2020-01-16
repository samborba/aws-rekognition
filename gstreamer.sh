#!/bin/bash

cd .. && cd amazon-kinesis-video-streams-producer-sdk-cpp && cd kinesis-video-native-build && cd downloads && cd local && cd bin && gst-launch-1.0 v4l2src device=/dev/video0 ! \
videoconvert ! video/x-raw,format=I420,width=640,height=480 ! \
x264enc bframes=0 key-int-max=45 bitrate=512 tune=zerolatency ! h264parse ! \
video/x-h264,stream-format=avc,alignment=au,profile=baseline ! \
kvssink stream-name=$1 \
storage-size=512 \
access-key=$2 \
secret-key=$3 \
aws-region=$4