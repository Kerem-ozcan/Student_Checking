import google.generativeai as genai
from PIL import Image
import json
import sqlite3

genai.configure(api_key="BURAYA_API_KEY_GELECEK")
model = genai.GenerativeModel('gemini-1.5-flash')


def ai_screenshot_handler(image_path, current_user_id):

    try:
        img = Image.open(image_path)

        prompt = """
        Sen bir ders programı asistanısın. Bu resimdeki dersleri analiz et.
        Bana SADECE şu formatta bir JSON listesi döndür:
        [{"title": "Ders Adı", "description": "Hoca veya Sınıf", "date": "YYYY-MM-DD", "start_time": "HH:MM", "end_time": "HH:MM"}]

        KURALLAR:
        - Tarih yoksa Bugünü tarih al veya kullanıcıdan gün aralığı veya tarih iste
        - JSON dışında hiçbir açıklama veya metin ekleme.
        - Kullanıcı ile iş ahlaki sınırlarımdan çıkma ve gerekirse nazikçe uyar
        - Belirli aralıklar ile AI olduğunu hatırlat ve hata yapabileceğini belirt
        - Kullanıcının Kişisel hayatına saygı duy ve ahlaki sınırlar içinde öneride bulun
        - Kullanıcı ile aynı dil ile iletişim kur(Gelen girdiye göre cevap ver)
        - Kullanıcı bilgilerini korunmasına katkıda bulun ve hiçbir kişisel bilgiyi başka birisine yayma
        """

        response = model.generate_content([prompt, img])

        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        events = json.loads(raw_text)

        conn = sqlite3.connect('student_checking.db')
        cursor = conn.cursor()

        added_count = 0
        for e in events:
            cursor.execute('''
                INSERT INTO events (user_id, title, description, date, start_time, end_time) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (current_user_id, e['title'], e.get('description', ''), e['date'], e['start_time'], e['end_time']))
            added_count += 1

        conn.commit()
        conn.close()

        return True, f"{added_count} ders başarıyla eklendi."

    except Exception as err:
        return False, f"Hata oluştu: {str(err)}"


# --- FLASK TARAFINDA KULLANIM ÖRNEĞİ ---
"""
@app.route('/upload-ss', methods=['POST'])
def upload_ss():
    file = request.files['screenshot']
    user_id = session.get('user_id')

    if file and user_id:
        path = "temp_ss.png"
        file.save(path)

        # Fonksiyonu çağırıyoruz
        success, message = ai_screenshot_handler(path, user_id)

        if success:
            return redirect('/timetable') # Başarılıysa takvime yönlendir
        else:
            return message
"""