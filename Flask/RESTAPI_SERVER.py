from flask import Flask, jsonify, request
import os
from image_proc import ImageProcess

app = Flask(__name__)

weathers = [
{
'id': 110000,
'city': 'BeiJing',
'description': 'rainy',
'high_template': '15',
'low_template': '3',
},
{
'id': 310000,
'city': 'ShangHai',
'description': 'sunny',
'high_template': '20',
'low_template': '6',
},
{
'id': 440100,
'city': 'GuangZhou',
'description': 'cloudy',
'high_template': '25',
'low_template': '8',
}
]

@app.route('/')
def index():
    return 'Hello,welcome to query the weathers!'

@app.route('/weather/api/weathers', methods=['GET'])
def get_weathers():
    return jsonify({'weathers': weathers})

@app.route('/device/request_image', methods=['POST'])
def device_request_image():
    """parse file data"""
    image_file = request.files['image_data']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path=os.path.join(BASE_DIR,'test.jpg')
    image_file.save(file_path)
    file_size = os.stat(file_path).st_size
    results,time=ImageProcess(file_path)
    print('file size: {0:.0f} KB'.format(file_size/1024))
    return jsonify({'proc_results':results,'proc_time':time})


from flask import abort
@app.route('/weather/api/weathers/<int:city_id>', methods=['GET'])
def get_city_weather_id(city_id):
    city = list(filter(lambda t: t['id'] == city_id, weathers))
    if len(city) == 0:
        abort(404)
    return jsonify({'weather': city[0]})

@app.route('/weather/api/weathers/<string:city_list>', methods=['GET'])
def get_city_weather(city_list):
    city = list(filter(lambda t: t['city'] == city_list, weathers))
    if len(city) == 0:
        abort(404)
    return jsonify({'weather': city[0]})

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    
    app.run(debug=True,host='0.0.0.0',port=5000)