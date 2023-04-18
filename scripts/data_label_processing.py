from collections import Counter
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
import tqdm

import argparse
import sys

parser = argparse.ArgumentParser(description='Process Algal Blooms Images')

parser.add_argument('--img_dir', type=str,
                    help='Path for training/validation/test images')
parser.add_argument('--label_dir', type=str,
                    help='Path for ground truth labels')
parser.add_argument('--new_img_dir', type=str,
                    help='Path for new training/validation/test images')
parser.add_argument('--seg_map_prep_dir', type=str,
                    help='Path for Color Palette Segmentation Maps')
parser.add_argument('--seg_map_dir', type=str,
                    help='Path for training/validation/test Segmentation Maps')

args = parser.parse_args()

img_dir = args.img_dir
label_dir = args.label_dir
new_img_dir = args.new_img_dir
seg_map_prep_dir = args.seg_map_prep_dir
seg_map_dir = args.seg_map_dir

if os.path.isdir(img_dir):
    print('Image Directory: {}'.format(img_dir))
else:
    print('Image Directory does not exist: {}'.format(img_dir))
    print('Exiting...')
    sys.exit(1)

if os.path.isdir(label_dir):
    print('Label Directory: {}'.format(label_dir))
else:
    print('Label Directory does not exist: {}'.format(label_dir))
    print('Exiting...')
    sys.exit(1)

if os.path.isdir(new_img_dir):
    print('New Ground Truth Directory: {}'.format(new_img_dir))
else:
    print('New Ground Truth Directory does not exist: {}'.format(new_img_dir))
    print('Creating New Ground Truth Directory...')
    os.mkdir(new_img_dir)

if os.path.isdir(seg_map_prep_dir):
    print('Color Segmap Directory: {}'.format(seg_map_prep_dir))
else:
    print('Color Segmap Directory does not exist: {}'.format(seg_map_prep_dir))
    print('Creating Color Segmap Directory...')
    os.mkdir(seg_map_prep_dir)

if os.path.isdir(seg_map_dir):
    print('Segmap Directory Directory: {}'.format(seg_map_dir))
else:
    print('Segmap Directory does not exist: {}'.format(seg_map_dir))
    print('Creating Segmap Directory...')
    os.mkdir(seg_map_dir)



classes = ['water',
            'land',
            'clouds',
            'algae']

# https://htmlcolorcodes.com/colors/shades-of-brown/
palette = [(0, 255, 255), #Cyan	#00FFFF	rgb(0, 255, 255)
           (0, 0, 0),   # BLACK
           (0, 0, 0),   # BLACK
           (170, 255, 0),    #Bright Green	#AAFF00	rgb(170, 255, 0)
            ]

class_id = [0,
            1,
            1,
            2
            ]

segmap_class_name_palette_dict = dict(zip(classes,palette))
segmap_class_name_class_id_dict = dict(zip(classes,class_id))

def remove_extra_labels(img_dir,label_dir):

    img_list = [i for i in os.listdir(img_dir)]

    label_list = [i for i in os.listdir(label_dir)]
    label_compare_list = []

    for label in label_list:
        label_split = label.split('.')
        new_label_split = []
        for label_part in label_split:
            if 'CIcyano' in label_part:
                pass
            elif 'rbd_rhos' in label_part:
                pass
            elif 'filt' in label_part:
                pass
            else:
                new_label_split.append(label_part)
        new_label_split.insert(-2,'truecolor')
        new_label = '.'.join(new_label_split)
        label_compare_list.append(new_label)

    for image_pairs in tqdm.tqdm(zip(label_list,label_compare_list),total=len(label_list)):

        if image_pairs[1] in img_list:
            pass
        else:
            label_to_remove = os.path.join(label_dir,image_pairs[0])
            os.remove(label_to_remove)
            print('Label is unpaired: {}'.format(image_pairs[1]))
            print('Removing {}'.format(label_to_remove))

def remove_extra_labels_2(img_dir,label_dir):

    img_list = [i for i in os.listdir(img_dir)]

    label_list = [i for i in os.listdir(label_dir)]
    label_compare_list = label_list

    for image_pairs in tqdm.tqdm(zip(label_list,label_compare_list),total=len(label_list)):

        if image_pairs[1] in img_list:
            pass
        else:
            label_to_remove = os.path.join(label_dir,image_pairs[0])
            os.remove(label_to_remove)
            print('Label is unpaired: {}'.format(image_pairs[1]))
            print('Removing {}'.format(label_to_remove))

def create_extra_ground_truth(img_dir,new_img_dir,label_dir):
    print('Generating New Color Images to Match Ground Truth Label Names')
    img_list = [os.path.join(img_dir,i) for i in os.listdir(img_dir)]
    label_list = [os.path.join(label_dir,i) for i in os.listdir(label_dir)]

    for image_path in tqdm.tqdm(img_list):
        img_name = os.path.split(image_path)[-1]
        img_name = img_name.split('.')[:8]
        img_name = '.'.join(img_name)

        location_name = os.path.split(image_path)[-1].split('.')[-2]

        label_index = []
        
        for i, label_path in enumerate(label_list):
            if img_name in label_path and location_name in label_path:
                label_index.append(i)

        img = Image.open(image_path).convert('RGB')
        label_file_names = [os.path.join(new_img_dir,os.path.split(label_list[i])[-1]) for i in label_index]

        for filename in label_file_names:
            print('Original Image: {}'.format(image_path))
            print('Saving: {}'.format(filename))
            img.save(filename)


