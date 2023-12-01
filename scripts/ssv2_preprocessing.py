import json
import numpy as np
import os
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(prog="ssv2_preprocessing",
                                    description="Quick script to split something something dataset to suit zero shot learning")
    parser.add_argument("--split",dest='split',action='store',default=0.2,type=float)
    parser.add_argument("--labels_dir",dest='labels_dir',action='store',default='/usr/local/src/playground/action-recognition/smth-smth/labels')
    parser.add_argument("--video_dir",dest='video_dir',action='store',default='/usr/local/src/playground/action-recognition/smth-smth/20bn-something-something-v2-bis')
    args = parser.parse_args()

    original_train_label_file = os.path.join(args.labels_dir,'train.json')
    original_val_label_file = os.path.join(args.labels_dir,'validation.json')
    label_file = os.path.join(args.labels_dir,'labels.json')
    
    with open(original_train_label_file, "r") as f:
        og_train_label_json = json.load(f)

    with open(original_val_label_file, "r") as f:
        og_val_label_json = json.load(f)

    data = og_train_label_json + og_val_label_json

    with open(label_file,'r') as f:
        label_dict = json.load(f)

    label_index = np.arange(0,len(label_dict),1)
    np.random.shuffle(label_index)
    train_labels_idxs = label_index[0:int((1-args.split)*len(label_dict))]
    
    train_labels = []
    val_labels = []

    for label in label_dict:
        if int(label_dict[label]) in train_labels_idxs:
            train_labels.append(label)
        else:
            val_labels.append(label)

    train_json = []
    val_json = []

    train_video_desc = []
    val_video_desc = []

    for i,datum in enumerate(data):
        datum_label = datum['template'].replace('[','').replace(']','')
        if datum_label in train_labels:
            train_json.append(datum)
            extend_frame_desc_file(train_video_desc,datum,i,args)
        else :
            val_json.append(datum)
            extend_frame_desc_file(val_video_desc,datum,i,args)

    train_video_desc_df = pd.DataFrame(train_video_desc) 
    train_video_desc_df.to_csv('new_train.csv')

    with open('preprocessed_val.json','w') as f: 
        json.dump(val_json,f,indent="\t")

    with open('preprocessed_train.json','w') as f:
        json.dump(train_json,f,indent="\t")

    with open('preprocessed_train_labels.json','w') as f:
        json.dump(train_labels,f,indent="\t")

    with open('preprocessed_val_labels.json','w') as f:
        json.dump(val_labels,f,indent="\t")


def extend_frame_desc_file(frame_desc_dict,datum,i,args):
    video_id = datum['id']
    video_dir = os.path.join(args.video_dir,video_id)
    jpg_ids = os.listdir(video_dir)
    frame_desc_dict.extend([[datum['id'],i,k,jpg_id] for k,jpg_id in enumerate(jpg_ids)])

if __name__ == "__main__":
    main()
