import cv2
import numpy as np
from keras.models import model_from_json
import time
from gtts import gTTS
from IPython.display import Audio
import os

def text_to_speech(text, output_file='output.mp3'):
    tts = gTTS(text=text, lang='th', slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

def emotion_processing():
    emotion_dict = {0: "โกรธ", 1: "เบื่อเบื่อ", 2: "กลัวนิดหน่อย", 3: "ยิ้ม มีความสุขดี", 4: "นิ่งนิ่ง", 5: "เศร้า", 6: "ตะลึง ตกใจ"}

    # load json and create model
    json_file = open(r'D:\AIgen\blindblind\Emotion_detection_with_CNN-main\model\emotion_model.json',"r")
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

    # load weights into new model
    emotion_model.load_weights(r'D:\AIgen\blindblind\Emotion_detection_with_CNN-main\model\emotion_model.h5')

    # start the webcam feed
    cap = cv2.VideoCapture(2)
    first_iteration = True
    last_print_time = time.time()

    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        frame = cv2.resize(frame, (390, 640))
        if not ret:
            break
        face_detector = cv2.CascadeClassifier(r'D:\AIgen\blindblind\Emotion_detection_with_CNN-main\haarcascades\haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            # cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            label = "คนด้านหน้าของคุณกำลังรู้สึก {}".format(emotion_dict[maxindex])
            current_time = time.time()
            if first_iteration or (current_time - last_print_time >= 8):
                print(emotion_dict[maxindex])

                text_to_speech(label)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                last_print_time = current_time
                first_iteration = False       

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    emotion_processing()