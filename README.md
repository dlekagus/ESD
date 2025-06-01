<div align="center">
 
#  🥤음료 용기 분리수거 쓰레기통 🚮
(demo 이미지 or gif 첨부)

대학교 캠퍼스 내 음료 용기 분리수거 환경 개선을 목표로,

Raspberry Pi 기반의 YOLOv5n 모델을 활용해 쓰레기 종류를 인식하고,

여러 센서와 액추에이터를 장착한 실구조물을 제어하여 자동 분리수거를 수행하는 시스템
</div>

## Content

+ [Deployment](#deployment)
+ [Commit History](#commit-history)
+ [Key Features](#key-features)
+ [Technologies Used](#technologies-used)
+ [Tasks & Responsibilities](#tasks--responsibilities)
+ [How To Run](#1-how-to-run)
+ [Model Training](#2-model-training)
+ [Embedded Control Logic](#3-embedded-control-logic)
+ [Evaluation](#4-evaluation)

## Deployment

(배포 링크 첨부, 파일 tree 추가)

## Commit History

🕰 2025.04.16 ~ 2025.06.11

[25/04/27] repository 생성

[25/05/14] fine-tuning 및 모델 정확도 보완 시도

[25/05/14] Raspberry Pi에서 서보모터 3개 동작 확인 및 전력 문제 해결

[25/05/18] README 내용 추가: Model Training, Flow Chart

[25/05/18] Embedded Control Logic 초안 업로드 및 README 내용 추가

[25/05/25] Embedded Control Logic 테스트 버전 업로드 및 README 내용 추가

[25/05/28] 서보모터 구조물 하중 확인 및 보완

[25/05/30] 모델 정확도 보완을 위해 클래스 재조정 및 dataset 재구성

[25/05/31] fine-tuning 재진행으로 인한 README 코드 및 dataset 링크 수정

[25/06/01] Embedded Control Logic 수정본 업로드: 재분류 조건(detect.py), 클래스 조정(main.py)

[25/06/02] README 내용 추가: Content, Key Features, Technologies Used, Tasks & Responsibilities, How To Run, Evaluation

## Key Features

+ fine-tuned YOLOv5n 기반 실시간 쓰레기 분류
+ PCA9685 기반 서보모터 3개 제어
+ GPIO 기반 초음파센서 및 LED 제어
+ FSM을 통해 Raspberry Pi에서의 전체 동작 흐름 관리

## Technologies Used 
💻 Platform

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white)

🧠 Software Stack

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv5n](https://img.shields.io/badge/YOLOv5n-00FFFF?style=for-the-badge&logo=github&logoColor=black)

![Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-44A833?style=for-the-badge&logo=anaconda&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

🔩 Hardware Stack

| 카메라 | 서보모터 (MG996R) | 서보모터 (SG-90) | 초음파센서 | LED | PCA9685 Driver | 전원공급 장치 |
|:------:|:-----------------:|:---------------:|:----------:|:---:|:--------------:|:-------------:|
| <img src="https://github.com/user-attachments/assets/6c0492f8-ac86-4322-a9e0-25cef9a381c0" width="150"/> | <img src="https://github.com/user-attachments/assets/e7cf65cf-3438-4a57-b9ed-a7c6066803f8" width="150"/> | <img src="https://github.com/user-attachments/assets/2f0ddf28-8226-4bd3-a1ec-503e4cea0219" width="150"/> | <img src="https://github.com/user-attachments/assets/1789c1e5-4773-4f63-998d-b287c9d67a5a" width="150"/> | <img src="" width="150"/> | <img src="https://github.com/user-attachments/assets/8c282cc2-3795-4eea-b862-2c561e002e9e" width="150"/> | <img src="https://github.com/user-attachments/assets/445fee6c-6855-4cd7-b330-2357d3549239" width="150"/> 
| 쓰레기 실시간 인식 | 중앙 회전축 기준 받침대 위치 변경 (양날개) | 두 받침대 외회전 (단날개) | 분리통 꽉참 여부 확인 | 분리통 꽉참 상태 경고 표시 | 서보모터 3개 구동 | 외부 전원 공급용 |

## Tasks & Responsibilities

(개인 캐릭터 그림 추가)

| Member   | Tasks                                                                                                                  |
|----------|-------------------------------------------------------------------------------------------------------------------------|
| 이담현   | - YOLOv5n 모델 fine-tuning<br>- 라즈베리파이 추론 테스트 및 FPS 개선<br>- 모델 오류 수정<br>- Embedded Control Logic 작성 및 테스트 |
| 최현빈   | - 준비물 구성 및 확보<br>- 서보모터 하중 테스트 및 위치 보완<br>- 하드웨어 배치 최적화<br>- 자료 제작|
| 공동     | - 데이터셋 구성<br>- 구조물 제작 및 보완<br>- PCA9685 전력 안정화 구성<br>- 전체 동작 통합 테스트 및 최적화|

## 1. How To Run

🔄 Flow Chart

<img src="https://github.com/user-attachments/assets/0821dbdc-e17e-4df1-b87a-50daf8506f4d" width="250"/>

#### 1) Setup

실구조물은 2층 회전 구조로, 2층의 두 받침대는 SG-90 서보모터 2개와 각각 붙어 있고 이 두 서보모터는 MG996R 서보모터의 양 날개에 각각 부착되어 있습니다. 층층이 연결된 이 구조는 1층 분리통의 정중앙과 얇은 봉을 통해 연결되며 분류 결과에 따라 서보모터가 회전하며 낙하를 통해 쓰레기가 처리됩니다.  

📐 Wiring Diagram & Physical Structure

부품 배치는 다음과 같습니다:

(연결 회로도 사진)

<img src="https://github.com/user-attachments/assets/fde17e5d-96df-4e12-b131-bf441ab5554c" width="350"/>

🔌 5V Power Supply

Raspberry Pi에서 2개 이상의 서보모터를 동시 구동할 경우 shutdown이 발생하기에 5V 외부 전원 공급이 반드시 필요합니다. 

(연결 사진)

+ PCA9685 V+ 단자에 5V 어댑터 연결
+ GND는 Raspberry Pi와 공통으로 연결

#### 2) Requirements

📥 Download [Deployment](#deployment) Packages and Unzip it 

#### 3) Run Command

⌨ Run the following commands in Command Prompt:

```bash
source ESD/bin/activate           # change 'ESD' into your own conda virtual environment name
pip install -r requirements.txt
python main.py
```

#### ⚠️ Know Issues

| 이슈                        | 원인 및 해결 방안                                     |
| ------------------------- | ---------------------------------------------- |
| 서보모터가 멈추거나 라즈베리파이가 꺼짐 | PCA9685에 5V 안정 전원 공급 필수|
| 카메라 인식 안 됨             | 안정적인 작동을 위해 PiCamera 대신 USB 웹캠 사용 권장 |
| 초음파 센서/LED 미작동       | GND 공통 연결 여부 확인, GPIO 핀 번호 확인|

## 2. Model Training

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

## 3. Embedded Control Logic

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

+ 분류 클래스: can, plastic, re(demo용 구조물에서는 To be Sorted로 표기), paper


#### 3) Hardware Control Logic

🗂️ 서보모터, 초음파센서, 그리고 LED 센서 제어는 *control.py*에서 수행합니다. 

+ Servo

PCA9685 기반으로 SG-90 모델 ２개와 MG996R 모델 １개에 대한 회전 제어

+ Ultrasonic and LED

GPIO 기반으로 demo용으로서 wastes 클래스에 대해서만 동작 확인


## 4. Evaluation

본 프로젝트의 성능 평가는 다음과 같은 정량적, 정성적 지표를 기준으로 진행되었습니다. 

| 항목                          | 설명                                          |
| --------------------------- | ------------------------------------------- |
|FPS| Raspberry Pi에서 실시간 추론 속도 측정 (10 이상된 거 캡처본) |
| Precision / Recall      | YOLOv5n 분류 정확도 평가 (계산 값, curve, accuracy)          |
| Confusion Matrix      | 클래스 간 오분류 양상 (시각화)                            |
|System Stability        | 실사용 편의성, 낙하 안정성 |

💡 Encountered Difficulties & Solutions

(개선 후 사진과 함께 solution 추가)

+ 모델 인식 오류

+ 서보모터 전력 부족

+ 서보모터 하중 한계

+ 실구조물 구조적 문제

