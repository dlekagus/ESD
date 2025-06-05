from detect import run
from control import (
    rotate_bin,
    return_bin,
    rotate_tray,
    check_full,
    notification,
    cleanup,
)
import cv2
import time

# Define states
STATE_IDLE = "IDLE"
STATE_CLASS = "CLASS"
STATE_SERVO = "SERVO"
STATE_FULL = "FULL"
STATE_LED = "LED"

FULL_THRES = 4
INFERENCE_INTERVAL = 3

# initialization
state = STATE_IDLE
drop = {'re': 0, 'can': 0, 'plastic': 0, 'paper': 0}
detected_label = "unknown"
frame_cnt = 0
sys_frame_cnt = 0
last_res = ("unknown", None, 0.0, 0.00)
last_yolo_fps = 0.0
full = set()

# system FPS
sys_start = time.time()
yolo_total_time = 0.0
yolo_infer_cnt = 0

try:
    while True:
        frame_cnt += 1
        sys_frame_cnt += 1

        # demo: Real-time streaming just for checking(not required for actual commercialization) 
        _, frame, _, _ = last_res
        if frame is not None:
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) == ord("q"):
                break
        
        # Control FSM
        if state == STATE_IDLE:
            if frame_cnt % INFERENCE_INTERVAL == 0:
                state = STATE_CLASS

        elif state == STATE_CLASS:
            yolo_start = time.time()
            label, frame, yolo_fps, conf = run(
                weights = "best.pt",
                imgsz = (160, 160),
                source = 0,
                return_res = True
            )
            yolo_end = time.time()
            yolo_infer_cnt += 1
            yolo_total_time += (yolo_end - yolo_start)

            last_res = (label, frame, yolo_fps, conf)
            last_yolo_fps = yolo_fps

            if not label or label == "unknown":
                print("[CLASS] 감지 실패")
                state = STATE_IDLE
            else: 
                if label in full:
                    print(f"[FULL] {label} 통이 이미 가득 찼습니다.")
                    state = STATE_LED
                else: 
                    print(f"[detected] {label} ({conf: .2f})")
                    drop[label] += 1
                    detected_label = label
                    state = STATE_SERVO

        elif state == STATE_SERVO:
            if detected_label != 're':  # 're' (To be Sorted) is the origin for rotation thus doesn't require rotation
                rotate_bin(detected_label)
                time.sleep(0.5)
                rotate_tray()
                time.sleep(1)
                return_bin(detected_label)

            if drop[detected_label] >= FULL_THRES:
                state = STATE_FULL
            else:
                state = STATE_IDLE

        # demo: Check FULL only for 'plastic' class due to one ultrasonic sensor and one LED
        elif state == STATE_FULL:
            if detected_label == "plastic" and check_full():
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
    total_sys_time = time.time() - sys_start
    sys_fps = sys_frame_cnt / total_sys_time if total_sys_time > 0 else 0
    avg_yolo_fps = yolo_infer_cnt / yolo_total_time if yolo_total_time > 0 else 0
    
    print(f"[YOLO average FPS] {avg_yolo_fps: .1f}, [System FPS] {sys_fps: .1f}")
    cv2.destroyAllWindows()
    cleanup()



