# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:59:19 2017

@author: Toshiharu
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create binary thresholded images to isolate lane line pixels
def abs_sobel_xy(img, sobel_kernel=3, orient='x',sxy_thresh=(0,255)):
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = np.copy(img)
    # Take the derivative in x or y given orient = 'x' or 'y'
    if (orient == 'x'):
        sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = sobel_kernel)
    elif(orient == 'y'):
        sobel = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = sobel_kernel)
    else:
        raise Exception("Invalid orientation")

    abs_sobel = np.absolute(sobel)   # Take the absolute value of the derivative or gradient
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))  #Scale to 8-bit (0 - 255) then convert to type = np.uint8
    sxbinary = np.zeros_like(scaled_sobel) 
    sxbinary[(scaled_sobel >= sxy_thresh[0]) & (scaled_sobel <= sxy_thresh[1])] = 1 # Create a mask of 1's

    return sxbinary

def dir_sobel(img, sobel_kernel=15, dir_thresh=(3.14/2*0.95, 3.14/2*1.05)):
    img = np.copy(img)
    # Apply the following steps to img
    # 1) Convert to grayscale
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 2) Take the gradient in x and y separately
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = sobel_kernel)
    # 3) Take the absolute value of the x and y gradients
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
     # 4) Use np.arctan2(abs_sobely, abs_sobelx) to calculate the direction of the gradient 
    directions = np.arctan2(abs_sobely, abs_sobelx)
    # 5) Create a binary mask where direction thresholds are met
    sxbinary = np.zeros_like(directions)
    sxbinary[(directions >= dir_thresh[0]) & (directions <= dir_thresh[1])] = 1

    return sxbinary

def mag_sobel(img, sobel_kernel=11, mag_thresh=(30,100)):
    img = np.copy(img) 
    # Apply the following steps to img
    # 1) Convert to grayscale
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 2) Take the gradient in x and y separately
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = sobel_kernel)
    # 3) Calculate the magnitude 
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    # 4) Scale to 8-bit (0 - 255) and convert to type = np.uint8
    scaled_sobel = np.uint8(255*gradmag/np.max(gradmag))
    # 5) Create a binary mask where mag thresholds are met
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= mag_thresh[0]) & (scaled_sobel <= mag_thresh[1])] = 1
    
    return sxbinary


def Multifilter(img,s_thresh=(180, 255),b_thresh=(155,200),l_thresh=(225,255),sxy_thresh=(20,100), show=True):

    s_channel = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)[:,:,1]
    plt.imshow(s_channel)
    plt.show()
    
    l_channel = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)[:,:,0]

    b_channel = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)[:,:,2]   

#    # Threshold color channel
#    s_thresh_min = 180
#    s_thresh_max = 255
#    s_binary = np.zeros_like(s_channel)
#    s_binary[(s_channel >= s_thresh_min) & (s_channel <= s_thresh_max)] = 1
#    
#    b_thresh_min = 155
#    b_thresh_max = 200
#    b_binary = np.zeros_like(b_channel)
#    b_binary[(b_channel >= b_thresh_min) & (b_channel <= b_thresh_max)] = 1
#    
#    l_thresh_min = 225
#    l_thresh_max = 255
#    l_binary = np.zeros_like(l_channel)
#    l_binary[(l_channel >= l_thresh_min) & (l_channel <= l_thresh_max)] = 1
    
    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    
    b_binary = np.zeros_like(b_channel)
    b_binary[(b_channel >= b_thresh[0]) & (b_channel <= b_thresh[1])] = 1
    
    l_binary = np.zeros_like(l_channel)
    l_binary[(l_channel >= l_thresh[0]) & (l_channel <= l_thresh[1])] = 1
    
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float)
    sobelxy_binary = abs_sobel_xy(gray, sobel_kernel=3, orient='x',sxy_thresh=sxy_thresh)
    sobel_mag = mag_sobel(gray,sobel_kernel=3)
    sobel_dir = dir_sobel(gray)
    #color_binary = np.dstack((u_binary, s_binary, l_binary))
    
    combined_binary = np.zeros_like(s_binary)
    combined_binary[(s_binary == 1) | (b_binary == 1)] = 1

    if show == True:
        # Plotting thresholded images
        f, ((ax1, ax2, ax3), (ax4,ax5, ax6)) = plt.subplots(2, 3, sharey='col', sharex='row', figsize=(10,4))
        f.tight_layout()
        
        ax1.set_title('Original Image', fontsize=16)
        ax1.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB).astype('uint8'))
        
        ax2.set_title('sobelxy binary threshold', fontsize=16)
        ax2.imshow(dir_sobel(gray), cmap='gray')
        
        ax3.set_title('b binary threshold', fontsize=16)
        ax3.imshow(b_binary, cmap='gray')
        
        ax4.set_title('l binary threshold', fontsize=16)
        ax4.imshow(l_binary, cmap='gray')
        
        ax5.set_title('H-HSV binary threshold', fontsize=16)
        ax5.imshow(s_binary, cmap='gray')

        ax6.set_title('Combined color thresholds', fontsize=16)
        ax6.imshow(combined_binary, cmap='gray')
        
        
    else: 
        return combined_binary

import pickle

calibration_par = 'camera_cal/calibration.p'
dist_pickle = pickle.load( open( calibration_par, "rb" ) )
mtx = dist_pickle["mtx"]
dist = dist_pickle["dist"]

# Load perpective matrices
perspective_mat = 'camera_cal/perspective.p'
dist_pickle = pickle.load( open( perspective_mat, "rb" ) )
M = dist_pickle["M"]
Minv = dist_pickle["Minv"]
    
from imageProcessing import perspectiveCal,Calibration,birdEye
    
test1 = cv2.imread('test_images/test5.jpg')
top_down = birdEye(test1, mtx, dist,M)
Multifilter(top_down,s_thresh=(210, 255),b_thresh=(145,200),l_thresh=(220,255),sxy_thresh=(20,100), show=True)