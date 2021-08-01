import json

import simpleaudio as sa
from flask import request, jsonify, Flask

from jarvis.utils import config_utils

app = Flask(__name__)


@app.route("/play_raw_audio", methods=['POST'])
def play_raw_audio():
    play_obj = sa.play_buffer(audio_data=request.data, num_channels=1, bytes_per_sample=2, sample_rate=16000)

    play_obj.wait_done()
    return jsonify("OK")


def get_data_in_request(flask_request):
    data_str = str(flask_request.data.decode('utf8')).replace('"', '\"').replace("\'", "'")

    # if no data return an empty json to avoid error with json.loads below
    if not data_str:
        return {}

    data_json = json.loads(data_str)

    if not isinstance(data_json, dict):
        data_json = json.loads(data_json)

    return data_json


def start_server():
    app.config['JSON_AS_ASCII'] = False
    app.run(port=config_utils.get_in_config("PORT"), debug=False, host='0.0.0.0', threaded=True)
