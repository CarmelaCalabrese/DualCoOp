python train_openvclip_zsl.py --config_file configs/models/rn50_ep50.yaml --openvclip_cfg /DualCoOp/OpenVCLIP/configs/Kinetics/TemporalCLIP_vitb16_8x16_STAdapter.yaml --datadir /DualCoOp/datasets/ssv2 --dataset_config_file configs/datasets/ssv2.yaml --input_size 224  --n_ctx_pos 64 --n_ctx_neg 64 