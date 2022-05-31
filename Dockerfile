FROM ultralytics/yolov5:latest-arm64
RUN python3 -m pip install onnx
RUN python3 -m pip install onnxruntime
RUN apt-get update
RUN apt-get install -y libqt5gui5
RUN rm -rf /var/lib/apt/lists/*

