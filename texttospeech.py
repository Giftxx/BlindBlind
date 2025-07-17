# ไม่มี ollam ข้อมูลมีคำผิดอยู่บ้าง
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound
import uuid
import os
import time
import re
from pythainlp.tokenize import word_tokenize

# ตั้งค่า path ของ tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ฟังก์ชันทำความสะอาดและตัดคำ
def clean_text(text):
    # ลบอักขระที่ไม่จำเป็น
    text = re.sub(r'[^\u0E00-\u0E7FA-Za-z0-9]', '', text)
    text = re.sub(r'\s+', '', text)  # ลบ space ผิดปกติ

    # ใช้ PyThaiNLP ตัดคำ (engine='newmm' แม่นที่สุด)
    words = word_tokenize(text, engine='newmm')

    # รวมคำใหม่เป็นประโยคที่พูดได้
    return ' '.join(words)

# แปลงข้อความเป็นเสียงภาษาไทย
def text_to_speech(text):
    if not text.strip():
        return
    filename = f"speech_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='th', slow=False)
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# ฟังก์ชันหลัก อ่านกล้องและประมวลผล
def process_text():
    cap = cv2.VideoCapture(0)
    first_iteration = True
    last_print_time = time.time()

    while True:
        ret, frame = cap.read()
        cv2.imshow("Webcam", frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 31, 2)

        current_time = time.time()
        if first_iteration or (current_time - last_print_time >= 8):
            raw_text = pytesseract.image_to_string(thresh, lang='tha+eng')

            if raw_text.strip():
                print("\n[Raw OCR]:", raw_text)
                cleaned = clean_text(raw_text)
                print("[Cleaned ]:", cleaned)
                text_to_speech(cleaned)

            last_print_time = current_time
            first_iteration = False

        # กด q เพื่อออก
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_text()

# ------------------------------------------------------มี ollama 
# import cv2
# import pytesseract
# from gtts import gTTS
# from playsound import playsound
# import uuid
# import os
# import time
# import re
# from pythainlp.tokenize import word_tokenize
# from threading import Thread
# import subprocess

# # ตั้งค่า path ของ tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # ล้างข้อความจาก OCR
# def clean_text(text):
#     text = re.sub(r'[^\u0E00-\u0E7FA-Za-z0-9]', '', text)
#     text = re.sub(r'\s+', '', text)
#     words = word_tokenize(text, engine='newmm')
#     return ' '.join(words)

# # เรียก Ollama มาช่วยแก้ไขข้อความ OCR
# def fix_with_ollama(text):
#     if not text.strip():
#         return ""

#     prompt = f"""ข้อความ OCR ต่อไปนี้อาจผิดพลาด กรุณาช่วยปรับให้เป็นประโยคภาษาไทยที่ถูกต้อง อ่านแล้วเข้าใจง่าย:{text}"""

#     try:
#         result = subprocess.run(
#             ["ollama", "run", "llama3", prompt],
#             capture_output=True,
#             text=True,
#             timeout=15,
#             encoding='utf-8'  # <--- เพิ่มบรรทัดนี้
#         )
#         return result.stdout.strip()
#     except Exception as e:
#         print("[Ollama Error]:", e)
#         return text

# # แปลงข้อความเป็นเสียง (รันแยก Thread)
# def text_to_speech_async(text):
#     def speak():
#         if not text.strip():
#             return
#         filename = f"speech_{uuid.uuid4().hex}.mp3"
#         tts = gTTS(text=text, lang='th', slow=False)
#         tts.save(filename)
#         playsound(filename)
#         os.remove(filename)
#     Thread(target=speak).start()

# # ฟังก์ชันหลัก
# def process_text():
#     cap = cv2.VideoCapture(0)
#     first_iteration = True
#     last_print_time = time.time()
#     last_result = ""

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         cv2.imshow("Webcam", frame)

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (3, 3), 0)
#         thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                        cv2.THRESH_BINARY, 31, 2)

#         current_time = time.time()
#         if first_iteration or (current_time - last_print_time >= 8):
#             raw_text = pytesseract.image_to_string(thresh, lang='tha+eng')

