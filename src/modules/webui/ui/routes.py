from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify

from src.modules.webui import utils
from src.modules.webui.ui.forms import CycleConfigForm

from src.measure import measurement_cycle
from src.modules.webui.celery import task_queue

routes = Blueprint("routes", __name__)

@routes.route('/')
def index():
    return render_template("index.html")

@routes.route("/live/")
def live():
    return render_template("live.html")

@routes.route("/config/", methods=["GET", "POST"])
def config():
    form = CycleConfigForm()

    if request.method == 'POST' and form.validate():
        config = {
            "sample_frequency": form.frequency.data,
            "duration": form.duration.data,
        }

        task = measurement_cycle.delay(config["duration"], config["sample_frequency"])
        async_result = task_queue.AsyncResult(id=task.task_id, app=task_queue)
        
        flash("Success! Configuration sent to box. Measurements Starting...", "alert-success")
        return redirect("/live/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("config.html", form=form)

@routes.route("/data/")
def data():
    files = utils.get_files_in_dir("/")
    return render_template("data.html", file_list=files)

@routes.route("/download/")
def download_root():
    return render_template("404.html"), 404

@routes.route("/download/<string:file_name>/")
def download(file_name):
    return send_from_directory("/", filename=file_name)

@routes.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)

@routes.route("/old_api/")
def old_api():
    data = utils.old_get_live_data()
    return jsonify(data)