from flask import Flask, request, jsonify, Response, render_template_string
from datetime import datetime
import time

app = Flask(__name__)

latest_data = {
    "status": "offline",
    "site": None,
    "risk": 0,
    "violations": [],
    "time": None
}

last_update = time.time()

# ---------------- LOGIN ----------------
USERNAME = "admin"
PASSWORD = "1234"

# ---------------- DASHBOARD ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PPE Monitor</title>
</head>
<body style="font-family:Arial">

<h2>PPE Monitoring Dashboard</h2>

<p>Status: {{data.status}}</p>
<p>Site: {{data.site}}</p>
<p>Risk: {{data.risk}}</p>
<p>Violations: {{data.violations}}</p>
<p>Time: {{data.time}}</p>

<hr>

<h3>Live Camera</h3>
<img src="/video" width="600">

</body>
</html>
"""

# ---------------- LOGIN PAGE ----------------
LOGIN_PAGE = """
<form method="POST" action="/login">
  <input name="username" placeholder="Username"><br>
  <input name="password" type="password" placeholder="Password"><br>
  <button type="submit">Login</button>
</form>
"""

@app.route('/')
def home():
    return LOGIN_PAGE

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
        return render_template_string(HTML, data=latest_data)
    return "Invalid Login"

# ---------------- RECEIVE DATA ----------------
@app.route('/update', methods=['POST'])
def update():
    global latest_data, last_update

    data = request.json
    last_update = time.time()

    latest_data = {
        "status": "online",
        "site": data.get("site"),
        "risk": data.get("risk"),
        "violations": data.get("violations"),
        "time": str(datetime.now())
    }

    return {"ok": True}

# ---------------- API ----------------
@app.route('/data')
def data():
    if time.time() - last_update > 10:
        latest_data["status"] = "offline"
    return jsonify(latest_data)

# ---------------- LIVE VIDEO STREAM ----------------
camera = None

@app.route('/video_feed')
def video_feed():
    def generate():
        global camera
        while True:
            if camera is None:
                continue
            success, frame = camera.read()
            if not success:
                continue

            import cv2
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video():
    return "<img src='/video_feed'>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)