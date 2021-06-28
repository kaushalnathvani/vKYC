from flask import render_template, Response, request, redirect, url_for
import cv2 as cv
from datetime import datetime
import requests
import db_manager
from models import AgentDetails, Queue
import json


class RegisterServices:
    def __init__(self, app):
        self.app = app
        self.camera = cv.VideoCapture(0)
        self.fourcc = cv.VideoWriter_fourcc(*'XVID')
        # self.fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.fps = self.camera.get(cv.CAP_PROP_FPS)
        self.out = None
        self.open = False
        self.db_manager = db_manager.DBManager()
        # self.scanner = image_crop.Scanner()

        self.app.add_url_rule('/', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed, methods=['GET', 'POST'])
        self.app.add_url_rule('/start_recording', 'start_recording', self.start_recording, methods=['GET', 'POST'])
        self.app.add_url_rule('/stop_recording', 'stop_recording', self.stop_recording, methods=['GET', 'POST'])
        self.app.add_url_rule('/screen_capture', 'screen_capture', self.screen_capture, methods=['GET', 'POST'])
        self.app.add_url_rule('/get_queue', 'get_queue', self.get_queue, methods=['GET', 'POST'])

    def login(self):
        error = None
        loc_info = self.track_ip_and_location()
        session = self.db_manager.get_session()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # enc_password = self.f.encrypt(password.encode())
            # print('enc_password:',enc_password)

            agent_details = session.query(AgentDetails.name).filter(AgentDetails.username == username,
                                                                    AgentDetails.password == password).all()
            if not agent_details:
                error = 'Invalid Credentials. Please try again.'
            elif loc_info.get('country', '') != 'IN':
                error = 'Location outside India not allowed.'
                return render_template('index.html', error=error)
            else:
                return render_template('/video_feed.html', info=loc_info.get('ip'), country=loc_info.get('country', ''))
        return render_template('index.html', error=error)

    def video_feed(self):
        return Response(self.show_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def show_video(self):
        while True:
            success, frame = self.camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv.imencode('.jpg', frame)
                frame2 = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')  # concat frame one by one and show result

    def start_recording(self):
        return Response(self.recorder(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stop_recording(self):
        self.open = False
        print('Saving ...')
        # self.camera.release()
        self.out.release()
        print('Saved ...')
        return ''
        # return Response(self.show_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def recorder(self):
        print('Start recording ...')
        self.open = True
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.out = cv.VideoWriter('media/' + time_now + '_output.avi', self.fourcc, self.fps, (1280, 720))
        while self.open:
            success, v_frame = self.camera.read()  # read the camera frame
            if success:
                self.out.write(v_frame)

            # Record 10 seconds of video
            # if time.time() > timeout:
            #     print('Saving ...')
            #     camera.release()
            #     out.release()

    def screen_capture(self):
        _, p_frame = self.camera.read()
        img_name = 'media/' + str(datetime.now()) + 'snap.jpg'
        cv.imwrite(img_name, p_frame)
        print("{} written!".format(img_name))

        # if success:
        #     _, frame = self.scanner.detect_edge(frame, True)
        #     ret, jpeg = cv.imencode('.jpg', frame)
        #     self.transformed_frame = jpeg.tobytes()
        # else:
        #     return None
        # return self.transformed_frame
        return ''

    def track_ip_and_location(self):
        # Automatically geolocate the connecting IP
        url = 'http://ipinfo.io/json'
        try:
            response = requests.get(url)
            info = response.text
            return json.loads(info)
        except Exception as e:
            print('Error:', e)
            print("Location could not be determined automatically")
            return {}

    def get_queue(self):
        session = self.db_manager.get_session()
        rows = session.query(Queue).order_by(Queue.added_date).all()
        return render_template('queue.html', title='View Submitted KYC', rows=rows)
