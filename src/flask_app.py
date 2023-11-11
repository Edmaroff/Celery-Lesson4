import flask
from flask import jsonify, request, send_file
from flask.views import MethodView

from celery_app import get_task, my_celery_server, upscale
from utils import HttpError, generate_path

app = flask.Flask("my_flask_app")
my_celery_server.conf.update(app.config)


class ContextTask(my_celery_server.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


my_celery_server.Task = ContextTask


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


class UpscaleView(MethodView):
    """
    POST /upscale. Принимает файл с изображением и возвращает id задачи
    """

    def post(self):
        image_name = self.save_image("image")
        task = upscale.delay(image_name)
        return jsonify(
            {"task_id": task.id, "image_name": image_name, "task_status": task.status}
        )

    def save_image(self, field):
        image = request.files.get(field)

        try:
            filename = image.filename
        except AttributeError:
            raise HttpError(400, "No image in request")

        input_path = generate_path("input", filename)
        image.save(input_path)

        return filename


class TasksView(MethodView):
    """
    GET /tasks/<task_id> возвращает статус задачи и ссылку на обработанный файл,
     если задача выполнена
    """

    def get(self, task_id):
        task = get_task(task_id)
        result = {"status": task.status}
        if task.status == "SUCCESS":
            result["image_url"] = f"{request.host_url}processed/{task.result}"
        elif task.status == "FAILURE":
            raise HttpError(409, "Failure image processing")

        return jsonify(result)


class ProcessedView(MethodView):
    """
    GET /processed/{file} возвращает обработанный файл
    """

    def get(self, filename):
        output_path = generate_path("output", filename)
        return send_file(output_path)


upscale_view = UpscaleView.as_view("upscale_view")
tasks_view = TasksView.as_view("tasks_view")
processed_view = ProcessedView.as_view("processed_view")

app.add_url_rule("/upscale", view_func=upscale_view, methods=["POST"])

app.add_url_rule("/tasks/<string:task_id>", view_func=tasks_view, methods=["GET"])

app.add_url_rule(
    "/processed/<string:filename>", view_func=processed_view, methods=["GET"]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
