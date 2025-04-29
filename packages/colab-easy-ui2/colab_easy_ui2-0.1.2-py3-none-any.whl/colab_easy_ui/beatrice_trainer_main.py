import fire
import time
import functools
import os
from colab_easy_ui.ColabEasyUI import ColabEasyUI
from colab_easy_ui.plugins.unzip_function import unzip
from colab_easy_ui.plugins.json_save_function import json_save
from colab_easy_ui.Functions import JsonApiFunc

def run_server(
    ipython=None,
    logfile=None,
    port: int | None = None,
    allow_origins: list[str] = ["*"],
    # display=None,
    # download_func=None,
):
    c = ColabEasyUI.get_instance(port=port, allow_origins=allow_origins)
    port = c.port
    print(f"port: {port}")

    # ファイルアップローダ
    c.enable_file_uploader("upload", {"Voice(zip)": "voice.zip"})
    c.register_functions(
        [
            JsonApiFunc(
                id="unzip",
                type="progress",
                display_name="unzip",
                method="GET",
                path="/functions_unzip",
                func=functools.partial(unzip, port=port, zip_path="upload/voice.zip", extract_to="raw_data"),
            ),
            JsonApiFunc(
                id="json_save",
                type="progress",
                display_name="json_save",
                method="GET",
                path="/functions_json_save",
                func=functools.partial(json_save, port=port, output_path="./config.json"),
            ),
        ])
    
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    static_files_path = os.path.join(current_dir, "frontend/dist")
    c.mount_static_folder("/front", static_files_path)

    port = c.start()
    print(f"open http://localhost:{port}/front")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("サーバーを終了します")
        c.stop()
        print("サーバーを終了しました")

def wrapped_run_server(
    # port: int,
    ipython=None,
    logfile=None,
    port: int | None = None,
    allow_origins: list[str] = ["*"],
):
    """
    run_serverの戻り値であるportを標準出力に出さないようにするためのラッパ。
    """
    run_server(ipython, logfile, port=port, allow_origins=allow_origins)
    

def main():
    fire.Fire(wrapped_run_server)

if __name__ == "__main__":
    main()
