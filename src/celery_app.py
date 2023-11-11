import os

import cv2
from celery import Celery
from celery.result import AsyncResult
from cv2 import dnn_superres

from utils import generate_path

BACKEND = os.getenv("BACKEND", "redis://localhost:6379/1")
BROKER = os.getenv("BROKER", "redis://localhost:6379/2")

my_celery_server = Celery(
    "main_name_celery_server",
    backend=BACKEND,
    broker=BROKER,
    broker_connection_retry_on_startup=True,
)


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=my_celery_server)


@my_celery_server.task()
def upscale(image_name: str, model_name: str = "EDSR_x2.pb") -> str:
    input_path = generate_path("input", image_name)
    output_path = generate_path("output", image_name)
    model_path = generate_path("model", model_name)

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)
    return image_name
