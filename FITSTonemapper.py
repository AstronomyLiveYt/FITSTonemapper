import numpy as np
import math
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import skycoord_to_pixel
from astropy.io.fits import getheader
from astropy.utils.data import get_pkg_data_filename
from astropy.coordinates import FK5
from PIL import Image
import cv2
import os
import sys
import fnmatch


pattern = '*.fit*'
filelist = os.listdir('.')    
firstimage = True       
for idx, entry in enumerate(filelist):
    if fnmatch.fnmatch(entry,pattern):
        skip = False
        image_data = fits.getdata(entry)
        imagenew = np.array(image_data,dtype = np.float32)
        imagenew = np.moveaxis(imagenew, 0, 2)
        print(entry)
        frame_height, frame_width, channels = imagenew.shape
        tonemap = cv2.createTonemapReinhard(1, 0,0,1)
        imagenormalized = tonemap.process(imagenew)
        eightbit =  np.clip(imagenormalized*255, 0, 255).astype('uint8')
        
        hsvImg = cv2.cvtColor(eightbit,cv2.COLOR_BGR2HSV)

        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*1.5

        #multiple by a factor of less than 1 to reduce the brightness 
        #hsvImg[...,2] = hsvImg[...,2]*0.6

        eightbit=cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        if firstimage is True:
            out = cv2.VideoWriter('FITSHDRout.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width,frame_height))
            firstimage = False
        out.write(eightbit)
        cv2.imshow('Processed', eightbit)
        cv2.waitKey(1)
        cv2.imwrite(str(str(entry.split('.')[0])+str(idx)+'_aligned.jpg'), eightbit)

out.release()
