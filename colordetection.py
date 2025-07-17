# import cv2
# import time
# from gtts import gTTS
# from IPython.display import Audio
# import os
# import uuid
# from playsound import playsound

# def text_to_speech(text):
#     filename = f"speech_{uuid.uuid4().hex}.mp3"
#     tts = gTTS(text=text, lang='th', slow=False)
#     tts.save(filename)
#     playsound(filename)
#     os.remove(filename)  # ลบไฟล์หลังเล่นเสร็จ

# def color_processing():
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#     first_iteration = True
#     last_print_time = time.time()

#     while True:
#         _, frame = cap.read()
#         hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         height, width, _ = frame.shape

#         cx = int(width / 2)
#         cy = int(height / 2)

#         pixel_center = hsv_frame[cy, cx]
#         hue_value = pixel_center[0]
#         color = "Undefined"
#         if hue_value < 5:
#             color = "สีแดง"
#         elif hue_value < 11:
#             color = "สีแดงส้ม"
#         elif hue_value < 22:
#             color = "สีเหลืองส้ม"
#         elif hue_value < 33:
#             color = "สีเหลือง"
#         elif hue_value < 45:
#             color = "สีเหลืองเขียว"
#         elif hue_value < 60:
#             color = "สีเขียว"
#         elif hue_value < 85:
#             color = "สีเขียวอ่อน"
#         elif hue_value < 100:
#             color = "สีเขียว"
#         elif hue_value < 115:
#             color = "สีฟ้า"
#         elif hue_value < 130:
#             color = "สีน้ำเงิน"
#         elif hue_value < 150:
#             color = "สีน้ำเงิน"
#         elif hue_value < 165:
#             color = "สีคราม"
#         elif hue_value < 170:
#             color = "สีม่วง"
#         elif hue_value < 190:
#             color = "สีม่วงแดง"
#         elif hue_value < 220:
#             color = "สีแดงกุหลาบ"
#         elif hue_value < 255:
#             color = "สีม่วงแดง"
#         else:
#             color = "สีดำ"

#         pixel_center_bgr = frame[cy, cx]
#         b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
#         cv2.rectangle(frame, (cx - 220, 10), (cx + 130, 120), (255, 255, 255), -1)
#         cv2.putText(frame, "COLOR", (cx - 200, 100), 0, 3, (b, g, r), 5)
#         cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
#         cv2.imshow("Frame", frame)
#         current_time = time.time()
#         if first_iteration or (current_time - last_print_time >= 5):
#             text_to_speech(color)
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 break
#             last_print_time = current_time
#             first_iteration = False
#         key = cv2.waitKey(1)
#         if key == 27:
#             break

# if __name__ == "__main__":
#     color_processing()

import cv2
import time
from gtts import gTTS
from IPython.display import Audio
import os
import uuid
from playsound import playsound
import numpy as np

def text_to_speech(text):
    filename = f"speech_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='th', slow=False)
    tts.save(filename)
    playsound(filename)
    os.remove(filename)  # ลบไฟล์หลังเล่นเสร็จ

