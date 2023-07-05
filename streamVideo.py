from flask import Flask, Response
import cv2
import numpy as np
import pyautogui
import time
import utility

FRAME_RATE = 15
IP = utility.get_ip_address()

app = Flask(__name__)

SCREEN_SIZE = (1280,720)
# SCREEN_SIZE = (1920,1080)

def gen_frames():
    while True:
        start_time = time.time()  # Record the start time

        # Capture the screen
        img = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

        # Resize the screenshot to the desired resolution
        img = cv2.resize(img, SCREEN_SIZE)

        # Convert the frame to a JPEG image
        ret, buffer = cv2.imencode('.jpg', img)

        # Yield the image data as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        # Calculate the time elapsed since the start of the loop
        elapsed_time = time.time() - start_time

        # If the elapsed time is less than the desired time per frame, delay the loop
        if elapsed_time < 1 / FRAME_RATE:
            time.sleep(1 / FRAME_RATE - elapsed_time)

@app.route('/')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print(f'Path: http://{IP}:5000')
    app.run(host=IP)




# # using threading
# import threading
# from flask import Flask, Response
# import cv2
# import numpy as np
# import pyautogui
# import time

# FRAME_RATE = 15
# IP = '192.168.1.9'

# app = Flask(__name__)

# SCREEN_SIZE = (1280,720)

# def gen_frames():
#     while True:
#         start_time = time.time()

#         img = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

#         img = cv2.resize(img, SCREEN_SIZE)

#         ret, buffer = cv2.imencode('.jpg', img)

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

#         elapsed_time = time.time() - start_time

#         if elapsed_time < 1 / FRAME_RATE:
#             time.sleep(1 / FRAME_RATE - elapsed_time)

# @app.route('/')
# def video():
#     return Response(gen_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# def start_flask_app():
#     print(f'Path: http://{IP}')
#     app.run(host=IP)

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=start_flask_app)
#     flask_thread.start()
#     flask_thread.join()