def gather_colors(label_dir):

    #### GATHER Images
    color_count_unique_dict = {}
    label_list = [os.path.join(label_dir,i) for i in os.listdir(label_dir)]
    counter = 0

    for label_path in tqdm.tqdm(label_list):
        color_list = []
        label = Image.open(label_path).convert('RGB')
        seg_image = np.asarray(label)

        for i in range(seg_image.shape[0]):
            for j in range(seg_image.shape[1]):
                coordinate = y, x = j, i
                pixel_rgb = label.getpixel(coordinate)
                color_list.append(pixel_rgb)

        color_set_unique = set(color_list)
        color_list_unique = list(color_set_unique)

        for color in color_list_unique:
            if color in color_count_unique_dict:
                color_count_unique_dict[color]+=1
            else:
                color_count_unique_dict[color]=1
        counter+=1
        if counter == 5:
            break
    for key in color_count_unique_dict:
        print('{}, {}'.format(key, color_count_unique_dict[key]))

def generate_segmap(label_dir, seg_map_dir):
    print('Generating Segmentation Maps')
    label_list = [os.path.join(label_dir,i) for i in os.listdir(label_dir)]
    segmap_list = [os.path.join(seg_map_dir,i) for i in os.listdir(label_dir)]

    label_name_list = [i for i in os.listdir(label_dir)]
    label_compare_list = segmap_list

    counter = 0

    for label_path in tqdm.tqdm(zip(label_list,segmap_list,label_compare_list),total=len(label_list)):
        color_list = []
        label = Image.open(label_path[0]).convert('RGB')
        seg_image = np.asarray(label)
        seg_map = np.zeros(seg_image.shape[0:2])

        for i in range(seg_image.shape[0]):
            for j in range(seg_image.shape[1]):
                coordinate = y, x = j, i
                pixel_rgb = label.getpixel(coordinate)

                #### PIXEL REMAP STATEMENTS
                segmap_pixel_rgb = 0
                if pixel_rgb == (0, 0, 0):
                    segmap_pixel_rgb = segmap_class_name_class_id_dict['water']
                elif pixel_rgb == (247, 247, 247) or pixel_rgb == (150, 150, 150):
                    segmap_pixel_rgb = segmap_class_name_class_id_dict['land']
                elif len(set(pixel_rgb))==1 and pixel_rgb != (0, 0, 0) and pixel_rgb != (247, 247, 247):
                    segmap_pixel_rgb = segmap_class_name_class_id_dict['clouds']
                else:
                    segmap_pixel_rgb = segmap_class_name_class_id_dict['algae']

                seg_map[i,j] = segmap_pixel_rgb
        print(label_path[2])
        seg_map_img = Image.fromarray(np.uint8(seg_map))
        print(seg_map_img)
        seg_map_img.save(label_path[2])

        counter+=1

def generate_color_segmap(label_dir, seg_map_dir):
    print('Generating Segmentation Maps')
    label_list = [os.path.join(label_dir,i) for i in os.listdir(label_dir)]
    segmap_list = [os.path.join(seg_map_dir,i) for i in os.listdir(label_dir)]

    label_name_list = [i for i in os.listdir(label_dir)]
    label_compare_list = segmap_list

    counter = 0

    for label_path in tqdm.tqdm(zip(label_list,segmap_list,label_compare_list),total=len(label_list)):
        color_list = []
        label = Image.open(label_path[0]).convert('RGB')
        seg_image = np.asarray(label)
        seg_map = np.zeros(seg_image.shape)

        for i in range(seg_image.shape[0]):
            for j in range(seg_image.shape[1]):
                coordinate = y, x = j, i
                pixel_rgb = label.getpixel(coordinate)

                #### PIXEL REMAP STATEMENTS
                segmap_pixel_rgb = 0
                if pixel_rgb == (0, 0, 0):
                    segmap_pixel_rgb = segmap_class_name_palette_dict['water']
                elif pixel_rgb == (247, 247, 247) or pixel_rgb == (150, 150, 150):
                    segmap_pixel_rgb = segmap_class_name_palette_dict['land']
                elif len(set(pixel_rgb))==1 and pixel_rgb != (0, 0, 0) and pixel_rgb != (247, 247, 247):
                    segmap_pixel_rgb = segmap_class_name_palette_dict['clouds']
                else:
                    segmap_pixel_rgb = segmap_class_name_palette_dict['algae']

                seg_map[i,j] = segmap_pixel_rgb
        print(label_path[2])
        seg_map_img = Image.fromarray(np.uint8(seg_map))
        print(seg_map_img)
        seg_map_img.save(label_path[2])

        counter+=1

remove_extra_labels(img_dir,label_dir)
create_extra_ground_truth(img_dir,new_img_dir,label_dir)
# remove_extra_labels_2(new_img_dir,label_dir)
# generate_segmap(label_dir, seg_map_dir)
# generate_color_segmap(label_dir, seg_map_prep_dir)
