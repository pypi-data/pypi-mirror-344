import json
import uuid
import requests

def submit_asr_task(app_id:str, app_token :str, audio_url:str ):
    submit_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
    task_id = str(uuid.uuid4())
    headers = {
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": app_token,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": task_id,
        "X-Api-Sequence": "-1"
    }
    request = {
        "user": {
            "uid": "fake_uid"
        },
        "audio": {
            "url": audio_url,
            "format": "mp3",
            "codec": "raw",
            "rate": 16000,
            "bits": 16,
            "channel": 1
        },
        "request": {
            "model_name": "bigmodel",
            # "enable_itn": True,
            # "enable_punc": True,
            # "enable_ddc": True,
            "show_utterances": True,
            # "enable_channel_split": True,
            # "vad_segment": True,
            # "enable_speaker_info": True,
            "corpus": {
                # "boosting_table_name": "test",
                "correct_table_name": "",
                "context": ""
            }
        }
    }
    # print(f'Submit task id: {task_id}')
    response = requests.post(submit_url, data=json.dumps(request), headers=headers)
    if 'X-Api-Status-Code' in response.headers and response.headers["X-Api-Status-Code"] == "20000000":
        # print(f'Submit task response header X-Api-Status-Code: {response.headers["X-Api-Status-Code"]}')
        # print(f'Submit task response header X-Api-Message: {response.headers["X-Api-Message"]}')
        x_tt_log_id = response.headers.get("X-Tt-Logid", "")
        # print(f'Submit task response header X-Tt-Logid: {response.headers["X-Tt-Logid"]}\n')
        return task_id, x_tt_log_id
    else:
        # print(f'Submit task failed and the response headers are: {response.headers}')
        exit(1)
    # return task_id
def query_asr_task(app_id, token ,task_id, x_tt_log_id):
    query_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

    headers = {
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": token,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": task_id,
        "X-Tt-Logid": x_tt_log_id  # 固定传递 x-tt-logid
    }

    response = requests.post(query_url, json.dumps({}), headers=headers)

    if 'X-Api-Status-Code' not in response.headers:
        exit(1)

    return response
