import torch
import numpy as np
from pathlib import Path
from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import (non_max_suppression, scale_boxes, check_img_size)
from utils.torch_utils import select_device
from ultralytics.utils.plotting import Annotator, colors


def load_model(weights='best.pt', imgsz=(160, 160), device=''):
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=False, data=None, fp16=False)
    stride = model.stride
    imgsz = check_img_size(imgsz, s=stride)  # ensure divisible
    return model, imgsz, device


def run(model, frame, imgsz=(160, 160), conf_thres=0.3, iou_thres=0.45, classes=None, return_res=False):
    names = model.names
    device = model.device
    stride = model.stride

    im = letterbox(frame, imgsz, stride=stride, auto=False)[0]
    im = im[:, :, ::-1].transpose(2, 0, 1)
    im = np.ascontiguousarray(im)
    im = torch.from_numpy(im).to(device).float() / 255.0
    if len(im.shape) == 3:
        im = im[None]

    pred = model(im)
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes)

    detected_class = []
    all_detections = []
    im0 = frame.copy()

    for det in pred:
        if len(det):
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls in det:
                label = names[int(cls)]
                detected_class.append(label)
                all_detections.append((label, float(conf), xyxy))

    if not detected_class:
        return "unknown", im0, 0.0

    is_re = 're' in detected_class
    top_label = 're' if is_re else detected_class[0]

    if return_res and all_detections:
        annotator = Annotator(im0, line_width=2, example=str(names))
        if is_re:
            for label, conf, xyxy in all_detections:
                color_idx = list(names.values()).index(label)
                annotator.box_label(xyxy, f"{label} {conf:.2f}", color=colors(color_idx, True))
            im0 = annotator.result()
            return 're', im0, 0.0
        else:
            best = max(all_detections, key=lambda x: x[1])
            color_idx = list(names.values()).index(best[0])
            annotator.box_label(best[2], f"{best[0]} {best[1]:.2f}", color=colors(color_idx, True))
            top_conf = max([c[1] for c in all_detections])
            im0 = annotator.result()
            return top_label, im0, top_conf



