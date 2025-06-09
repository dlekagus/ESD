<div align="center">
 
#  🥤음료 용기 분리수거 쓰레기통 🚮
### (Automated Beverage Container Recycling Bin)
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

(배포 링크 첨부 or 별도 폴더 추가, 파일 tree 추가)

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

[25/06/02] logic 폴더 생성 및 해당 파일 및 README 내용 이동: Embedded Control Logic(main.py, detect.py, control.py)

[25/06/02] control.py 코드 수정: GPIO pin 번호 변경

[25/06/03] 구조물 문제점 해결 및 시스템 통합 진행

[25/06/04] 구조물 보완 및 SG-90 서보모터 최종 동작 확인

[25/06/04] README 내용 추가: How To Run > Hardware Setup

[25/06/05] MG996R 서보모터 로직 보완 및 최종 동작 확인

[25/06/05] main.py, detect.py, control.py 수정

[25/06/09] Raspberry Pi fine-tuned YOLOv5n 추론 및 서보모터 로직 연결 확인, 로직 최적화 진행

[25/06/10] main.py, detect.py, FSM 수정 및 logic 폴더 README 내용 추가: 각 .py 파일에 대한 로직 설명


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

MG996R의 경우 180과 360으로 두 가지 버전이 있으며 360도 회전을 위해서는 반드시 360 버전이 있어야 합니다. 

| 카메라 | 서보모터<br>(MG996R-360 ver.) | 서보모터<br>(SG-90) | 초음파센서<br>(HC-SR04) | LED | PCA9685 Driver | 전원공급 장치 |
|:------:|:-----------------:|:---------------:|:----------:|:---:|:--------------:|:-------------:|
| <img src="https://github.com/user-attachments/assets/6c0492f8-ac86-4322-a9e0-25cef9a381c0" width="200"/> | <img src="https://github.com/user-attachments/assets/e7cf65cf-3438-4a57-b9ed-a7c6066803f8" width="200"/> | <img src="https://github.com/user-attachments/assets/2f0ddf28-8226-4bd3-a1ec-503e4cea0219" width="200"/> | <img src="https://github.com/user-attachments/assets/1789c1e5-4773-4f63-998d-b287c9d67a5a" width="200"/> | <img src="https://github.com/user-attachments/assets/c1274c5f-55c1-423f-a773-0f0524bffcc0" width="200"/> | <img src="https://github.com/user-attachments/assets/8c282cc2-3795-4eea-b862-2c561e002e9e" width="200"/> | <img src="https://github.com/user-attachments/assets/445fee6c-6855-4cd7-b330-2357d3549239" width="200"/> 
| 쓰레기<br>실시간 인식 | 중앙 회전축 기준<br>받침대 위치 변경 (양날개) | 두 받침대<br>외회전 (단날개) | 분리통 꽉참<br>여부 확인 | 분리통 꽉참 상태 경고 표시 | 서보모터 3개 구동 | 외부 전원 공급 |

## Tasks & Responsibilities

(개인 그림 추가)

| Member   | Tasks                                                                                                                  |
|----------|-------------------------------------------------------------------------------------------------------------------------|
| 이담현   | - YOLOv5n 모델 fine-tuning<br>- Raspberry Pi 추론<br>- Embedded Control Logic 작성 및 최적화<br>- 회로 구성 및 전력 안정화 |
| 최현빈   | - 준비물 구성 및 확보<br>- 서보모터 하중 테스트 및 위치 보완<br>- 구조물 문제점 해결 |
| 공동     | - 구조물 제작<br>- 하드웨어 배치 최적화<br>- 전체 동작 통합 테스트<br>- 자료 제작|

## 1. How To Run

🔄 Flow Chart

<img src="https://github.com/user-attachments/assets/0821dbdc-e17e-4df1-b87a-50daf8506f4d" width="250"/>

#### 1) Hardware Setup

실구조물은 2층 회전 구조로, 2층의 두 받침대는 SG-90 서보모터 2개와 각각 붙어 있고 이 두 서보모터는 MG996R 서보모터의 양 날개에 각각 부착되어 있습니다. 층층이 연결된 이 구조는 1층 분리통의 정중앙과 얇은 봉을 통해 연결되며 분류 결과에 따라 서보모터가 회전하며 낙하를 통해 쓰레기가 처리됩니다.  

📐 Wiring Diagram & Physical Structure

부품 배치는 다음과 같습니다:

<img src="https://github.com/user-attachments/assets/fe846f67-e28e-493c-8093-01bc09df8e64" width="500"/>

