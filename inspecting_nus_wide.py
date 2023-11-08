import sys
sys.path.insert(0, './')
sys.path.insert(0, '../')
import numpy as np
import torch.utils.data as data
from PIL import Image
import torch
import os
import torchvision.transforms as transforms
from dataloaders.helper import CutoutPIL
from randaugment import RandAugment
import pickle

data_split = 'train'

ann_file_names = {'train': 'formatted_train_all_labels_filtered.npy',
                    'val': 'formatted_val_all_labels_filtered.npy',
                    'val_gzsl': 'formatted_val_gzsl_labels_filtered_small.npy',
                    'test_gzsl': 'formatted_val_gzsl_labels_filtered.npy'}
img_list_name = {'train': 'formatted_train_images_filtered.npy',
                    'val': 'formatted_val_images_filtered.npy',
                    'val_gzsl': 'formatted_val_gzsl_images_filtered_small.npy',
                    'test_gzsl': 'formatted_val_gzsl_images_filtered.npy'}

annFile = os.path.join('./datasets/nus_wide/annotations', 'zsl', ann_file_names[data_split])
prova= np.load(annFile)
#print(prova)
#print(len(prova))
#print(len(prova[0]))
#res = [idx for idx, val in enumerate(prova[10]) if val != 0]
#res2 = [val for idx, val in enumerate(prova[10]) if val != 0]
 
# printing result
#print("Indices of Non-Zero elements : " + str(res))
#print("Values of Non-Zero elements : " + str(res2))


cls_id = pickle.load(open(os.path.join('./datasets/nus_wide/annotations', 'zsl', "cls_id.pickle"), "rb"))
print('*****cls_id*****')
print(cls_id)

cls_id = cls_id['seen']
print('*****seen*****')
print(len(cls_id))

cls_id = pickle.load(open(os.path.join('./datasets/nus_wide/annotations', 'zsl', "cls_id.pickle"), "rb"))
cls_id = cls_id['unseen']
print('*****unseen*****')
#print(len(cls_id))

cls_id = pickle.load(open(os.path.join('./datasets/nus_wide/annotations', 'zsl', "cls_id.pickle"), "rb"))            
cls_id = list(range(1006))
print('*****zsl*****')
#print(cls_id)

image_list = os.path.join('./datasets/nus_wide/annotations', 'zsl', img_list_name[data_split])
#print(np.load(image_list))

import pickle 

cls_id = {'seen': [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 22, 26, 28, 29, 30, 
            34, 36, 38, 41, 43, 45, 46, 48, 49, 51, 52, 54, 56, 57, 58, 59, 61, 62, 63, 64, 
            65, 66, 67, 68, 69, 70, 72, 73, 74, 76, 77, 78, 79, 80], 
        'unseen': [24, 60, 37, 47, 27, 17]}

# with open('cls_id.pkl', 'wb') as f:  # open a text file
#     pickle.dump(cls_id, f) # serialize the list
#     f.close()
