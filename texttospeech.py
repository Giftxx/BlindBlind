import cv2
import pytesseract
from gtts import gTTS
from IPython.display import Audio
import os
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\acer\tesseract.exe'
def text_to_speech(text, output_file='output.mp3'):
    tts = gTTS(text=text,lang='th',slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

def process_text():
    first_iteration = True
    last_print_time = time.time()
    cap = cv2.VideoCapture(2)

    while True:
        ret, frame = cap.read()
        cv2.imshow('Webcam', frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        current_time = time.time()
        if first_iteration or (current_time - last_print_time >= 8):

            text = pytesseract.image_to_string(gray_frame, lang='tha+eng')
            #text = pytesseract.image_to_string(gray_frame, lang='tha+eng', config='--psm 6 --oem 1')

            if text:
                print("Text detected:", text)
                text_to_speech(text)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            last_print_time = current_time
            first_iteration = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_text()
    