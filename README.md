# 음료 용기 분리수거 쓰레기통 
(demo 이미지 or gif 첨부)

대학교 캠퍼스 내 음료 용기 분리수거 환경 개선을 목표로,
Raspberry Pi 기반의 YOLOv5n 모델을 활용해 쓰레기 종류를 인식하고,
여러 센서와 액추에이터를 장착한 실구조물을 제어하여 자동 분리수거를 수행하는 시스템

## Technologies Used
+ YOLOv5n (fine-tuned)
+ Raspberry Pi with 서보모터, 초음파센서, LED

## Commit History
[25/04/27] repository 생성  
[25/05/18] README에 학습(fine-tuning) 코드 추가


## 1. System Design

## 2. Training (Fine-tuning)
colab T4 GPU 환경에서 실행
+ 폴더 구조
``` text
MyDrive/
└── ESD/
    ├── dataset/
    │   ├── train/
    │   │   ├── images/
    │   │   │   ├── wastes01.jpg
    │   │   │   ├── plastic01.jpg
    │   │   │   └── ...
    │   │   ├── labels/
    │   │   │   ├── wastes01.txt
    │   │   │   ├── plastic01.txt
    │   │   │   └── ...
    │   ├── valid/    # same structure as train/
    │   ├── test/     # same structure as train/
    │   ├── data.yaml
    │   └── README.txt
    ├── fine_tuning_yolo.ipynb    # create a new .ipynb file to write the fine-tuning code
```
+ .ipynb파일에서 fine-tuning code 실행
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
  --name 4cls_360img \
  --project /content/drive/MyDrive/yolov5_runs \
  --cache
```
``` python
# Download best.pt for inference
from google.colab import files
files.download('/content/drive/MyDrive/yolov5_runs/4cls_360img/weights/best.pt')
```

## 3. Inference

## 4. How To Run

## 5. Evaluation

## 6. 

