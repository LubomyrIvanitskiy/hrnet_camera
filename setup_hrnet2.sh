#!/bin/bash
# Download and setup HRNet
HRNET=hrnet
git clone https://github.com/LubomyrIvanitskiy/HRNet.git $HRNET
sh $HRNET/setup.sh