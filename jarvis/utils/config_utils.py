import json
import os

path = os.getcwd() + "/jarvis"


def get_in_config(name):
    config_json = json.load(open(path + "/config/config.json", encoding='utf-8', mode='r'))
    if name in config_json:
        if isinstance(config_json.get(name), str):
            if "!secret" in config_json.get(name):
                # secret_name = config_json.get(name).removeprefix('!secret ')
                secret_name = config_json.get(name).replace('!secret ', '')
                return get_in_secret(secret_name)
            else:
                return config_json.get(name)
        else:
            return config_json.get(name)
    else:
        return None


def get_in_secret(secret_name):
    secrets_json = json.load(open(path + "/config/secrets.json", encoding='utf-8', mode='r'))

    if secret_name in secrets_json:
        return secrets_json.get(secret_name)
    else:
        return None
