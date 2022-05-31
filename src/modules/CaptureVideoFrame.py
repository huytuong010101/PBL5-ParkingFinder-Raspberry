import cv2
import time


class CaptureVideoFrame:
    def __init__(self, source, video_id, time_interval: int=2):
        self.videp_capture = cv2.VideoCapture(source)
        self.time_interval = time_interval
        self.video_id = video_id
        self.source = source
        
    def background_run(self, frame_dict):
        print(f"[INFO] Capture frame from video {self.video_id} in background")
        previous_time = 0
        while self.videp_capture.isOpened():
            # Fetch next frame
            success, frame = self.videp_capture.read()
            # Check if after interval time
            if time.time() - previous_time < self.time_interval:
                continue
            # Check if fetch frame success
            if not success:
                print(f"[ERROR] Cannot get frame from source {self.source}. Stop this loop!")
                continue
            # Check if already have frame in dict then assisn
            if self.video_id in frame_dict:
                print(f"[WARNNING] Update frame but previous frame was not precessed.")
            frame_dict[self.video_id] = frame
            previous_time = time.time()