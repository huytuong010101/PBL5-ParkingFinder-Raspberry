import requests
import cv2
from datetime import datetime

class RequestInfo:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        
    def background_run(self, output_dict: dict):
        print("[INFO] Send request job is running in background")
        while True:
            for video_id in list(output_dict.keys()):
                num, frame = output_dict.pop(video_id)
                cv2.imwrite("./.tmp.jpg", frame)
                payload = {
                    'park_id': str(video_id),
                    'time': str(datetime.now()).replace(" ", "T") + "Z",
                    'num_of_empty_space': str(num),
                    'token': str(self.token)
                }
                files=[
                    ('file',("tmp.jpg", open("./.tmp.jpg",'rb'),'image/jpg'))
                ]
                headers = {}
                response = requests.request("POST", self.url, headers=headers, data=payload, files=files)
                if response.status_code != 200:
                    print(f"[ERROR] Failt to request to server with video {video_id}")
                    print(response.text)