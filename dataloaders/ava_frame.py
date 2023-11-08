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
import pandas as pd


class AVA_ZSL(data.Dataset):
    def __init__(self, root, data_split, img_size=224, p=1, annFile="", label_mask=None, partial=1+1e-6):
        ann_file_names = {'train': 'train_set_anno.npy',
                          'val': 'val_set_anno.npy',
                          'test': 'test_set_anno.npy'}
        img_list_name = {'train': 'train_set_image_list.csv',
                         'val': 'val_set_image_list.csv',
                         'test': 'test_set_image_list.csv'}
        self.root = root
        class_name_files = os.path.join(self.root, 'annotations', 'all_labels.txt')
        with open(class_name_files) as f:
            classnames = f.readlines()
        self.classnames = [a.strip() for a in classnames]
        print(self.classnames)

        if annFile == "":
            annFile = os.path.join(self.root, 'annotations', ann_file_names[data_split])
        else:
            raise NotImplementedError
        cls_id = pickle.load(open(os.path.join(self.root, 'annotations', "cls_id.pkl"), "rb"))
        if data_split == 'train':
            cls_id = cls_id['seen']
        elif data_split in ['val', 'test']:
            cls_id = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 22, 24, 26, 27, 28, 
                    29, 30, 34, 36, 37, 38, 41, 43, 45, 46, 47, 48, 49, 51, 52, 54, 56, 57, 58, 
                    59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 76, 77, 78, 79, 80]
        else:
            raise ValueError
        self.cls_id = cls_id
        self.anns = np.load(annFile)
        image_list = os.path.join(self.root, 'annotations', img_list_name[data_split])
        image_csv = pd.read_csv(image_list)
        self.image_list = image_csv

        #self.image_list = np.load(image_list) 
        #assert len(self.anns) == len(self.image_list) #controlla che ci siano tutte le annotazioni per ogni immagine
        assert len(self.anns) == len(image_csv)

        self.data_split = data_split
        ids = list(range(len(image_list)))
        if data_split == 'train':
            num_examples = len(ids)
            pick_example = int(num_examples * p)
            self.ids = ids[:pick_example]
        else:
            self.ids = ids

        
        #UGUALE
        train_transform = transforms.Compose([
            # transforms.RandomResizedCrop(img_size)
            transforms.Resize((img_size, img_size)),
            CutoutPIL(cutout_factor=0.5),
            RandAugment(),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
        ])
        #UGUALE
        test_transform = transforms.Compose([
            # transforms.CenterCrop(img_size),
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
        ])

        if self.data_split == 'train':
            self.transform = train_transform
        elif self.data_split in ['val', 'test']:
            self.transform = test_transform
        else:
            raise ValueError('data split = %s is not supported in Ava_frame' % self.data_split)

        # create the label mask
        self.mask = None
        #self.partial = partial
        #if data_split == 'train' and partial < 1.:
        #    if label_mask is None:
        #        rand_tensor = torch.rand(len(self.ids), len(self.classnames))
        #        mask = (rand_tensor < partial).long()
        #        mask = torch.stack([mask], dim=1)
        #        torch.save(mask, os.path.join(self.root, 'annotations', 'partial_label_%.2f.pt' % partial))
        #    else:
        #        mask = torch.load(os.path.join(self.root, 'annotations', label_mask))
        #    self.mask = mask.long()
    
    def __len__(self):
        return len(self.ids)

    def __getitem__(self, index):
        img_id = self.ids[index]
        url_id = image_list[img_id]['url_id']
        sec = image_list[img_id]['Second']
        frame_name= f'url_{url_id}_sec_{sec}.jpg'
        img_path = os.path.join(self.root, 'frames', frame_name)
        img = Image.open(img_path).convert('RGB')
        targets = self.anns[img_id]
        targets = torch.from_numpy(targets).long()
        target = targets[None, ]

        #Ignoring mask-related code pieces because interested in ZSL
        #if self.mask is not None:
        #    masked = - torch.ones((1, len(self.classnames)), dtype=torch.long)
        #    target = self.mask[index] * target + (1 - self.mask[index]) * masked

        if self.transform is not None:
            img = self.transform(img)

        return img, target

    def name(self):
        return 'ava_frame'









