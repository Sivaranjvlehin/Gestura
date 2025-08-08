from flask import Flask, render_template, request, jsonify
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/run-gesture', methods=['POST'])
def run_gesture():
    if 'pdfFile' not in request.files:
        return jsonify({"success": False, "message": "No file part in the request."})
    
    file = request.files['pdfFile']
    start_page = request.form.get('startPage', default="1")  # Get startPage from form data

    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected."})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            # Pass both the PDF file path and start page number to gesture_recognition.py
            subprocess.Popen(["python", "gesture_recognition.py", file_path, start_page])
            return jsonify({"success": True, "message": "Gesture control started!"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    else:
        return jsonify({"success": False, "message": "Invalid file type. Only PDF files are allowed."})

if __name__ == '__main__':
    app.run(debug=True)