#             if raw_text.strip():
#                 print("\n[Raw OCR]:", raw_text)
#                 cleaned = clean_text(raw_text)
#                 print("[Cleaned ]:", cleaned)

#                 fixed = fix_with_ollama(cleaned)
#                 print("[Ollama  ]:", fixed)

#                 if fixed != last_result:
#                     text_to_speech_async(fixed)
#                     last_result = fixed
                

#             last_print_time = current_time
#             first_iteration = False

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     process_text()
# # ---------------------------------------------ollama
# import cv2
# import pytesseract
# from gtts import gTTS
# from playsound import playsound
# import uuid
# import os
# import time
# import re
# from pythainlp.tokenize import word_tokenize
# from threading import Thread
# import subprocess

# # ตั้งค่า path ของ tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # ล้างข้อความจาก OCR
# def clean_text(text):
#     text = re.sub(r'[^\u0E00-\u0E7FA-Za-z0-9]', '', text)
#     text = re.sub(r'\s+', '', text)
#     words = word_tokenize(text, engine='newmm')
#     return ' '.join(words)

# # เรียก Ollama มาช่วยแก้ไขข้อความ OCR
# def fix_with_ollama(text):
#     if not text.strip():
#         return ""

#     prompt = f"""
# ข้อความต่อไปนี้ถูกแปลงมาจากภาพโดยระบบ OCR ซึ่งอาจมีคำผิดหรือข้อมูลเพี้ยน กรุณาช่วย "เฉพาะ" ในส่วนที่สามารถเข้าใจได้เท่านั้น
# ถ้าไม่สามารถแปลความหมายของข้อความได้ **กรุณาไม่ตอบอะไรกลับมาเลย**
# ห้ามเดา และห้ามแต่งประโยคขึ้นเอง

# **กรุณาตอบเป็นภาษาไทยเท่านั้น ห้ามอธิบายเพิ่มเติม หรือใช้ภาษาอังกฤษ**

# ข้อความ OCR:
# {text}
# """


#     try:
#         result = subprocess.run(
#             ["ollama", "run", "llama3", prompt],
#             capture_output=True,
#             text=True,
#             timeout=60,  # ⬅ เปลี่ยนจาก 15 เป็น 60 วินาที
#             encoding='utf-8'  
# )
#         if result.returncode != 0 or not result.stdout.strip():
#             print("[Ollama STDERR]:", result.stderr)
#             return text
#         return result.stdout.strip()
#     except Exception as e:
#         print("[Ollama Error]:", e)
#         return text

# # แปลงข้อความเป็นเสียง (รันแยก Thread)
# def text_to_speech_async(text):
#     def speak():
#         if not text.strip():
#             return
#         filename = f"speech_{uuid.uuid4().hex}.mp3"
#         tts = gTTS(text=text, lang='th', slow=False)
#         tts.save(filename)
#         playsound(filename)
#         os.remove(filename)
#     Thread(target=speak).start()

# # ฟังก์ชันหลัก
# def process_text():
#     cap = cv2.VideoCapture(0)
#     first_iteration = True
#     last_print_time = time.time()
#     last_result = ""

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         cv2.imshow("Webcam", frame)

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (3, 3), 0)
#         thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                        cv2.THRESH_BINARY, 31, 2)

#         current_time = time.time()
#         if first_iteration or (current_time - last_print_time >= 8):
#             raw_text = pytesseract.image_to_string(thresh, lang='tha+eng')

#             if raw_text.strip():
#                 print("\n[Raw OCR]:", raw_text)
#                 cleaned = clean_text(raw_text)
#                 print("[Cleaned ]:", cleaned)

#                 fixed = fix_with_ollama(cleaned)
#                 print("[Ollama  ]:", fixed)

#                 # ใช้ข้อความที่แก้ไขแล้วจาก Ollama สำหรับพูด
#                 if fixed != last_result:
#                     text_to_speech_async(fixed)
#                     last_result = fixed

#             last_print_time = current_time
#             first_iteration = False

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     process_text()
