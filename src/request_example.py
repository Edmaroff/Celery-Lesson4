import time
from datetime import datetime

import requests

from utils import generate_path

# # Получение статуса задачи
# response = requests.get(
#     f"http://127.0.0.1:5000/tasks/8d5e3504-bda5-4935-a71f-9bdeeb6c57f8"
# )

# # Получение обработанного файла
# response = requests.get(f'http://127.0.0.1:5000/processed/lama_300px.png')

# Отправка задачи в Celery
# response = requests.post(
#     "http://127.0.0.1:5000/upscale",
#     files={
#         "image": open("files/test_file/test_1.png", "rb"),
#     },
# )
# print(response.text)


# response = requests.get(
#     f"http://127.0.0.1:5000"
# )
# print(response)

# def main():
#     start_time = datetime.now()
#
#     test_images_names = [
#         "test_1.png",
#         "test_2.jpeg",
#         "test_3.jpg",
#     ]
#     test_images_paths = [generate_path("test", name) for name in test_images_names]
#     finish_statuses = ["SUCCESS", "FAILURE"]
#     tasks_ids = []
#     images_urls = []
#
#     # Отправка задачи в Celery
#     for path in test_images_paths:
#         with open(path, "rb") as file:
#             response = requests.post(
#                 "http://127.0.0.1:5000/upscale",
#                 files={
#                     "image": file,
#                 },
#             )
#             print(response.json())
#             task_id = response.json().get("task_id")
#             tasks_ids.append(task_id)
#
#     # Получение статуса задачи
#     while tasks_ids:
#         time.sleep(5)
#         for task_id in tasks_ids.copy():
#             response = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}")
#             status_task = response.json().get("status")
#             print(f"Задача {task_id} статус: {status_task}")
#             if status_task in finish_statuses:
#                 tasks_ids.remove(task_id)
#                 images_urls.append(response.json().get("image_url"))
#
#     # Получение обработанного файла
#     for image_url in images_urls:
#         response = requests.get(image_url)
#         print(response.status_code)
#
#     end_time = datetime.now()
#     print(f"Время выполнения: {end_time - start_time}")
#
#
# if __name__ == "__main__":
#     main()
