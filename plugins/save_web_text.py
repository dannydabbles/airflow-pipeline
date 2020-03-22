# This is the class you derive to create a plugin
import requests
import json

from flask_appbuilder import BaseView as AppBuilderBaseView

from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint, redirect, request
from flask_appbuilder import expose
from flask_appbuilder import has_access
from flask_admin.base import MenuLink

import airflow
from airflow.models import DagModel, DagRun
from airflow import jobs, models, settings
from airflow.utils import timezone
from airflow.utils.state import State
from airflow.www import utils as wwwutils
from airflow import configuration as conf

# Creating a flask admin BaseView
class SaveWebText(AppBuilderBaseView):
    @expose('/')
    def list(self):
        return self.render_template("main.html", content="Hello galaxy!")

bp = Blueprint(
    "save_web_text", __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/save_web_text')


v_appbuilder_view = SaveWebText()
v_appbuilder_package = {"name": "Save Web Text Form",
                        "category": "Save Web Text",
                        "view": v_appbuilder_view}


# Defining the plugin class
class AirflowSaveWebText(AirflowPlugin):
    name = "save_web_text"
    appbuilder_views = [v_appbuilder_package]
    flask_blueprints = [bp]
