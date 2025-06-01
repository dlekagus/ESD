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