def get_english_color_name(thai_color):
    """
    แปลงชื่อสีภาษาไทยเป็นภาษาอังกฤษเพื่อการแสดงผล
    """
    color_dict = {
        "สีดำ": "Black",
        "สีขาว": "White", 
        "สีเทาอ่อน": "Light Gray",
        "สีเทาเข้ม": "Dark Gray",
        "สีแดงสด": "Bright Red",
        "สีแดง": "Red",
        "สีแดงอ่อน": "Light Red",
        "สีแดงส้ม": "Red Orange",
        "สีส้มสด": "Bright Orange",
        "สีส้ม": "Orange",
        "สีส้มเหลือง": "Yellow Orange",
        "สีเหลืองสด": "Bright Yellow",
        "สีเหลือง": "Yellow",
        "สีเหลืองอ่อน": "Light Yellow",
        "สีเหลืองเขียว": "Yellow Green",
        "สีไลม์": "Lime",
        "สีเขียวสด": "Bright Green",
        "สีเขียว": "Green",
        "สีเขียวอ่อน": "Light Green",
        "สีเขียวมิ้นต์": "Mint Green",
        "สีเขียวฟ้า": "Cyan",
        "สีฟ้าเขียว": "Blue Green",
        "สีฟ้าสด": "Bright Blue",
        "สีฟ้า": "Blue",
        "สีฟ้าอ่อน": "Light Blue",
        "สีฟ้าน้ำเงิน": "Blue",
        "สีน้ำเงินสด": "Bright Navy",
        "สีน้ำเงิน": "Navy",
        "สีน้ำเงินอ่อน": "Light Navy",
        "สีน้ำเงินเข้ม": "Dark Navy",
        "สีคราม": "Indigo",
        "สีม่วงสด": "Bright Purple",
        "สีม่วง": "Purple",
        "สีม่วงอ่อน": "Light Purple",
        "สีม่วงแดง": "Red Purple",
        "สีชมพูเข้ม": "Dark Pink",
        "สีชมพู": "Pink"
    }
    return color_dict.get(thai_color, "Unknown")

def detect_color_advanced(hsv_pixel, brightness_threshold=30, saturation_threshold=30):
    """
    ตรวจจับสีแบบละเอียด โดยพิจารณาจาก Hue, Saturation, และ Value
    """
    hue, saturation, value = hsv_pixel[0], hsv_pixel[1], hsv_pixel[2]
    
    # ตรวจสอบสีขาว/เทา/ดำ ก่อน
    if value < brightness_threshold:
        return "สีดำ"
    elif saturation < saturation_threshold:
        if value > 200:
            return "สีขาว"
        elif value > 120:
            return "สีเทาอ่อน"
        else:
            return "สีเทาเข้ม"
    
    # ตรวจจับสีต่างๆ แบบละเอียด
    if hue < 5 or hue > 175:
        if saturation > 150:
            return "สีแดงสด"
        elif saturation > 100:
            return "สีแดง"
        else:
            return "สีแดงอ่อน"
    elif hue < 8:
        return "สีแดงส้ม"
    elif hue < 12:
        if saturation > 150:
            return "สีส้มสด"
        else:
            return "สีส้ม"
    elif hue < 18:
        return "สีส้มเหลือง"
    elif hue < 25:
        if saturation > 150:
            return "สีเหลืองสด"
        elif saturation > 100:
            return "สีเหลือง"
        else:
            return "สีเหลืองอ่อน"
    elif hue < 35:
        return "สีเหลืองเขียว"
    elif hue < 45:
        return "สีไลม์"
    elif hue < 60:
        if saturation > 150:
            return "สีเขียวสด"
        elif saturation > 100:
            return "สีเขียว"
        else:
            return "สีเขียวอ่อน"
    elif hue < 75:
        return "สีเขียวมิ้นต์"
    elif hue < 85:
        return "สีเขียวฟ้า"
    elif hue < 95:
        return "สีฟ้าเขียว"
    elif hue < 105:
        if saturation > 150:
            return "สีฟ้าสด"
        elif saturation > 100:
            return "สีฟ้า"
        else:
            return "สีฟ้าอ่อน"
    elif hue < 115:
        return "สีฟ้าน้ำเงิน"
    elif hue < 125:
        if saturation > 150:
            return "สีน้ำเงินสด"
        elif saturation > 100:
            return "สีน้ำเงิน"
        else:
            return "สีน้ำเงินอ่อน"
    elif hue < 135:
        return "สีน้ำเงินเข้ม"
    elif hue < 145:
        return "สีคราม"
    elif hue < 155:
        if saturation > 150:
            return "สีม่วงสด"
        elif saturation > 100:
            return "สีม่วง"
        else:
            return "สีม่วงอ่อน"
    elif hue < 165:
        return "สีม่วงแดง"
    elif hue < 175:
        return "สีชมพูเข้ม"
    else:
        return "สีชมพู"

