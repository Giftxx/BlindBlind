import speech_recognition as sr  
from gtts import gTTS 
from playsound import playsound 
from datetime import datetime

r = sr.Recognizer()
with sr.Microphone() as source: 
	text = "สวัสดีค่ะ ยินดีต้อนรับ  สามารถเลือกหมวดการทำงานได้ดังนี้ค่ะ 1 หมวดreading 2 หมวดfeeling 3 หมวด what's that"
	tts = gTTS(text, lang="th")
	tts.save("welcome.mp3")
	playsound("welcome.mp3")
	
	playsound("sound.mp3") 
	audio = r.record(source, duration=5) #บันทึกเสียง 5 วินาที
	playsound("sound.mp3") 

	try:
		text = r.recognize_google(audio, language="th") #ส่งไปให้google cloud
		if "หมวดreading" or "1" in text:
			text = "สวัสดีค่ะ หมวดการอ่านนะคะ"
		if "หมวดfeeling" or "2" in text:
			text = "สวัสดีค่ะ หมวดตรวจจับความรู้สึกนะคะ"
		if text == "กี่โมงแล้ว":
			now = datetime.now() #รับค่าเวลาขณะนั้น
			text = now.strftime("ขณะนี้เวลา%Hนาฬิกา%Mนาที%Sวินาที")
	except:
		text = "ขอโทษค่ะ กรุณาพูดอีกรอบ"
		
	tts = gTTS(text, lang="th") #ส่งไปให้google cloud
	tts.save("answer.mp3") #บันทึกเสียงที่ได้จากgoogle cloud
	playsound("answer.mp3")