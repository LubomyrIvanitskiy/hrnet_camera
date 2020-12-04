#!/bin/bash
# Download and setup HRNet
HRNET=hrnet
git clone https://github.com/stefanopini/simple-HRNet.git $HRNET
python -m pip install -r $HRNET/requirements.txt
wget -nc -O weights https://github.com/leoxiaobin/deep-high-resolution-net.pytorch
YOLO=$HRNET/models/detectors/yolo
git clone https://github.com/eriklindernoren/PyTorch-YOLOv3 $YOLO
python -m pip install -r $YOLO/requirements.txt
rm -r weights
mkdir weights
wget -nc -O weights/pose_hrnet_w32_256x192.pth https://www.dropbox.com/s/85toprbvlzzslyk/pose_hrnet_w32_256x192.pth?dl=0