def get_dominant_color(frame, center_x, center_y, sample_size=20):
    """
    หาสีหลักจากพื้นที่รอบๆ จุดกลาง แทนการดูแค่ 1 พิกเซล
    """
    y_start = max(0, center_y - sample_size//2)
    y_end = min(frame.shape[0], center_y + sample_size//2)
    x_start = max(0, center_x - sample_size//2)
    x_end = min(frame.shape[1], center_x + sample_size//2)
    
    # ตัดพื้นที่ตัวอย่าง
    sample_area = frame[y_start:y_end, x_start:x_end]
    
    # หาค่าเฉลี่ยของสี
    mean_color = np.mean(sample_area, axis=(0, 1))
    
    return mean_color.astype(int)

def color_processing():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    first_iteration = True
    last_print_time = time.time()
    last_color = ""
    
    # ตัวแปรสำหรับการปรับแต่งการตรวจจับสี
    sample_size = 30  # ขนาดของพื้นที่ตัวอย่าง
    color_history = []  # เก็บประวัติสีที่ตรวจจับ
    history_size = 5   # จำนวนเฟรมที่จะเก็บไว้
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # แปลงเป็น HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        
        cx = int(width / 2)
        cy = int(height / 2)
        
        # ใช้พื้นที่ตัวอย่างแทนการดู 1 พิกเซล
        dominant_hsv = get_dominant_color(hsv_frame, cx, cy, sample_size)
        dominant_bgr = get_dominant_color(frame, cx, cy, sample_size)
        
        # ตรวจจับสี
        color = detect_color_advanced(dominant_hsv)
        
        # เก็บประวัติสีเพื่อความเสถียร
        color_history.append(color)
        if len(color_history) > history_size:
            color_history.pop(0)
        
        # หาสีที่ปรากฏบ่อยที่สุดในประวัติ
        if len(color_history) >= 3:
            most_common_color = max(set(color_history), key=color_history.count)
        else:
            most_common_color = color
        
        # แสดงผล
        b, g, r = int(dominant_bgr[0]), int(dominant_bgr[1]), int(dominant_bgr[2])
        
        # วาดกรอบข้อมูล
        cv2.rectangle(frame, (cx - 250, 10), (cx + 200, 150), (255, 255, 255), -1)
        cv2.rectangle(frame, (cx - 245, 15), (cx + 195, 145), (0, 0, 0), 2)
        
        # แสดงชื่อสี (ใช้ภาษาอังกฤษเพื่อความเข้ากันได้)
        color_english = get_english_color_name(most_common_color)
        cv2.putText(frame, "COLOR DETECTED", (cx - 230, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(frame, color_english, (cx - 230, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (b, g, r), 2)
        
        # แสดงค่า HSV
        cv2.putText(frame, f"H:{int(dominant_hsv[0])} S:{int(dominant_hsv[1])} V:{int(dominant_hsv[2])}", 
                   (cx - 230, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # แสดงค่า RGB
        cv2.putText(frame, f"R:{r} G:{g} B:{b}", 
                   (cx - 230, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # วาดจุดกลางและพื้นที่ตัวอย่าง
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), 3)
        cv2.rectangle(frame, (cx - sample_size//2, cy - sample_size//2), 
                     (cx + sample_size//2, cy + sample_size//2), (0, 255, 0), 2)
        
        # แสดงตัวอย่างสี
        cv2.rectangle(frame, (cx - 230, 125), (cx - 180, 140), (int(b), int(g), int(r)), -1)
        cv2.rectangle(frame, (cx - 230, 125), (cx - 180, 140), (0, 0, 0), 1)
        
        cv2.imshow("Enhanced Color Detection", frame)
        
        # เล่นเสียง (ใช้ภาษาไทย)
        current_time = time.time()
        if (first_iteration or (current_time - last_print_time >= 3)) and most_common_color != last_color:
            try:
                text_to_speech(most_common_color)  # เสียงเป็นภาษาไทย
                last_color = most_common_color
            except Exception as e:
                print(f"Error in text-to-speech: {e}")
            last_print_time = current_time
            first_iteration = False
        
        # ตรวจสอบการกดปุ่ม
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' หรือ ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    color_processing()