<img src="https://github.com/user-attachments/assets/9f11cb5b-f2db-4b79-bf2c-a8b5d695d7c6" width="500"/>

+ 회로 배치 Checklist

  ✔ PCA9685 배선 시, Embedded Control Logic과 일치하는 채널 번호로 연결
  
  ✔ BCM 번호로 GPIO 센서 연결 (초음파센서와 LED는 5V 출력 사용)
  
  ✔ 외부 전원 공급 방안 마련
  
  ✔ GND는 모두 Raspberry Pi의 GND와 공통 연결
+ 구조물 제작 Checklist
  ✔ 받침대의 외회전 반경을 고려하여 적절한 크기 설정 (1층 분리통의 절반 정도)
  
  ✔ 받침대 크기에 맞춰 2층 가이드 벽 크기 설정
  
  ✔ 받침대와 가이드 벽 간의 빈 공간 보완 (하중 부담을 높이지 않는 재료로 사선의 받침틀 추가)
  
  ✔ 받침틀은 외회전 반경 고려하여 기울임 설정
  

🔌 5V Power Supply

Raspberry Pi에서 서보모터 2개 이상을 동시에 구동하면 전력 부족으로 shutdown 될 수 있으므로, 외부 5V (최소 3A 필요) 전원 공급이 필수입니다. 이를 위해 PCA9685 driver를 사용해 서보모터에 안정적으로 전원을 공급합니다. PCA9685 screw 터미널(V+)에 전원 장치를 연결하여 공급할 수 있습니다. 

전원 공급 방식은 상황에 맞게 선택 가능합니다: 

| 방법 | 설명 | 권장 조건|
|------|------|----------|
|**Our Approach**:<br>5V 3A USB 어댑터 + USB 케이블 | USB 케이블을 잘라 피복을 벗긴 후 점퍼선(female)에 연결해 절연 테이프로 고정 | 저렴하고 간단<br>but 접촉 불안정 |
| 5V 3A USB 어댑터<br>+ DC to USB 케이블<br>+ barrel to screw | screw와 screw끼리 전선 연결 | 안정성<br>but 가장 고비용 |
| USB 보조배터리 | USB 케이블을 잘라 피복을 벗긴 후 점퍼선(female)에 연결해 절연 테이프로 고정 | 이동성<br>but 낮은 최대 전류 |
| 리튬이온 배터리팩 | screw에 전선 연결 | 이동성<br>but 충전 및 보호회로 필요 |
| 가변 정전압 모듈 | 원하는 전압 설정 | 미세 조절 가능<br>but 복잡 |


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
| 서보모터가 멈추거나 라즈베리파이가 꺼짐 | PCA9685에 5V 안정 전원 공급 필수, GND 공통 연결 여부 확인|
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

🔍 fine-tuning result

<img src="https://github.com/user-attachments/assets/a7bbf72b-877e-4a4c-9c4e-5e418433b563" width="600"/>

``` python
# Download best.pt for inference
from google.colab import files
files.download('/content/drive/MyDrive/yolov5_runs/4cls_328img/weights/best.pt')
```

## 3. Embedded Control Logic

자세한 내용은 *logic* 폴더에서 확인할 수 있습니다. 

## 4. Evaluation

본 프로젝트의 성능 평가는 다음과 같은 정량적, 정성적 지표를 기준으로 진행되었습니다. 

| 항목                          | 설명                                          |
| --------------------------- | ------------------------------------------- |
|FPS (yolo vs system)| Raspberry Pi에서 실시간 추론 속도 측정 |
| Precision / Recall (yolo vs system)   | 분류 및 서보모터 제어 정확도 평가 (계산 값, curve, accuracy) |
| Confusion Matrix      | 클래스 간 오분류 양상 (시각화)                            |
|System Stability        | 실사용 편의성, 낙하 안정성 |

📉 Validation for fine-tuned YOLOv5n (on Colab)
```bash
!python val.py --weights /content/drive/MyDrive/yolov5_runs/4cls_328img/weights/best.pt --data /content/drive/MyDrive/ESD/dataset/data.yaml --img 160
```

💡 Encountered Difficulties & Solutions

(개선 후 사진과 함께 solution 추가)

+ 모델 인식 오류

+ 서보모터 전력 부족

+ 서보모터 하중 한계

+ 실구조물 구조적 문제

+ 서보모터 360도 회전 동작 로직 구성

+ USB 웹캠 warmup 속도

🏳 Limitation

