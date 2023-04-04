from collections import Counter
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

# https://docs.opencv.org/3.4/d1/db7/tutorial_py_histogram_begins.html
# https://www.cambridgeincolour.com/tutorials/histograms1.htm
# https://en.wikipedia.org/wiki/Color_histogram#:~:text=In%20image%20processing%20and%20photography,set%20of%20all%20possible%20colors.

noaa_algal_blooms_folder_path = 'noaa_imgs_colorv2'
noaa_algal_blooms_analysis_folder_path = noaa_algal_blooms_folder_path+'_analysis'
noaa_images = os.listdir(noaa_algal_blooms_folder_path)

print('Images pulled from: {}'.format(noaa_algal_blooms_folder_path))
print('Image analysis plots saved to {}'.format(noaa_algal_blooms_analysis_folder_path))

all_blue = {}
all_green = {}
all_red = {}

counter=0
exception_counter=0
for image in noaa_images:
    local_image_path = os.path.join(noaa_algal_blooms_folder_path,image)
    img = cv2.imread(local_image_path)
    img_shape = img.shape
    img_size = img.size
    img_dtype = img.dtype
    color = ('BLUE','GREEN','RED')
    hist_list = []
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.rcParams["axes.titlesize"] = 8
    plt.xlabel('Color Brightness Value')
    plt.ylabel('Pixel Count')
    plt.title('RGB Color Channel Histogram\n Image Name: {}\n Image Dimensions: {} (HxWxC), Pixel Count: {}, dtype: {}'.format(image,img_shape,img_size,img_dtype))
    plt.savefig('{}/hist_{}.png'.format(noaa_algal_blooms_analysis_folder_path,image))
    plt.close()

    counter+=1
    print('PNG # {} : {}'.format(counter,image))
