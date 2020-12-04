import sys
import os
import asyncio
import base64
from PIL import Image
import importlib
import cv2
from hrnet.SimpleHRNet import SimpleHRNet

model = SimpleHRNet(32, 17, "../weights/pose_hrnet_w32_256x192.pth", multiperson=False)

def predict_image_points(img):
        pts = model.predict(img)
        import numpy as np
        from hrnet.misc.visualization import draw_points_and_skeleton, joints_dict
        #img = cv2.imread('image.jpg',0) # reads image 'opencv-logo.png' as grayscale
        person_ids = np.arange(len(pts), dtype=np.int32)
        for i, (pt, pid) in enumerate(zip(pts, person_ids)):
                img = draw_points_and_skeleton(img, pt, joints_dict()['coco']['skeleton'], person_index=pid,
                                          points_color_palette='gist_rainbow', skeleton_color_palette='jet',
                                          points_palette_samples=10)
        return img