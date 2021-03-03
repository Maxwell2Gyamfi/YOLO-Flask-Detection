from flask import Flask
from flask import send_file, render_template, Response, request, send_from_directory, url_for, session, flash, redirect
import cv2
import json
import numpy as np
from PIL import Image
from io import BytesIO
from base64 import b64decode
from detection import YoloDetection
camera = cv2.VideoCapture(0)

yolo = YoloDetection()

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def stringToRGB(base64_string):
    imagestr = base64_string
    im = Image.open(BytesIO(b64decode(imagestr.split(',')[1])))
    im.save("image.png")
    return im


def upload_file():
    if request.method == 'POST':
        print(request.json)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html', msg='')


@app.route("/runDetection", methods=['GET', 'POST'])
def runDetection():
    if request.method == "POST":
        stringToRGB(request.json["src"])
        if request.json["class"] == "all":
            total = yolo.detectAll()
        else:
            total = yolo.detectSpecific(request.json["class"])

        return json.dumps({'success': True, 'total': total}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route("/setConfidence", methods=["GET", "POST"])
def setConfidence():
    if request.method == "POST":
        global yolo
        confidence = request.json
        yolo.CONFIDENCE_THRESHOLD = int(confidence)/100
        print(yolo.CONFIDENCE_THRESHOLD)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = yolo.detectVideo(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
