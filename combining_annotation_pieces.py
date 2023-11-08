import pandas as pd
import os
import glob
import numpy as np

# replace with your folder's path
#folder_path = r'./datasets/ava_frame/annotations'

#all_files = os.listdir(folder_path)

#npfiles = ['annotations_values1.npy','annotations_values2.npy', 'annotations_values3.npy', 'annotations_values4.npy', 'annotations_values5.npy', 'annotations_values6.npy', 
#            'annotations_values7.npy', 'annotations_values8.npy', 'annotations_values9.npy', 'annotations_values10.npy', 'annotations_values11.npy', 'annotations_values12.npy']

#all_arrays = np.load(os.path.join('./datasets/ava_frame/annotations/annotations_values1.npy'))
#all_arrays = []
#for npfile in npfiles:
#    a = np.load(os.path.join('./datasets/ava_frame/annotations/', npfile))
#    print(len(a))
#    print(len(a[0]))
#    for item in a:
#        all_arrays.append(item)
#    #print(all_arrays)
#all_array = np.array(all_arrays)
#print(all_array)
#np.save('./datasets/ava_frame/annotations/ava_frame_dataset_target.npy', all_array)


df_or= pd.read_csv('./datasets/ava_frame/annotations/ava_frame_filtered_dataset.csv')

df= df_or.sample(frac=1).reset_index(drop=True)

print(df.shape[0])
alpha_val = 0.2
val_len = int(alpha_val*df.shape[0])
print(val_len)
alpha_test = 0.2
test_len = int(alpha_test*df.shape[0])
print(test_len)

val_df = df[:val_len]
annotations= []
for index, row in val_df.iterrows():
    url_id = row['url_id']
    second = row['Second']
    ann_vec = [0]*80
    actions_lab = row['Actions_id']
    actions_lab = [int(x) for x in actions_lab.replace('[','').replace(']','').split()]
    for idx, val in enumerate(actions_lab):
        ann_vec[int(val)-1] = 1
    annotations.append(ann_vec)

#print(annotations)

np.save('./datasets/ava_frame/annotations/val_set_anno.npy', annotations)
val_df.to_csv('./datasets/ava_frame/annotations/val_set_image_list.csv', index=False)

test_df = df[val_len:val_len+test_len]
annotations= []
for index, row in test_df.iterrows():
    url_id = row['url_id']
    second = row['Second']
    ann_vec = [0]*80
    actions_lab = row['Actions_id']
    actions_lab = [int(x) for x in actions_lab.replace('[','').replace(']','').split()]
    for idx, val in enumerate(actions_lab):
        ann_vec[int(val)-1] = 1
    annotations.append(ann_vec)

np.save('./datasets/ava_frame/annotations/test_set_anno.npy', annotations)
test_df.to_csv('./datasets/ava_frame/annotations/test_set_image_list.csv', index=False)

train_df = df[val_len+test_len:]
annotations= []
for index, row in train_df.iterrows():
    url_id = row['url_id']
    second = row['Second']
    ann_vec = [0]*80
    actions_lab = row['Actions_id']
    actions_lab = [int(x) for x in actions_lab.replace('[','').replace(']','').split()]
    for idx, val in enumerate(actions_lab):
        ann_vec[int(val)-1] = 1
    annotations.append(ann_vec)

np.save('./datasets/ava_frame/annotations/train_set_anno.npy', annotations)
train_df.to_csv('./datasets/ava_frame/annotations/train_set_image_list.csv', index=False)
