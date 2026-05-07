import google.generativeai as genai
from PIL import Image
import json
import sqlite3
import re
from pathlib import Path

# Database setup
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'student_checking.db'

# Configure Gemini
# Replace "YOUR_API_KEY_HERE" with your actual API Key
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

class AiHandler:
    @staticmethod
    def analyze_screenshot(image_path, current_user_id):
        """
        Analyzes the course schedule screenshot and saves lessons to the database.
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

            # Extract JSON from potential markdown markers
            json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
            
            if not json_match:
                return False, "AI could not find structured data in the image."

            events = json.loads(json_match.group())

            # Database Connection
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
        Helper function for the AI Chat Sidebar.
        """
        chat_prompt = f"You are a helpful student assistant. User says: {user_message}"
        response = model.generate_content(chat_prompt)
        return response.text