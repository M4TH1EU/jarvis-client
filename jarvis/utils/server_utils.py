import requests
from requests.structures import CaseInsensitiveDict


def send_record_to_server(frame_data):
    # TODO: use config or even ping to find the server on local network ?
    url_service = "http://192.168.1.12:5000" + "/process_audio_request"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/xml; charset=utf8"
    # headers["Authorization"] = config_utils.get_in_config("API_KEY")

    response = requests.post(url_service,
                             headers=headers,
                             data=frame_data)

    print(response.content)
