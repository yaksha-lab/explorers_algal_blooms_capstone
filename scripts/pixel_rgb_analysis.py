from collections import Counter
import os
import cv2
import matplotlib.pyplot as plt

# https://realpython.com/python-histograms/#:~:text=Histograms%20in%20Pure%20Python,-When%20you%20are&text=count_elements()%20returns%20a%20dictionary,value%20in%20hist%20by%201.%E2%80%9D

from collections import Counter
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
import tqdm

import argparse

parser = argparse.ArgumentParser(description='Analyze training/validation/test RGB Channel Distribution')

parser.add_argument('--img_dir', type=str,
                    help='Path for training/validation/test images')

args = parser.parse_args()

img_dir = args.img_dir

pixel_count_dict = {
                    'RED' : {},
                    'GREEN' : {},
                    'BLUE' : {}
                    }

def analyze_rgb_distribution(img_dir, pixel_count_dict):

    img_list = [os.path.join(img_dir,i) for i in os.listdir(img_dir)]

    total_pixels = 0

    for img_path in tqdm.tqdm(img_list, total=len(img_list)):

        img = Image.open(img_path).convert('RGB')
        img_arr = np.asarray(img)

        for i in range(img_arr.shape[0]):
            for j in range(img_arr.shape[1]):
                coordinate = y, x = j, i
                RED, GREEN, BLUE = img.getpixel(coordinate)
                ###
                if RED not in pixel_count_dict['RED']:
                    pixel_count_dict['RED'][RED] = 1
                else:
                    pixel_count_dict['RED'][RED] += 1

                if GREEN not in pixel_count_dict['GREEN']:
                    pixel_count_dict['GREEN'][GREEN] = 1
                else:
                    pixel_count_dict['GREEN'][GREEN] += 1

                if BLUE not in pixel_count_dict['BLUE']:
                    pixel_count_dict['BLUE'][BLUE] = 1
                else:
                    pixel_count_dict['BLUE'][BLUE] += 1
                ###
        total_pixels+=(img_arr.shape[0]*img_arr.shape[1])
        
    for i in pixel_count_dict:
        for j in pixel_count_dict[i]:
            pixel_count_dict[i][j] = pixel_count_dict[i][j]/total_pixels

    print('RGB Channel Distribution Finished')

    return pixel_count_dict
####
def generate_rgb_dist_plot(pixel_count_dict):

    RED_sorted_dict = dict(sorted(pixel_count_dict['RED'].items(), key=lambda x:x[0]))
    RED_dist_x = [key for key in RED_sorted_dict.keys()]
    RED_dist_y = [val*100 for val in RED_sorted_dict.values()]

    GREEN_sorted_dict = dict(sorted(pixel_count_dict['GREEN'].items(), key=lambda x:x[0]))
    GREEN_dist_x = [key for key in GREEN_sorted_dict.keys()]
    GREEN_dist_y = [val*100 for val in GREEN_sorted_dict.values()]

    BLUE_sorted_dict = dict(sorted(pixel_count_dict['BLUE'].items(), key=lambda x:x[0]))
    BLUE_dist_x = [key for key in BLUE_sorted_dict.keys()]
    BLUE_dist_y = [val*100 for val in BLUE_sorted_dict.values()]

    plt.title("RGB Channel Distribution by Percentage")
    plt.plot(RED_dist_x, RED_dist_y, 'red')
    plt.plot(GREEN_dist_x, GREEN_dist_y, 'green')
    plt.plot(BLUE_dist_x, BLUE_dist_y, 'blue')
    plt.xlabel('RGB Color Value')
    plt.ylabel('Total Pixels (%)')
    plt.savefig('RGB_HIST.png')
    plt.close()
####
pixel_count_dict = analyze_rgb_distribution(img_dir, pixel_count_dict)
generate_rgb_dist_plot(pixel_count_dict)

# def add_dicts(main_dict,new_dict):
#
#     for key, val in new_dict.items():
#         if key in main_dict:
#             main_dict[key] += new_dict[key]
#         else:
#             main_dict[key] = new_dict[key]
#     return main_dict
#
# # noaa_algal_blooms_folder_path = 'noaa_imgs_color'
# noaa_algal_blooms_folder_path = 'noaa_imgs_colorv2'
# noaa_algal_blooms_analysis_folder_path = noaa_algal_blooms_folder_path+'_analysis'
# noaa_images = os.listdir(noaa_algal_blooms_folder_path)
#
# all_blue = {}
# all_green = {}
# all_red = {}
#
# counter=0
# exception_counter=0
# for image in noaa_images:
#     local_image_path = os.path.join(noaa_algal_blooms_folder_path,image)
#     img = cv2.imread(local_image_path)
#     channels = cv2.split(img) # ("b", "g", "r")
#     # cv2.imshow('test',img)
#     # cv2.waitKey(0)
#     blue = Counter(channels[0].flatten().tolist())
#     green = Counter(channels[1].flatten().tolist())
#     red = Counter(channels[2].flatten().tolist())
#
#     ####
#     plt.title("Blue")
#     plt.bar(blue.keys(), blue.values(), 1, color='b')
#     plt.hist()
#     plt.savefig('{}/blue_{}.png'.format(noaa_algal_blooms_analysis_folder_path,image))
#     plt.close()
#     ####
#     plt.title("Green")
#     plt.bar(all_green.keys(), all_green.values(), 1, color='g')
#     plt.savefig('{}/green_{}.png'.format(noaa_algal_blooms_analysis_folder_path,image))
#     plt.close()
#     ####
#     plt.title("Red")
#     plt.bar(all_red.keys(), all_red.values(), 1, color='r')
#     plt.savefig('{}/red_{}.png'.format(noaa_algal_blooms_analysis_folder_path,image))
#     plt.close()
#     ###
#     all_blue = add_dicts(all_blue, blue)
#     all_green = add_dicts(all_green, green)
#     all_red = add_dicts(all_red, red)
#
#     counter+=1
#     print(counter)
#     break
#     # if counter == 2:
#     #     break
#
# plt.bar(all_blue.keys(), all_blue.values(), 1, color='b')
# plt.savefig('all_blue2.png')
# plt.close()
# plt.bar(all_green.keys(), all_green.values(), 1, color='g')
# plt.savefig('all_green2.png')
# plt.close()
# plt.bar(all_red.keys(), all_red.values(), 1, color='r')
# plt.savefig('all_red2.png')
# plt.close()
