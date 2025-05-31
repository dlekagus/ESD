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

[25/05/18] Embedded Control Logic 초안 업로드

[25/05/25] Embedded Control Logic 테스트 버전 업로드

## 1. System Architecture

본 시스템은 Fine-Tuned YOLOv5n 분류 모델과 Raspberry Pi 기반 하드웨어 제어 로직을 통합하여, 
자동 분리수거 기능을 수행하는 임베디드 시스템입니다. 

<img src="https://github.com/user-attachments/assets/0821dbdc-e17e-4df1-b87a-50daf8506f4d" width="250"/>

## 2. Model Training
 
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
    │   │   │   ├── wastes01.jpg
    │   │   │   ├── plastic01.jpg
    │   │   │   └── ...
    │   │   ├── labels/
    │   │   │   ├── wastes01.txt
    │   │   │   ├── plastic01.txt
    │   │   │   └── ...
    │   ├── valid/                # same structure as train/
    │   ├── test/                 # same structure as train/
    │   ├── data.yaml             # path configuration required depending on your environment
    │   └── README.txt
    ├── fine_tuning_yolo.ipynb    # create a new .ipynb file to write the fine-tuning code
├── yolov5_runs/
    │   ├── 4cls_360img/
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
names: ['can', 'plastic', 're', 'wastes']
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
(경량화 및 라즈베리파이 환경 적용 과정)

(best.pt 추론 방식 및 detect.py 실행 예시)

## 4. Embedded Control Logic

본 임베디드 시스템은 FSM(Finite State Machine)을 기반으로 각 기능을 단계적으로 제어합니다. 

: YOLOv5n으로 추론 및 분류 -> 분리수거통 및 받침대 회전 -> 초음파 센서로 FULL 여부 확인 -> LED 알림

#### 🗂️ 파일 구성

+ *detect.py* : 분류 함수 추가
+ *control.py* : 하드웨어 제어 
+ *main.py* : FSM 흐름 제어 

``` text
yolov5/
├── best.pt
├── detect.py
├── control.py
├── main.py
└── ...
```

#### 1) FSM

🗂️ FSM의 전체 state 제어는 *detect.py*와 *control.py*에서 함수를 호출하여 *main.py*에서 수행합니다.

<img src="https://github.com/user-attachments/assets/d066eb08-1c9e-4d71-ae1a-f7c466aaaa13" width="600"/>

#### 2) Classification Logic

🗂️ 추론과 동시에 분류가 이루어지도록, 해당 함수를 *detect.py*에 추가합니다. 

+ ultralytics yolov5n의 *detect.py* 내 run() 함수 수정하여 작성

+ 분류 클래스: can, plastic, re(demo용 구조물에서는 To be Sorted로 표기), wastes


#### 3) Hardware Control Logic

🗂️ 서보모터, 초음파센서, 그리고 LED 센서 제어는 *control.py*에서 수행합니다. 

+ Servo

PCA9685 기반으로 SG-90 모델 ２개와 MG996R 모델 １개에 대한 회전 제어

+ Ultrasonic and LED

GPIO 기반으로 demo용으로서 wastes 클래스에 대해서만 동작 확인


## 5. Evaluation


