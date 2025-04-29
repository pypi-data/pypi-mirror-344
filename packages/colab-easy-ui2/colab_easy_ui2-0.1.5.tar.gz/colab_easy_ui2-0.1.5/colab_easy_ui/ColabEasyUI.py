from typing import Callable
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter

# from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

from colab_easy_ui.EasyFileUploaderInternal import EasyFileUploader
import uvicorn
import threading
import nest_asyncio
import portpicker
# from colab_easy_ui.ColabInternalFetcher import ColabInternalFetcher
from colab_easy_ui.Functions import Functions, JsonApiFunc

import logging
from colab_easy_ui.const import LOG_FILE, LOGGER_NAME
from colab_easy_ui.logger import setup_logger

setup_logger(LOGGER_NAME, LOG_FILE)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.getLogger(LOGGER_NAME).info(f"Validation error occurred: {exc}")
    
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": (await request.body()).decode(),
        })
    )


async def log_request_middleware(request: Request, call_next):
    logging.getLogger(LOGGER_NAME).info(f"request: {request.url}")
    response = await call_next(request)
    return response


class ColabEasyUI(FastAPI):
    _instance = None
    port = 0
    server_thread = None

    @classmethod
    def get_instance(
        cls,
        port: int | None = None,
        allow_origins: list[str] = ["*"],
    ):
        if cls._instance is None:
            app_fastapi = ColabEasyUI(port=port, allow_origins=allow_origins)
            cls._instance = app_fastapi
            return cls._instance

        return cls._instance

    def __init__(self, port: int | None = None, allow_origins: list[str] = ["*"]):
        super().__init__(
            default_response_class=JSONResponse,
        )
        
        # ログ記録用ミドルウェアを追加
        self.middleware("http")(log_request_middleware)
        
        # バリデーションエラーのハンドラーを登録
        self.add_exception_handler(RequestValidationError, validation_exception_handler)
        
        if port is not None:
            self.port = port
        else:
            self.port = portpicker.pick_unused_port()

    def _run_server(self, port: int, host: str):

        config = uvicorn.Config(self, host=host, port=port, log_level="critical")
        self.server = uvicorn.Server(config)
        self.server.run()   # ブロッキング        

    def start(self, host: str = "127.0.0.1"):

        logging.getLogger(LOGGER_NAME).info(f"-----------------------------------------------")    
        logging.getLogger(LOGGER_NAME).info(f"Starting ColabEasyUI version start: {self.port}")    
        logging.getLogger(LOGGER_NAME).info(f"-----------------------------------------------")    

        nest_asyncio.apply()
        self.server_thread = threading.Thread(target=self._run_server, args=(self.port, host))
        self.server_thread.start()
        return self.port

    def stop(self):
        if self.server and self.server.should_exit is False:
            self.server.should_exit = True  # サーバーに終了要求を出す


        if self.server_thread:
            self.server_thread.join()
            self.server_thread = None

    def mount_static_folder(self, path: str, real_path: str):
        self.mount(
            path,
            StaticFiles(directory=real_path, html=True),
            name="static",
        )

    def enable_file_uploader(self, upload_dir: str, allowed_files: dict[str, str] | None = None):
        self.fileUploader = EasyFileUploader(upload_dir)
        self.fileUploader.set_allowed_filenames(allowed_files)
        self.include_router(self.fileUploader.router)

    # def enable_colab_internal_fetcher(
    #     self,
    #     project_dir: str,
    #     ipython=None,
    #     logfile=None,
    # ):
    #     from fastapi import APIRouter

    #     self.colabInternalFetcher = ColabInternalFetcher("trainer", ipython, logfile)

    #     router = APIRouter()
    #     router.add_api_route("/internal_start_tb", self.colabInternalFetcher.start_tensorboard, methods=["GET"])
    #     router.add_api_route("/internal_runs", self.colabInternalFetcher.get_runs, methods=["GET"])
    #     router.add_api_route("/internal_scalars_tags", self.colabInternalFetcher.get_scalars_tags, methods=["GET"])
    #     router.add_api_route("/internal_scalars_scalars", self.colabInternalFetcher.get_scalars_scalars, methods=["GET"])
    #     router.add_api_route("/internal_scalars_multirun", self.colabInternalFetcher.get_scalars_scalars, methods=["GET"])
    #     router.add_api_route("/internal_images_tags", self.colabInternalFetcher.get_images_tags, methods=["GET"])
    #     router.add_api_route("/internal_images_images", self.colabInternalFetcher.get_images_images, methods=["GET"])
    #     router.add_api_route("/internal_images_individualImage", self.colabInternalFetcher.get_images_individualImage, methods=["GET"])
    #     router.add_api_route("/internal_audio_tags", self.colabInternalFetcher.get_audio_tags, methods=["GET"])
    #     router.add_api_route("/internal_audio_audio", self.colabInternalFetcher.get_audio_audio, methods=["GET"])
    #     router.add_api_route("/internal_audio_individualAudio", self.colabInternalFetcher.get_audio_individualAudio, methods=["GET"])
    #     self.include_router(router)

    def register_functions(self, funcs: list[JsonApiFunc]):
        functions = Functions()
        functions.register_functions(funcs)
        self.include_router(functions.router)

