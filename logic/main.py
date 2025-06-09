from detect import load_model, run
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
import os

# Define states
STATE_IDLE = "IDLE"
STATE_CLASS = "CLASS"
STATE_SERVO = "SERVO"
STATE_FULL = "FULL"
STATE_LED = "LED"

FULL_THRES = 4
INFERENCE_INTERVAL = 3

WINDOW = True # to improve fps

# initialization
state = STATE_IDLE
drop = {'re': 0, 'can': 0, 'plastic': 0, 'paper': 0}
detected_label = "unknown"
full = set()
fps_list=[]
trash_cnt = 0

# warmup camera
print("[CAM] 카메라 워밍업 중...")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 160)
while True:
    test_ret, test_frame = cap.read()
    if test_ret:
        print("[READY] 카메라 준비 완료")
        break
    time.sleep(0.1)
input("Enter를 누르면 동작을 시작합니다.\n")

model, imgsz, device = load_model(weights="best.pt", imgsz=(160, 160), device="")

try:
    while trash_cnt < 3:    # just for demo (real: infinite loop)
        # system FPS
        sys_frame_cnt = 0
        sys_start = time.time()
        sys_frame_cnt += 1
     
        # Control FSM
        if state == STATE_IDLE:
            trash_cnt += 1
            state = STATE_CLASS

        elif state == STATE_CLASS:
            frames = []
            start_time = time.time()
            print("[STATE] 3초간 프레임 수집 중...")

            while (time.time() - start_time) < 3.0:
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
                    if WINDOW:
                        cv2.imshow("Live Capture", frame)
                        if cv2.waitKey(1) == ord("q"):
                            break
            cap.release()

            # inference per every 3 frames
            results = []
            fps_list.clear()
            for idx, frame in enumerate(frames):
                if idx % INFERENCE_INTERVAL != 0:
                    continue

                yolo_start = time.time()
                label, out_frame, conf = run(model, frame, imgsz=imgsz, return_res=True)
                yolo_end = time.time()

                fps_list.append(1/ (yolo_end - yolo_start))

                if label and label != "unknown" and conf is not None:
                    results.append((label, conf, out_frame))

            if not results:
                print("[CLASS] 감지 실패")
                state = STATE_IDLE
            else:
                top_result = max(results, key=lambda x: x[1])  # choose max confidence 
                detected_label, top_conf, top_frame = top_result

                cv2.imwrite("result.jpg", top_frame)
                os.system("xdg-open result.jpg")

                avg_yolo_fps = sum(fps_list) / len(fps_list) if fps_list else 0
                print(f"[yolo FPS] {avg_yolo_fps: .1f}")

                if detected_label in full:
                    print(f"[FULL] {detected_label} 통이 이미 가득 찼습니다.")
                    state = STATE_LED
                else:
                    print(f"[detected] {detected_label} ({top_conf:.2f})")
                    drop[detected_label] += 1
                    state = STATE_SERVO

        elif state == STATE_SERVO:
            if detected_label != 're':  # 're' (To be Sorted) is the origin for rotation thus doesn't require rotation
                rotate_bin(detected_label)
                time.sleep(0.5)
                rotate_tray()
                time.sleep(1)
                return_bin(detected_label)
            else:
                rotate_tray()

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
        
        total_sys_time = time.time() - sys_start
        sys_fps = sys_frame_cnt / total_sys_time if total_sys_time > 0 else 0
        print(f"[System FPS] {sys_fps: .1f}")
except KeyboardInterrupt:
    pass
finally:
    cv2.destroyAllWindows()
    cleanup()

