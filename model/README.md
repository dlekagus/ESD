새로운 분류 모델을 원할 경우, 아래의 절차를 따라 다시 fine-tuning하면 됩니다. 
 
#### 1) Dataset Preparation

dataset은 직접 촬영 후 Roboflow에서 라벨링하여 확보했고, 해당 링크를 통해 YOLOv5 PyTorch 형식으로 다운로드 받아 아래와 같이 폴더 구성을 맞추어 바로 학습에 사용할 수 있습니다.

+ Download the dataset

<https://app.roboflow.com/esd-owahw/drink-container-waste/1>
``` text
MyDrive/
├── ESD/
    ├── dataset/
    │   ├── train/
    │   │   ├── images/
    │   │   │   ├── can01.jpg
    │   │   │   ├── plastic01.jpg
    │   │   │   └── ...
    │   │   ├── labels/
    │   │   │   ├── can01.txt
    │   │   │   ├── plastic01.txt
    │   │   │   └── ...
    │   ├── valid/                # same structure as train/
    │   ├── test/                 # same structure as train/
    │   ├── data.yaml             # path configuration required depending on your environment
    │   └── README.txt
    ├── fine_tuning_yolo.ipynb    # create a new .ipynb file to write the fine-tuning code
├── yolov5_runs/
    │   ├── 4cls_328img/
    │   │   ├── weights/
    │   │   │   ├── best.pt
    │   │   │   └── ...
    │   │   └── ...
└── ...
```

+ Edit *data.yaml* for Path Configuration

``` yaml
train: /content/drive/MyDrive/ESD/dataset/train
val: /content/drive/MyDrive/ESD/dataset/valid
test: /content/drive/MyDrive/ESD/dataset/test

nc: 4
names: ['can', 'paper', 'plastic', 're']
```
#### 2) Fine-Tuning on Colab

본 모델은 Google Colab T4 GPU 환경에서 YOLOv5n을 사용하여 fine-tuning 하였습니다.

``` bash
# Install YOLOv5n
!git clone https://github.com/ultralytics/yolov5
%cd yolov5
!pip install -r requirements.txt
!wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt

# train
!python train.py \
  --img 160 \
  --batch 16 \
  --epochs 50 \
  --data /content/drive/MyDrive/ESD/dataset/data.yaml \
  --weights yolov5n.pt \
  --name 4cls_328img \
  --project /content/drive/MyDrive/yolov5_runs \
  --cache
```
``` python
# Download best.pt for inference
from google.colab import files
files.download('/content/drive/MyDrive/yolov5_runs/4cls_328img/weights/best.pt')
```
