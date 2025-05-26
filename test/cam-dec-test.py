import cv2
import requests
import numpy as np

url = "http://192.168.68.114:81/stream"
stream = requests.get(url, stream=True)

bytes_buffer = b""

for chunk in stream.iter_content(chunk_size=1024):
    print(chunk)
    bytes_buffer += chunk
    start = bytes_buffer.find(b'\xff\xd8')  # JPEG start
    end = bytes_buffer.find(b'\xff\xd9')    # JPEG end

    if start != -1 and end != -1:
        jpg = bytes_buffer[start:end+2]
        bytes_buffer = bytes_buffer[end+2:]

        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("ESP32 MJPEG", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
