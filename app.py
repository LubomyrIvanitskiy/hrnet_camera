from flask_ngrok import run_with_ngrok

import os
print(os.getcwd())
from sys import stdout
from image_processor import ImageProcessor
import logging
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from camera import Camera


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['PORT'] = 8050
socketio = SocketIO(app)
# run_with_ngrok(app)   #starts ngrok when the app is run
camera = Camera(ImageProcessor())


@socketio.on('input image', namespace='/test')
def test_message(input):
    print("test_message")
    input = input.split(",")[1]
    camera.enqueue_input(input)


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")
    print("client connected")


@app.route('/')
def index():
    """Video streaming home page."""
    print("index")
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    print("starting to generate frames!")
    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        print("getframe")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    print("video_feed")
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app)
    # app.run()
