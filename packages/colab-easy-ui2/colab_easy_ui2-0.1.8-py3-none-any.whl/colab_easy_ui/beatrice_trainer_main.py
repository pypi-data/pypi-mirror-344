import fire
import time
import functools
import os
from colab_easy_ui.ColabEasyUI import ColabEasyUI
from colab_easy_ui.plugins.unzip_function import unzip
from colab_easy_ui.plugins.json_save_function import json_save
from colab_easy_ui.Functions import JsonApiFunc

def run_server(
    port: int | None = None,
    allow_origins: list[str] = ["*"],
    colab:bool=False,
    upload_dir = "upload",
    upload_title = "Voice(zip)",
    upload_filename = "voice.zip",
    extract_to = "raw_data",
    config_path = "config.json",

):
    # c = ColabEasyUI.get_instance(port=port, allow_origins=allow_origins)
    c = ColabEasyUI(port=port, allow_origins=allow_origins)
    port = c.port
    print(f"port: {port}")

    # ファイルアップローダ
    c.enable_file_uploader(upload_dir, {upload_title: upload_filename})
    c.register_functions(
        [
            JsonApiFunc(
                id="unzip",
                type="progress",
                display_name="unzip",
                method="GET",
                path="/functions_unzip",
                func=functools.partial(unzip, port=port, zip_path=f"{upload_dir}/{upload_filename}", extract_to=extract_to),
            ),
            JsonApiFunc(
                id="json_save",
                type="progress",
                display_name="json_save",
                method="GET",
                path="/functions_json_save",
                func=functools.partial(json_save, port=port, output_path=config_path),
            ),
        ])
    
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    static_files_path = os.path.join(current_dir, "frontend_beatrice_trainer_colab/dist")
    c.mount_static_folder("/front", static_files_path)

    port = c.start()
    print(f"open http://localhost:{port}/front")
    if colab == False:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("サーバーを終了します")
            c.stop()
            print("サーバーを終了しました")

def wrapped_run_server(
    port: int | None = None,
    allow_origins: list[str] = ["*"],
    colab:bool=False,
    upload_dir = "upload",
    upload_title = "Voice(zip)",
    upload_filename = "voice.zip",
    extract_to = "raw_data",
    config_path = "config.json",
):
    """
    run_serverの戻り値であるportを標準出力に出さないようにするためのラッパ。
    """
    run_server(port=port, allow_origins=allow_origins, colab=colab, upload_dir=upload_dir, upload_title=upload_title, upload_filename=upload_filename, extract_to=extract_to, config_path=config_path)
    
def get_html_setup(port: int, device: str):
    """
    htmlを返す。
    """
    return f"""
  <script>var colab_server_port={port}</script>
  <script>var colab_server=1</script>
  <script>var app_mode = "setup"</script>
  <script>var device = "{device}"</script>
  <script defer="defer" src="http://localhost:{port}/front/assets/index.js"></script>
  <div id="root" style="width:100%;height:100%"></div>
  """
def get_html_upload(port: int, language: str):
    """
    htmlを返す。
    """
    return f"""
  <script>var colab_server_port={port}</script>
  <script>var colab_server=1</script>
  <script>var app_mode = "upload"</script>
  <script>var language = "{language}"</script>
  <script defer="defer" src="http://localhost:{port}/front/assets/index.js"></script>
  <div id="root" style="width:100%;height:100%"></div>
  """


