from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from userclass import User
from eventclass import Event
from ai import AiHandler
import uuid
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_for_session"


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        # Create a unique UserID
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
            # IMPORTANT: We store user info in the session
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            errors.append("Invalid username or password.")

    return render_template('login.html', errors=errors)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/api/lessons')
def get_month_lessons():
    if 'user_id' not in session:
        return jsonify([])

    user_events = Event.get_event_with_user_id(session['user_id'])

    month = request.args.get('month')  # "5" gibi
    year = request.args.get('year')  # "2026" gibi

    result = []
    for event in user_events:
        event_date = event[4]  # Format: "2026-05-12"
        e_year, e_month, e_day = event_date.split('-')

        if e_year == year and int(e_month) == int(month):
            result.append({"day": int(e_day), "hasLesson": True})

    return jsonify(result)


@app.route('/api/schedule/<date_str>')
def get_day_schedule(date_str):
    if 'user_id' not in session:
        return jsonify([])

    user_events = Event.get_event_with_user_id(session['user_id'])

    result = []
    for event in user_events:
        event_date = event[4]
        if event_date == date_str:
            start_time = event[5]
            hour = int(start_time.split(':')[0])
            result.append({"hour": hour, "isFilled": True, "title": event[2]})

    return jsonify(result)


@app.route('/api/lessons/add', methods=['POST'])
def add_lesson_api():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    date_str = data.get('date')
    time_slot = data.get('time')

    hour = int(time_slot.split(':')[0])
    end_time = f"{str(hour + 1).zfill(2)}:00"

    Event.add_event(session['user_id'], "Manual Lesson", "Added via UI", date_str, time_slot, end_time)
    return jsonify({"success": True})


@app.route('/api/chat', methods=['POST'])
def ai_chat():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    ai_response = AiHandler.chat_assistant(user_message)

    return jsonify({"response": ai_response})


@app.route('/api/upload_schedule', methods=['POST'])
def upload_schedule():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    if 'schedule_image' not in request.files:
        return jsonify({"success": False, "error": "Fotoğraf bulunamadı."}), 400

    file = request.files['schedule_image']
    if file.filename == '':
        return jsonify({"success": False, "error": "Dosya seçilmedi."}), 400

    if file:
        temp_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "temp_schedule.png")
        file.save(temp_path)

        success, message = AiHandler.analyze_screenshot(temp_path, session['user_id'])

        if os.path.exists(temp_path):
            os.remove(temp_path)

        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 500


if __name__ == '__main__':
    app.run(debug=True)