from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify

from src.modules.webui import utils
from src.modules.webui.ui.forms import CycleConfigForm, AddSiteForm

from src.measure import measurement_cycle
from src.modules.webui.celery import task_queue

from src.modules.config import Config
CONFIG = Config("config.ini")

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
    site_list = utils.get_site_list()

    if request.method == 'POST':
        config = {
            "frequency": form.frequency.data,
            "hr": form.hr.data,
            "min": form.min.data,
            "sec": form.sec.data,
            "site_id": form.site_id.data,
        }
            
        for data in config:
            if config[data] is None:
                flash("Required Field Not Completed!", "alert-warning")
                return render_template("config.html", form=form, site_list=site_list)

        task = measurement_cycle.delay(config["site_id"], config["hr"], config["min"], config["sec"], config["frequency"])
        async_result = task_queue.AsyncResult(id=task.task_id, app=task_queue)
        
        flash("Success! Configuration sent to box. Measurements Starting...", "alert-success")
        return redirect("/live/")

    return render_template("config.html", form=form, site_list=site_list)

@routes.route("/data/")
def data():
    files = utils.get_files_in_dir(CONFIG.USB_DIR)
    return render_template("data.html", file_list=files)

@routes.route("/download/")
def download_root():
    return render_template("404.html"), 404

@routes.route("/download/<string:file_name>/")
def download(file_name):
    return send_from_directory(CONFIG.USB_DIR, filename=file_name)

@routes.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)

@routes.route("/site/add/", methods=["GET", "POST"])
def add_site():
    form = AddSiteForm()
    site_list = utils.get_site_list()

    if request.method == 'POST':
        site = {
            "name": form.name.data,
            "latitude": form.latitude.data,
            "longitude": form.longitude.data,
            "depth": form.depth.data
        }
            
        for data in site:
            if site[data] is None:
                flash("Required Field Not Completed!", "alert-warning")
                return render_template("add_site.html", form=form, site_list=site_list)

        utils.add_site(site["name"], site["latitude"], site["longitude"], site["depth"])
        
        flash("Success! Site Added to Database.", "alert-success")
        return redirect("/site/add/")

    return render_template("add_site.html", form=form, site_list=site_list)

@routes.route("/api/gps/")
def read_gps():
    gps_results = utils.read_gps()
    return jsonify(gps_results)


# @routes.route("/old_api/")
# def old_api():
#     data = utils.old_get_live_data()
#     return jsonify(data)