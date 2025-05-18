from detect import run
from control import (
    check_full,
    notification,
    cleanup,
)
import cv2
import time

# Define parameter
STATE_IDLE = "IDLE"
STATE_CLASS = "CLASS"
STATE_SERVO = "SERVO"
STATE_FULL = "FULL"
STATE_LED = "LED"
FULL_THRES = 4
INFERENCE_INTERVAL = 3

# initialization
state = STATE_IDLE
drop = {'can': 0, 'plastic': 0, 're': 0, 'wastes': 0}
detected_label = "unknown"
frame_cnt = 0
last_res = ("unknown", 0.0, None)
full = set()

try:
    while True:
        frame_cnt += 1
        # demo: Real-time streaming just for checking(not required for actual commercialization) 
        _, _, frame = last_res
        if frame is not None:
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) == ord("q"):
                break
        
        # Control FSM
        if state == STATE_IDLE:
            if frame_cnt % INFERENCE_INTERVAL == 0:
                state = STATE_CLASS
        elif state == STATE_CLASS:
            label, conf, frame = run(
                weights = "best.pt",
                imgsz = (160, 160),
                source = 0,
                return_res = True
            )
            last_res = (label, conf, frame)

            if label != "unknown":
                if label in full:
                    print(f"[FULL] {label} 통이 이미 가득 찼습니다.")
                    state = STATE_LED
                else: 
                    print(f"[detected] {label} ({conf: .2f})")
                    drop[label] += 1
                    detected_label = label
                    state = STATE_SERVO
            else:
                state = STATE_IDLE
        elif state == STATE_SERVO:

        # demo: Check FULL only for wastes class due to one ultrasonic sensor and one LED
        elif state == STATE_FULL:
            if detected_label == "wastes" and check_full():
                full.add(detected_label)
                state = STATE_LED
            else:
                drop[detected_label] = 0
                state = STATE_IDLE
        elif state == STATE_LED:
            notification()
            state = STATE_IDLE
except KeyboardInterrupt:
    pass
finally:
    cv2.destroyAllWindows()
    cleanup()
