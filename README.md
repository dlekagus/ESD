<div align="center">
 
#  🥤음료 용기 분리수거 쓰레기통 🚮
(demo 이미지 or gif 첨부)

대학교 캠퍼스 내 음료 용기 분리수거 환경 개선을 목표로,

Raspberry Pi 기반의 YOLOv5n 모델을 활용해 쓰레기 종류를 인식하고,

여러 센서와 액추에이터를 장착한 실구조물을 제어하여 자동 분리수거를 수행하는 시스템
</div>

## Content

## Deployment

## Commit History

[25/04/27] repository 생성

[25/05/14] fine-tuning 및 모델 정확도 보완 시도

[25/05/14] Raspberry Pi에서 서보모터 3개 동작 확인 및 문제점 해결

[25/05/18] YOLOv5n fine-tuning 및 README에 코드 추가

[25/05/18] Embedded Control Logic 초안 업로드

[25/05/25] Embedded Control Logic 테스트 버전 업로드

[25/05/28] 서보모터 구조물 하중 확인 및 보완

[25/05/30] 모델 정확도 보완을 위해 클래스 재조정 및 dataset 재구성

[25/05/31] fine-tuning 재진행으로 인한 README 코드 및 dataset 링크 수정

[25/06/01] Embedded Control Logic 수정: 재분류 조건(detect.py), 클래스 조정(main.py)

[25/06/01] system architecture 수정

## Key Features

+ fine-tuned YOLOv5n 기반 실시간 분류
+ Raspberry Pi with 서보모터(PCA9685), 초음파센서/LED(GPIO)

## Technologies Used 
** Platform **

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white)

** Software Stack**

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv5n](https://img.shields.io/badge/YOLOv5n-00FFFF?style=for-the-badge&logo=github&logoColor=black)

![Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

** Hardware Stack**

| 서보모터 (MG996R) | 서보모터 (SG-90) | 초음파센서 | LED | PCA9685 Driver | 전원공급 장치 |
|:-----------------:|:---------------:|:----------:|:---:|:--------------:|:-------------:|
| <img src="https://github.com/user-attachments/assets/e7cf65cf-3438-4a57-b9ed-a7c6066803f8" width="150"/> | <img src="https://github.com/user-attachments/assets/2f0ddf28-8226-4bd3-a1ec-503e4cea0219" width="150"/> | <img src="https://github.com/user-attachments/assets/1789c1e5-4773-4f63-998d-b287c9d67a5a" width="150"/> | <img src="" width="150"/> | <img src="https://github.com/user-attachments/assets/8c282cc2-3795-4eea-b862-2c561e002e9e" width="150"/> 



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


