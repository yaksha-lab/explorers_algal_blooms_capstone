from collections import Counter
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
import tqdm

import argparse

parser = argparse.ArgumentParser(description='Analyze training/validation/test Segmentation Map Class Distribution')

parser.add_argument('--seg_map_dir', type=str,
                    help='Path for training/validation/test Segmentation Maps')

args = parser.parse_args()

seg_map_dir = args.seg_map_dir

classes = ['water',
            'land/clouds',
            'algae']

# https://htmlcolorcodes.com/colors/shades-of-brown/
palette = [(0, 255, 255), #Cyan	#00FFFF	rgb(0, 255, 255)
           (0, 0, 0),   # BLACK
           (0, 0, 0),   # BLACK
           (170, 255, 0),    #Bright Green	#AAFF00	rgb(170, 255, 0)
            ]

plot_palette = [(0, 255, 255), #Cyan	#00FFFF	rgb(0, 255, 255)
           (0, 0, 0),   # BLACK
           (170, 255, 0),    #Bright Green	#AAFF00	rgb(170, 255, 0)
            ]
plot_palette = [(R/255, G/255, B/255) for R,G,B in plot_palette]
class_id = [0,
            1,
            2
            ]

segmap_class_name_palette_dict = dict(zip(classes,palette))
segmap_class_name_class_id_dict = dict(zip(classes,class_id))
segmap_class_id_class_name_dict = dict(zip(class_id,classes))

def analyze_class_distribution(seg_map_dir, segmap_class_id_class_name_dict):

    segmap_list = [os.path.join(seg_map_dir,i) for i in os.listdir(seg_map_dir)]

    class_id_list = [key for key in segmap_class_id_class_name_dict.keys()]
    class_count_list = [0 for i in class_id_list]

    class_count_name_list = [segmap_class_id_class_name_dict[key] for key in segmap_class_id_class_name_dict.keys()]

    class_count_dict = dict(zip(class_id_list,class_count_list))
    class_count_name_dict = dict(zip(class_count_name_list,class_count_list))

    total_pixels = 0

    for segmap_path in tqdm.tqdm(segmap_list, total=len(segmap_list)):
        color_list = []
        segmap = Image.open(segmap_path).convert('P')
        seg_image = np.asarray(segmap)

        for i in range(seg_image.shape[0]):
            for j in range(seg_image.shape[1]):
                coordinate = y, x = j, i
                pixel_gray = segmap.getpixel(coordinate)
                class_id = pixel_gray
                class_count_dict[class_id] += 1

        total_pixels+=(seg_image.shape[0]*seg_image.shape[1])
        
    for i in class_count_dict:
        class_count_dict[i] = class_count_dict[i]/total_pixels

    for i, j in zip(class_count_name_dict,class_count_dict):
        class_count_name_dict[i] = class_count_dict[j]

    for key in class_count_name_dict:
        print("{}, {}".format(key, class_count_name_dict[key]))

    return class_count_name_dict
####
def generate_class_dist_plot(class_count_name_dict, classes, plot_palette):

    class_count_name_sorted_dict = dict(sorted(class_count_name_dict.items(), key=lambda x:x[1], reverse=True))
    colors = dict(zip(classes, plot_palette))
    perecentages = [val*100 for val in class_count_name_sorted_dict.values()]

    plt.title("Class Distribution by Percentage")
    plt.bar(class_count_name_sorted_dict.keys(), perecentages, color=[colors[key] for key in class_count_name_sorted_dict])
    plt.xlabel('Class Name')
    plt.ylabel('Total Pixels (%)')
    plt.savefig('CLASS_HIST.png')
    plt.close()

class_count_name_dict = analyze_class_distribution(seg_map_dir, segmap_class_id_class_name_dict)
generate_class_dist_plot(class_count_name_dict, classes, plot_palette)
