from detect import load_model, run
from control import (
    rotate_bin,
    return_bin,
    rotate_tray
)
import cv2
import time

# Define states
STATE_IDLE = "IDLE"
STATE_CLASS = "CLASS"
STATE_SERVO = "SERVO"

INFERENCE_INTERVAL = 3

WINDOW = False

# ROI
ROI_X1, ROI_X2 = 5, 395
ROI_Y1, ROI_Y2 = 80, 480

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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
while True:
    test_ret, test_frame = cap.read()
    if test_ret:
        print("[READY] 카메라 준비 완료")
        break
    time.sleep(0.1)
input("Enter를 누르면 동작을 시작합니다.\n")

model, imgsz, device = load_model(weights="best.pt", imgsz=(160, 160), device="")

try:
    done = False    # just for demo
    start_total = time.time()   # elapsed time

    while not done:
        # Control FSM
        if state == STATE_IDLE:
            state = STATE_CLASS

        elif state == STATE_CLASS:
            frames = []
            start_time = time.time()
            print("[STATE] 3초간 프레임 수집 중...")

            while (time.time() - start_time) < 3.0:
                ret, frame = cap.read()
                if ret:
                    roi = frame[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]
                    frames.append(roi)

                    if WINDOW:
                        vis_frame = frame.copy()
                        cv2.rectangle(vis_frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 0, 255), 2)
                        cv2.imshow("Live Capture", vis_frame)
                        if cv2.waitKey(1) == ord("q"):
                            break

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

                frame_with_box = frame.copy()
                cv2.rectangle(vis_frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 0, 255), 2)
                cv2.putText(frame_with_box, f"{detected_label} ({top_conf:.2f})", (ROI_X1, ROI_Y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                cv2.imwrite("result8.jpg", frame_with_box)

                avg_yolo_fps = sum(fps_list) / len(fps_list) if fps_list else 0
                print(f"[yolo FPS] {avg_yolo_fps: .1f}")

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
            
            print(f"[SERVO] 서보모터 회전 완료")
            done = True
            state = STATE_IDLE

except KeyboardInterrupt:
    pass
finally:
    cv2.destroyAllWindows()
    # system fps
    end_total = time.time()
    elapsed_time = end_total - start_total
    print(f"[Elapsed Time] 분류 1회 처리에 걸린 시간: {elapsed_time:.2f}초")

