from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Initialize CORS with your app

model = YOLO("yolov8s.pt")
def serialize(A):
    return {"x1": int(A[0]), "y1": int(A[1]), "x2": int(A[2]), "y2": int(A[3])}

    


@app.route('/detect', methods=['POST'])
def detect():
    # Get the image from the request
    image_file = request.files['image']

    # Convert the image to a format compatible with OpenCV
    image_np = np.fromstring(image_file.read(), np.uint8)
    image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Save the image temporarily so ultralytics YOLO can read it
    temp_image_path = 'temp_image.jpg'
    cv2.imwrite(temp_image_path, image_cv)

    # Detect persons in the image
    results = model.predict(image_cv, conf=0.3)
    annotated_frame = results[0].plot()

        # Display the annotated frame
    cv2.imwrite('temp_image.jpg', annotated_frame)
    
    box_list = []
    for result in results:                                         # iterate results
        boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
        for box in boxes:                                          # iterate boxes
            r = box.xyxy[0].astype(int)                            # get corner points as int
            box_list.append(serialize(r))
            # print(r)          
    print("The boxes:", box_list)

    return jsonify(box_list)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
