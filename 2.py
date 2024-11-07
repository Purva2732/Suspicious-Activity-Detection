from ultralytics import YOLO
import cv2
import socket
import time

# Load the pre-trained YOLOv8n model
model = YOLO('yolov8n.pt')

# Check the class names to see how 'cell phone' is labeled
print(model.names)

# Replace 'http://<RPI_IP>:<port>/' with your Raspberry Pi's actual stream URL
cap = cv2.VideoCapture('http://192.168.20.187:8080/', cv2.CAP_FFMPEG)

# UDP setup to send messages to Raspberry Pi
udp_ip = "192.168.20.187"  # Replace with your Raspberry Pi's IP address
udp_port = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Reduce frame size to speed up processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)  # Reduce buffering
cap.set(cv2.CAP_PROP_FPS, 15)  # Set to 15 FPS, you can tweak this value

frame_skip_rate = 2
frame_count = 0

# Loop to continuously get frames from the stream
while True:
    frame_count += 1
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image from the stream.")
        break

    # Skip frames for faster processing
    if frame_count % frame_skip_rate != 0:
        continue

    # Perform object detection
    results = model(frame, conf=0.5, iou=0.45, verbose=False)

    # Extract detected class names and draw bounding boxes only for cell phones
    annotated_frame = frame.copy()

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = model.names[class_id]

            if class_name == 'cell phone':
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Send UDP message to Raspberry Pi
                sock.sendto(b"hello darshan", (udp_ip, udp_port))
                print("hello darshan")

    # Display the frame with detections
    cv2.imshow('YOLOv8 Live Object Detection', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
sock.close()