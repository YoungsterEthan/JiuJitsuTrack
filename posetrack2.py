from ultralytics import YOLO
import cv2
import tensorflow as tf
import numpy as np
from joblib import load

model = YOLO("yolov8s-pose.pt")

classModel = tf.keras.models.load_model('position_classifier.h5', compile=False)
classModel.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(), 
              metrics=['accuracy'])

scaler = load("scaler.joblib")
le = load("label_encoder.joblib")
# source = "video.mp4"

# model.predict(source=source, save=True, imgsz=330, conf=0.3)
placeholder = [-1] * 17 * 3

def predict_position(pose1, pose2):
    # Concatenate and reshape the pose data
    data = np.concatenate((pose1, pose2), axis=0).reshape(1, -1)

    # Normalize the data
    data = scaler.transform(data)

    # Make a prediction
    predictions = classModel.predict(data)

    # Convert prediction from probabilities to class label
    predicted_label = np.argmax(predictions, axis=1).reshape(-1, 1)

    # Decode the label
    print(predicted_label)
    predicted_label = le.inverse_transform(predicted_label)

    return predicted_label[0]




vidcap = cv2.VideoCapture("video.avi")
success,img = vidcap.read()

while vidcap.isOpened():
    success,img = vidcap.read()

    if success:

        results = model.predict(source=img, imgsz=330, conf=0.3)
        poses = [result for result in results[0].keypoints]
        annotated_frame = results[0].plot()
        if len(poses) == 2:
            label = predict_position(poses[0], poses[1])
            annotated_frame = cv2.putText(annotated_frame, str(label), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

        
        cv2.imshow("Pose Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

vidcap.release()