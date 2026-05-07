import google.generativeai as genai
from PIL import Image
import json
import sqlite3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'student_checking.db'

genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

class AiHandler:
    @staticmethod
    def analyze_screenshot(image_path, current_user_id):
        """
        Ders programı ekran görüntüsünü analiz eder ve dersleri veritabanına kaydeder.
        """
        try:
            img = Image.open(image_path)

            prompt = """
            Analyze this course schedule image and extract all lessons. 
            Return ONLY a JSON list in the following format:

            [
                {
                    "title": "Course Name", 
                    "description": "Teacher or Room", 
                    "date": "YYYY-MM-DD", 
                    "start_time": "HH:MM", 
                    "end_time": "HH:MM"
                }
            ]

            RULES:
            1. Output ONLY the raw JSON. No introductory text.
            2. If the date is not clear, use the dates for the current week.
            3. Use 24-hour time format (e.g., 14:30).
            """

            response = model.generate_content([prompt, img])
            raw_text = response.text

            json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
            
            if not json_match:
                return False, "AI could not find structured data in the image."

            events = json.loads(json_match.group())

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            added_count = 0
            for e in events:
                cursor.execute('''
                    INSERT INTO events (user_id, title, description, date, start_time, end_time) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    current_user_id, 
                    e['title'], 
                    e.get('description', ''), 
                    e['date'], 
                    e['start_time'], 
                    e['end_time']
                ))
                added_count += 1

            conn.commit()
            conn.close()

            return True, f"Successfully added {added_count} lessons to your calendar."

        except Exception as err:
            return False, f"System Error: {str(err)}"

    @staticmethod
    def chat_assistant(user_message):
        """
        Kullanıcı ile sohbet eden asistan fonksiyonu.
        """
        chat_prompt = f"""
        You are a helpful student assistant. 
        Current request: {user_message}
        Remember to stay professional and remind the user that you can make mistakes.
        """
        response = model.generate_content(chat_prompt)
        return response.text

    @app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        # UserID oluşturma (Benzersiz numara)
        import uuid
        user_id = uuid.uuid4().int & ((1 << 31) - 1)
        
        if User.register_user(username, password, user_id):
            return redirect(url_for('login'))
        else:
            errors.append("This username is already taken.")
    return render_template('register.html', errors=errors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        
        user = User.login(username, password)
        if user:
            session['user_id'] = user[0] # user_id'yi saklar
            session['username'] = user[1] # username'i saklar
            return redirect(url_for('dashboard'))
        else:
            errors.append("Invalid username or password.")
    return render_template('login.html', errors=errors)