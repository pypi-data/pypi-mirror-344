import os
import json
from typing import Callable
import uuid
from fastapi import BackgroundTasks
import requests
import functools
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from colab_easy_ui.Functions import ProgressTaskStatus, ProgressFunctionCallResponse, JsonApiTaskStatus, ProgressTaskProcessStatus


def exec_json_save(_callback: Callable[[JsonApiTaskStatus, ProgressTaskStatus], None], json_data: dict, output_path: str):
    progresses = ProgressTaskStatus(processStatus={})

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    progresses.processStatus["save"] = ProgressTaskProcessStatus(
        display_name="Save JSON",
        n=0,
        total=1,
        status="RUNNING",
        unit="",
    )

    try:
        # JSONファイルを保存
        print(f"json_save: {json_data}, {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
        progresses.processStatus["save"].n = 1
        progresses.processStatus["save"].total = 1
        progresses.processStatus["save"].status = "DONE"
        _callback("DONE", progresses)
    except Exception as e:
        print(f"json_save!!!!!!!!!!!!!!!!!!!!!!: {e}")
        progresses.processStatus["save"].status = "ERROR"
        _callback("ERROR", progresses)
        raise e


def json_save_callback(status: JsonApiTaskStatus, allStatus: ProgressTaskStatus, port: int, uuid_str: str):
    data = allStatus.model_dump_json()
    requests.get(f"http://localhost:{port}/functions_set_task_status?task_id={uuid_str}&status={status}&data={data}")


def json_save_function(port: int, uuid_str: str, json_data: dict, output_path: str):
    json_save_callback_fixed = functools.partial(json_save_callback, port=port, uuid_str=uuid_str)
    exec_json_save(json_save_callback_fixed, json_data, output_path)


def json_save(port: int, json_data: str, output_path: str, background_tasks: BackgroundTasks):
    print(f"json_save: {json_data}, {output_path}")
    json_data = json.loads(json_data)
    print(f"json_save: {json_data}, {output_path}")
    # UUIDを作成
    uuid_str = str(uuid.uuid4())

    background_tasks.add_task(json_save_function, port, uuid_str, json_data, output_path)

    try:
        data = ProgressFunctionCallResponse(
            status="OK",
            uuid=uuid_str,
            message="",
        )
        json_compatible_item_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_item_data)
    except Exception as e:
        data = ProgressFunctionCallResponse(
            status="NG",
            uuid="",
            message=str(e),
        )
        return JSONResponse(content=json_compatible_item_data) 