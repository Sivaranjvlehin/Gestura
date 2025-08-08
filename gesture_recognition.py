import sys
import cv2
import numpy as np
import fitz  # PyMuPDF for handling PDFs
from cvzone.HandTrackingModule import HandDetector
import time

# ===== Argument Parsing =====
if len(sys.argv) >= 3:
    pdfPath = sys.argv[1]
    try:
        startPage = int(sys.argv[2]) - 1  # Convert to 0-indexed
        if startPage < 0:
            startPage = 0
    except ValueError:
        startPage = 0
else:
    print("Usage: python gesture_recognition.py <PDF_Path> <Start_Page>")
    sys.exit(1)

print(f"Starting gesture recognition on '{pdfPath}' from page {startPage + 1}")

# Parameters
width, height = 1920, 1080
gestureThreshold = 300  # Threshold height for gestures
gestureCooldown = 1  # 1 second cooldown between gestures to prevent fast page turning

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(1, width)
cap.set(1, height)

# Hand Detector Setup
detectorHand = HandDetector(detectionCon=0.7, maxHands=1)

# PDF Setup
pdf_document = fitz.open(pdfPath)
totalPages = pdf_document.page_count
pageNumber = startPage if startPage < totalPages else 0

# Last gesture time to avoid multiple triggers
lastGestureTime = 0

# === Function to resize preserving aspect ratio ===
def resize_preserve_aspect_ratio(image, target_width, target_height):
    h, w = image.shape[:2]
    aspect_ratio = w / h
    if w / h > target_width / target_height:
        new_w = target_width
        new_h = int(new_w / aspect_ratio)
    else:
        new_h = target_height
        new_w = int(new_h * aspect_ratio)

    resized_img = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2
    canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized_img
    return canvas

# Convert PDF page to image
def pdf_to_image(page_num, zoom_x=2.5, zoom_y=2.5):
    page = pdf_document.load_page(page_num)
    matrix = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=matrix)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    if pix.alpha:
        img = img.reshape((pix.height, pix.width, 4))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = img.reshape((pix.height, pix.width, 3))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

# Load the initial page
imgCurrent = pdf_to_image(pageNumber)
imgCurrent = resize_preserve_aspect_ratio(imgCurrent, width, height)

# Full-screen display
cv2.namedWindow("PDF Pages", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("PDF Pages", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    hands, img = detectorHand.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands:
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]
        fingers = detectorHand.fingersUp(hand)
        xIndex, yIndex = lmList[8][0], lmList[8][1]

        current_time = time.time()
        if current_time - lastGestureTime > gestureCooldown:
            if cy <= gestureThreshold:
                if fingers == [1, 0, 0, 0, 0]:  # Pinky → Previous
                    print("Previous Page")
                    if pageNumber > 0:
                        pageNumber -= 1
                        imgCurrent = pdf_to_image(pageNumber)
                        imgCurrent = resize_preserve_aspect_ratio(imgCurrent, width, height)
                    lastGestureTime = current_time

                elif fingers == [0, 0, 0, 0, 1]:  # Thumb → Next
                    print("Next Page")
                    if pageNumber < totalPages - 1:
                        pageNumber += 1
                        imgCurrent = pdf_to_image(pageNumber)
                        imgCurrent = resize_preserve_aspect_ratio(imgCurrent, width, height)
                    lastGestureTime = current_time

        # Annotate pointer
        if fingers == [0, 1, 0, 0, 0]:
            cv2.circle(imgCurrent, (xIndex, yIndex), 4, (0, 0, 255), cv2.FILLED)

    cv2.imshow("PDF Pages", imgCurrent)
    cv2.imshow("Camera Feed", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()