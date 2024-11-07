import cv2
import numpy as np
from keras.models import load_model


# Load the trained model
model = load_model('keras_model.h5')  # Update the path accordingly

# Load the labels from the text file
with open('labels.txt', 'r') as file:  # Update the path accordingly
    labels = file.read().splitlines()

# Open video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam; change for other sources

# Loop to continuously get frames from the camera
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image from the camera.")
        break

    # Preprocess the frame for the model (assuming the model input size is 224x224)
    img = cv2.resize(frame, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Perform activity detection
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)[0]
    activity = labels[predicted_class]

    # Display the result
    cv2.putText(frame, f"Activity: {activity}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Activity Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
