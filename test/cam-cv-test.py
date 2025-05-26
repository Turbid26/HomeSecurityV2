import cv2

cap = cv2.VideoCapture("http://192.168.68.114:81/stream")

if not cap.isOpened():
    print("Error: Could not open stream")
    exit()

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("⚠️ Skipped corrupted frame")
        continue  # skip invalid frames

    cv2.imshow("Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
