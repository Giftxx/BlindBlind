from flask import Flask, render_template, redirect, url_for,request
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import subprocess

app = Flask(__name__)
running_processes = {}

@app.route('/')
def index():
    return render_template('page1.html')

def recognize_audio(source, recognizer, duration=5):
    text = None
    try:
        audio = recognizer.record(source, duration=duration)
        text = recognizer.recognize_google(audio, language="th")
    except sr.UnknownValueError:
        text = "ขอโทษค่ะ ไม่สามารถรับรู้เสียงได้"
    except sr.RequestError:
        text = "ขอโทษค่ะ เกิดข้อผิดพลาดในการเชื่อมต่อกับ Google API"
    return text

@app.route('/NextPage')
def NextPage():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text = "สวัสดีค่ะ กรุณาเลือกหมวดการทำงานดังนี้ 1 ตรวจจับวัตถุ 2 อ่านข้อความ 3 ระบุสี 4ตรวจจับความรู้สึก"
        tts = gTTS(text, lang="th")
        tts.save("welcome.mp3")
        playsound("welcome.mp3")

        playsound("sound.mp3")
        text = recognize_audio(source, recognizer)
        playsound("sound.mp3")

        if text:
            if "ตรวจจับวัตถุ" in text or "1" in text:
                playsound("speech1.mp3")
                return redirect(url_for('object_page'))
            elif "อ่านข้อความ" in text or "2" in text:
                playsound("speech2.mp3")
                return redirect(url_for('read_page'))
            elif "ระบุสี" in text or "3" in text:
                playsound("speech3.mp3")
                return redirect(url_for('color_page'))
            elif "ความรู้สึก" in text or "4" in text:
                playsound("speech4.mp3")
                return redirect(url_for('feeling_page'))
            else:
                text = "ขอโทษค่ะ ไม่เข้าใจคำสั่ง"

    tts = gTTS(text, lang="th")
    tts.save("answer.mp3")
    playsound("answer.mp3")
    return redirect(url_for('index'))


@app.route('/object')
def object_page():
    process = subprocess.Popen(['python', 'object_main.py'])
    running_processes["object"] = process
    return render_template('object.html')

@app.route('/read')
def read_page():
    process = subprocess.Popen(['python', 'texttospeech.py'])
    running_processes["อ่านข้อความ"] = process
    return render_template('read.html')

@app.route('/color')
def color_page():
    process = subprocess.Popen(['python', 'colordetection.py'])
    running_processes["ระบุสี"] = process
    return render_template('color.html')

@app.route('/feeling')
def feeling_page():
    process = subprocess.Popen(['python', 'TestEmotionDetector.py'])
    running_processes["ความรู้สึก"] = process
    return render_template('feeling.html')


@app.route('/message')
def message():
    return """
    <html>
    <head>
        <style>
            body {
                background-image:linear-gradient(to right, #AACAEF, #FDE7F9);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif; /* เปลี่ยนแบบอักษรเป็น Arial */
            }
            h1 {
                font-size: 50px;
                margin-bottom: 50px;
                color: white; /* เปลี่ยนสีของข้อความเป็นสีขาว */
            }
            button {
                display: block;
                width: 1000px;
                height: 120px;
                font-size: 35px;
                margin-bottom: 20px;
                background-color:  #70A1FF; /* เปลี่ยนสีพื้นหลังของปุ่ม */
                color: white; /* เปลี่ยนสีของข้อความบนปุ่ม */
                border: none; /* ลบเส้นขอบ */
                border-radius: 10px; /* ทำให้มีมุมโค้งบนเพื่อสวยงาม */
                cursor: pointer; /* เปลี่ยนรูปแบบเมาส์เป็นรูปแบบตัวชี้ */
            }
            button:hover {
                background-color: #98D9E1; /* เปลี่ยนสีพื้นหลังของปุ่มเมื่อเมาส์วางบนปุ่ม */
            }
        </style>
    </head>
    <body>
        <h1>Blind Blind</h1>
        <form action="/submit" method="post">
            <button name="button" value="ตรวจจับวัตถุ" type="submit">ตรวจจับวัตถุ</button>
            <button name="button" value="อ่านข้อความ" type="submit">อ่านข้อความ</button>
            <button name="button" value="ระบุสี" type="submit">ระบุสี</button>
            <button name="button" value="ความรู้สึก" type="submit">ความรู้สึก</button>
        </form>
    </body>
    </html>
    """
@app.route('/submit', methods=['POST'])
def submit():
    button_clicked = request.form['button']
    if button_clicked == 'ตรวจจับวัตถุ':
        playsound("speech1.mp3")
        process = subprocess.Popen(['python', 'object_main.py'])
        running_processes[button_clicked] = process
        return render_template('object.html')
    
    elif button_clicked == 'อ่านข้อความ':
        playsound("speech2.mp3")
        process = subprocess.Popen(['python', 'texttospeech.py'])
        running_processes[button_clicked] = process
        return render_template('read.html')
    
    elif button_clicked == 'ระบุสี':
        playsound("speech3.mp3")
        process = subprocess.Popen(['python', 'colordetection.py'])
        running_processes[button_clicked] = process
        return render_template('color.html')
    
    elif button_clicked == 'ความรู้สึก':
        playsound("speech4.mp3")
        process = subprocess.Popen(['python', 'TestEmotionDetector.py'])
        running_processes[button_clicked] = process
        return render_template('feeling.html')

@app.route('/stop', methods=['POST'])
def stop():
    for key, process in running_processes.items():
        process.terminate()
    
    running_processes.clear()
    playsound("speech8.mp3")
    return redirect('/message')


if __name__ == '__main__':
    app.run(debug=True)