import torch
import cv2
from time import time

class Yolo5Detection:
    def __init__(self, yolo_path: str, model_path: str, conf: float=0.25, iou: float=0.45):
        if yolo_path:
            self.model = torch.hub.load(yolo_path, 'custom', path=model_path, source='local')
        else:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.model.conf = conf 
        self.model.iou = iou  
        
    def detect(self, BRG_image):
        results = self.model(cv2.cvtColor(BRG_image, cv2.COLOR_BGR2RGB))
        num_slots = 0
        for i, row in results.pandas().xyxy[0].iterrows():
            xmin, ymin, xmax, ymax = int(row["xmin"]), int(row["ymin"]), int(row["xmax"]), int(row["ymax"])
            cv2.circle(BRG_image, ((xmax - xmin) // 2 + xmin, (ymax - ymin) // 2 + ymin), 10, color=(0, 255, 0), thickness=3)
            num_slots += 1
        return num_slots, BRG_image
    
    def background_run(self, input_dict: dict, output_dict: dict, show_frame=False):
        print("[INFO] Yolo v5 detection is running in background")
        while True:
            for video_id in list(input_dict.keys()):
                num, frame = self.detect(input_dict.pop(video_id))
                if show_frame:
                    cv2.imshow(video_id, frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                if video_id in output_dict:
                    print(f"[WARNNING] Result of video {video_id} was not send to server but was replaced now")
                output_dict[video_id] = num, frame
