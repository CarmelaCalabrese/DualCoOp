import os
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
from models import build_model
from utils.validations import validate_zsl
from opts import arg_parser
from dataloaders import build_dataset
from utils.build_cfg import setup_cfg
from torch.cuda.amp import autocast
from randaugment import RandAugment
from dataloaders.helper import CutoutPIL

from PIL import Image


import json
 
# # Opening JSON file
# with open("./datasets/mscoco_2014/annotations/instances_val2014_gzsi_48_17.json", "r") as f:
#     data = json.load(f)

# print(data['images'])

# data['images'] = []
# data['images'].append({'license': 6, 'file_name': 'prova.jpg', 'coco_url': 'http://images.cocodataset.org/val2014/COCO_val2014_000000029253.jpg', 'height': 513, 'width': 640, 'date_captured': '2013-11-17 10:30:30',  'id': 0})
# data['annotations'] = []
# data['annotations'].append({'segmentation': [[]], 'area': 0, 'iscrowd': 0, 'image_id': 0, 'bbox': [], 'category_id': 1, 'id': 0})
# data['categories'] = []
# data['categories'].append({'supercategory': 'animal', 'id': 0, 'name': 'elephant'}) 

# f.close()

# with open("./datasets/mscoco_2014/annotations/instances_val2014_gzsi_48_17.json", "w") as f:
#     json.dump(data, f)
# Closing file


def main():
    global args
    parser = arg_parser()
    args = parser.parse_args()
    cfg = setup_cfg(args)

    test_split = cfg.DATASET.TEST_SPLIT
    # print('test_split')
    # print(test_split)
    test_gzsl_dataset = build_dataset(cfg, test_split, cfg.DATASET.ZS_TEST)
    # print('test_gzsl_dataset')
    # print(test_gzsl_dataset)
    test_gzsl_cls_id = test_gzsl_dataset.cls_id
    # print('test_gzsl_cls_id')
    # print(test_gzsl_cls_id)
    # test_gzsl_split =  cfg.DATASET.TEST_GZSL_SPLIT
    # print('test_gzsl_split')
    # print(test_gzsl_split)
    # test_gzsl_loader = torch.utils.data.DataLoader(test_gzsl_dataset, batch_size=cfg.DATALOADER.TEST.BATCH_SIZE,
    #                                                shuffle=cfg.DATALOADER.TEST.SHUFFLE,
    #                                                num_workers=cfg.DATALOADER.NUM_WORKERS, pin_memory=True)
    # print('test_gzsl_loader')
    # print(test_gzsl_loader)

    image = args.single_image

    classnames = test_gzsl_dataset.classnames
    # classnames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
    #                 'elephant', 'bear', 'zebra', 'giraffe', 'house', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 
    #                 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 
    #                 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 
    #                 'teddy bear', 'hair drier', 'toothbrush']
    #print(classnames)

    model, arch_name = build_model(cfg, args, classnames)

    model.eval()

    if args.pretrained is not None and os.path.exists(args.pretrained):
        print('... loading pretrained weights from %s' % args.pretrained)
        checkpoint = torch.load(args.pretrained, map_location='cpu')
        state_dict = checkpoint['state_dict']
        epoch = checkpoint['epoch']
        model.load_state_dict(state_dict)
        print('Epoch: %d' % epoch)
    else:
        raise ValueError('args.pretrained is missing or its path does not exist')

    img_size=224
    train_transform = transforms.Compose([
            # transforms.RandomResizedCrop(img_size)
            transforms.Resize((img_size, img_size)),
            CutoutPIL(cutout_factor=0.5),
            RandAugment(),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
        ])
    test_transform = transforms.Compose([
            # transforms.CenterCrop(img_size),
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
        ])


    print('Evaluate with threshold %.2f' % args.thre)

    Softmax = torch.nn.Softmax(dim=1)
    Sig = torch.nn.Sigmoid()

    # switch to evaluate mode
    #model.eval()

    img = Image.open(image).convert('RGB')
    img = test_transform(img)

    preds = []
    targets = []
    output_idxs = []
    with torch.no_grad():

        #target = target.max(dim=1)[0]
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
        img = img.to(device)

        # compute output
        with autocast():
           output = model(img.unsqueeze(0), test_gzsl_cls_id)
        #target = target[:, cls_id]
        if output.dim() == 3:
            output = Softmax(output).cpu()[:, 1]
        else:
            output = Sig(output).cpu()

        # output, target = filter_samples(output, target, cls_id)
        # for mAP calculation
        preds.append(output.cpu())
        #targets.append(target.cpu())
        output_idx = output.argsort(dim=-1, descending=True)
        output_idxs.append(output_idx)

    #print('output_idxs')
    #print(output_idxs)
    idxs=torch.cat(output_idxs, dim=0).cpu().numpy()
    idxs=idxs[0][:5] 

    print('Outcome preds:')
    print(preds)
    print('Outcome output_idx:')
    print(idxs)
    print('Outcome output_lab:')
    print([classnames[val] for val in idxs])
    torch.cuda.empty_cache()



if __name__ == '__main__':
    main()