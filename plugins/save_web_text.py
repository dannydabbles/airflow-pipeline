# This is the class you derive to create a plugin
import requests
import json

from flask_appbuilder import BaseView as AppBuilderBaseView

from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint, redirect, request, flash
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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SaveWebTextForm(FlaskForm):
    url = StringField('URL to process', validators=[DataRequired()])
    submit = SubmitField('Save web text')


# Creating a flask admin BaseView
class SaveWebText(AppBuilderBaseView):
    @expose('/', methods=['GET', 'POST'])
    def list(self):
        form = SaveWebTextForm()
        if form.validate_on_submit():
            # TODO: Trigger pipeline here
            flash('Processing URL: {}'.format(
                form.url.data))
        return self.render_template('main.html', form=form)

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
