#!/bin/bash
# Download and setup HRNet
HRNET=hrnet
git clone https://github.com/LubomyrIvanitskiy/HRNet.git $HRNET
rm -r weights
mkdir weights
wget -nc -O weights/pose_hrnet_w32_256x192.pth https://www.dropbox.com/s/85toprbvlzzslyk/pose_hrnet_w32_256x192.pth?dl=0