from flask import Flask, jsonify, request
import os
import time
from image_proc import ImageProcess
import json

RECV_FOLDER='FileRecv'


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello,welcome to the edge computing server!'

from flask import make_response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



    
@app.route('/device/request_message', methods=['POST'])
def handle_message():  
    global possibility
    # get dic type data from JSON type
    msg_data=request.json
    print(msg_data)
    relay_msg = {'[Server]:':possibility}
    return jsonify(relay_msg)

@app.route('/device/request_image', methods=['POST'])
def device_request_image():
    global possibility
    """parse file data"""
    image_file = request.files['content']
    file_path=os.path.join(app.root_path,RECV_FOLDER,image_file.filename)
    image_file.save(file_path)
    file_size = os.stat(file_path).st_size
    results,time=ImageProcess(file_path)
    print('file size: {0:.0f} KB'.format(file_size/1024))
    possibility[1]=10
    return jsonify({'proc_results':results,'proc_time':time})
    



if __name__ == '__main__':
    possibility=[1,2,3,4,5,6,7,8,9]
    app.run(debug=True,host='0.0.0.0',port=5000)
    
    while True:
        print(possibility)
        time.sleep(5)
        