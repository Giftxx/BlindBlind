import cv2
import pytesseract
from gtts import gTTS
from IPython.display import Audio
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\acer\tesseract.exe'
def text_to_speech(text, output_file='output.mp3'):
    tts = gTTS(text=text,lang='th',slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

def process_text():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow('Webcam', frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray_frame, lang='tha+eng')

        if text:
            print("Text detected:", text)
            text_to_speech(text)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_text()
