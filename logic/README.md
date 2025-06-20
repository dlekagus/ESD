본 임베디드 시스템은 FSM(Finite State Machine)을 기반으로 각 기능을 단계적으로 제어합니다. 

: YOLOv5n으로 추론 및 분류 -> 받침대 회전

#### 🗂️ 파일 구성

+ *detect.py* : 모델 로딩 및 분류 로직을 포함한 추론
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

<img src="https://github.com/user-attachments/assets/1d893be2-3b5b-410a-bf5b-e0ec1fc6386f" width="600"/>

#### 2) Classification Logic

🗂️ 추론과 동시에 분류가 이루어지도록, 해당 로직을 *detect.py*에 추가합니다. 

+ ultralytics yolov5n이 제공하는 detect.py를 참고하여 커스텀 *detect.py* 새로 작성 (경량화 및 분류 로직 추가)

+ 분류 클래스: re, can, plastic, paper


#### 3) Hardware Control Logic

🗂️ 서보모터 제어는 *control.py*에서 수행합니다. 

+ Servo

PCA9685 기반으로 SG-90 모델 ２개와 MG996R 모델 １개에 대한 회전 제어
