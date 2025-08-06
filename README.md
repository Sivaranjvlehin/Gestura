# Gestura
A gesture-controlled PDF reader.
# 🤘 GESTURA - Gesture-Controlled PDF Reader

**GESTURA** is an innovative, touchless PDF reader that uses real-time hand gestures captured via webcam to control PDF navigation and annotation. Designed using Python, Flask, OpenCV, and CVZone, it provides a futuristic, hygienic, and accessible way to interact with documents—especially useful in presentations, educational settings, or for users with physical impairments.

## 📌 Features

- 📄 Gesture-based page navigation (Next, Previous)
- 🎯 Real-time pointer movement using index finger
- 📤 Upload and render PDF from any page
- ⚡ Fast and responsive UI
- 🔒 Secure and isolated file handling
- 💻 Cross-platform compatibility (Windows, macOS, Linux)

## 🖐 Supported Gestures

| Gesture | Action         |
|---------|----------------|
| Pinky   | Next Page      |
| Thumb   | Previous Page  |
| Index   | Pointer/Marker |

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript  
- **Backend**: Python, Flask  
- **Libraries**: OpenCV, CVZone, PyMuPDF, NumPy, Flask-CORS, Werkzeug

## 🧰 Installation & Setup

### Prerequisites
- Python 3.8+
- A webcam (integrated or external)

### Installation Steps
```bash
git clone https://github.com/yourusername/gestura.git
cd gestura
pip install -r requirements.txt
```

### Run the App
```bash
python app.py
```
Then open `http://localhost:5000` in your browser.

## 📂 Project Structure

```
gestura/
├── static/
├── templates/
├── uploads/
├── app.py
├── gesture.py
├── pdf_handler.py
└── requirements.txt
```

## 📈 Performance Overview

- Gesture Recognition Accuracy: ~83%
- Average System Response Time: ~400ms
- PDF Navigation: Smooth, real-time gesture-controlled
- Resource Usage: Within optimal limits

## 🧪 Testing Conducted

- ✅ Unit Testing  
- ✅ Integration Testing  
- ✅ User Acceptance Testing  
- ✅ Performance Testing  
- ✅ Error Handling for invalid inputs

## 🚀 Future Enhancements

- Support for multiple file formats (DOCX, PPTX, etc.)
- Voice command integration
- Cross-platform desktop deployment
- AI/ML-powered gesture classification
- AR/VR & Eye-tracking features
- Cloud synchronization & user customization

## 👨‍💻 Contributors

- **Sivaranj V Lehin**
- VI Semester BCA Project Team

## 📚 References

- https://docs.opencv.org/
- https://pymupdf.readthedocs.io/
- https://flask.palletsprojects.com/
- https://numpy.org/doc/
- https://flask-cors.readthedocs.io/

## 📃 License

This project is licensed under the MIT License.

## 💡 Inspiration

GESTURA was created to redefine the way users interact with documents—enabling a cleaner, smarter, and more accessible reading experience, especially in post-pandemic environments or for users with mobility constraints.
