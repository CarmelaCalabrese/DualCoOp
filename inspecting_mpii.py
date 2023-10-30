import scipy.io
import numpy as np
import os
import sys
import copy
from pathlib import Path

import scipy.io
import numpy as np
from tqdm import tqdm
#from adjustText import adjust_text
from matplotlib import pyplot as plt
from matplotlib.patches import Circle



#./datasets/mpii/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat

# Load the mat file.
matlab_mpii = scipy.io.loadmat('./datasets/mpii/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat', struct_as_record=False)['RELEASE'][0, 0]
num_images = annotation_mpii = matlab_mpii.__dict__['annolist'][0].shape[0]
print('num_images')
print(num_images)

initial_index = 0

categories = []
actions = []
ident = []
count_empty = 0

file = open("dataset.txt", "w")

# Iterate over each image
for img_idx in tqdm(range(initial_index, num_images)):
    annotation_mpii = matlab_mpii.__dict__['annolist'][0, img_idx]

    # Load the individual image.
    img_name = annotation_mpii.__dict__['image'][0, 0].__dict__['name'][0]
    #print('img_name')
    #print(img_name)

    action_mpii = matlab_mpii.__dict__['act'][img_idx,0]
    if not action_mpii.__dict__['cat_name']:
        #print('Empty label')
        count_empty += 1
        file.write(str(img_name) + "\n")
        continue
    cat_name = action_mpii.__dict__['cat_name'][0]
    categories.append(cat_name)
    act_name = action_mpii.__dict__['act_name'][0]
    single_act_name = act_name.split(',')
    for act_lab in single_act_name:
        #print(act_lab)
        #actions.append(act_lab)
        actions.append(act_name)
    act_id = action_mpii.__dict__['act_id'][0][0]
    ident.append(act_id)

    file.write(str(img_name) + "\t" + "\t" + str(cat_name) + "\t" + "\t" + str(act_name) + "\t" + "\t" + str(act_id) +"\n")

file.close()

print('We have # empty label images')
print(count_empty)


###
file2 = open("unique_categories.txt", "w")
set_categories = set(categories) 
print("The unique elements of the categories:\n") 
list_categories = (list(set_categories))
 
for item in list_categories: 
    file2.write(str(item.lstrip())+"\n")
    #print(item) 
file2.close()

print('Dimension categories:')
print(len(list_categories))


###
file3 = open("unique_actions.txt", "w")
set_actions = set(actions) 
print("The unique elements of the actions:\n") 
list_actions = (list(set_actions))

print('List of actions')
print(list_actions)
 
for item in list_actions: 
    file3.write(str(item.lstrip())+"\n")
    #print(item) 
file3.close()

print('Dimension actions:')
print(len(list_actions))


###
set_ident = set(ident) 
print("The unique elements of the ident:\n") 
list_ident = (list(set_ident))
 
# for item in list_ident: 
#     print(item) 

print('Dimension ident:')
print(len(list_ident))