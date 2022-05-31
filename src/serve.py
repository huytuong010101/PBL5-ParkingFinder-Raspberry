from threading import Thread
from multiprocessing import Process, Manager
from modules import CaptureVideoFrame, Yolo5Detection, RequestInfo
from config import config

if __name__ == "__main__":
    # Init all camera capture
    video_capture_tasks = [
        CaptureVideoFrame(
            source=config["PARK"][park_id]["VIDEO_SRC"],
            video_id=str(park_id),
            time_interval=config["PARK"][park_id]["CAPTURE_INTERVAL"]
        ) for park_id in config["PARK"]
    ]
    # Init detection
    detection_task = Yolo5Detection(
        yolo_path=config["MODEL"]["YOLO_REPO"],
        model_path=config["MODEL"]["PATH"],
        conf=config["MODEL"]["CONF"],
        iou=config["MODEL"]["IOU"]
    )
    # Init request
    request_task = RequestInfo(
        url=config["SERVER"]["URL"],
        token=config["NODE"]["TOKEN"]
    )
    # This variable use to share data between thread
    shared_var = Manager()
    frame_dict = shared_var.dict()
    output_dict = shared_var.dict()
    # Create all thread
    video_capture_threads = [Thread(target=video_capture_task.background_run, args=(frame_dict,), daemon=True) for video_capture_task in video_capture_tasks]
    detection_thread = Thread(target=detection_task.background_run, args=(frame_dict, output_dict, True), daemon=True)
    request_thread = Thread(target=request_task.background_run, args=(output_dict,), daemon=True)
    # Start all thread
    for video_capture_thread in video_capture_threads:
        video_capture_thread.start()
    detection_thread.start()
    request_thread.start()
    # Waitiing
    detection_thread.join()
    request_thread.join()
    for video_capture_thread in video_capture_threads:
        video_capture_thread.join()