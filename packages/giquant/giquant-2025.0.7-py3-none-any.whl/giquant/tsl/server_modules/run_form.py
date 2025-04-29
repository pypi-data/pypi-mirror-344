from urllib.parse import urlencode

from flask import Flask, Blueprint, render_template, request, render_template_string, send_from_directory, redirect, current_app
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators
from wtforms import StringField, RadioField, SelectField, TextAreaField
from wtforms.validators import InputRequired

from flask import current_app as app

import giquant.tsl.server
import giquant.tsl.helpers as helpers

# Scaffolding
# ===========

run_form=Blueprint(
  'run_form',
  __name__,
  static_folder='static',
  template_folder='templates',
  url_prefix='/run_form'
)

# Used by tsl.server to register the Blueprint
route = run_form

# Form
# =====
#

class RunForm(FlaskForm):
  pos3       = StringField('Output Table', validators=[InputRequired()])
  pos4       = TextAreaField('stmts', validators=[InputRequired()])
  index_type = SelectField('Index', choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly','monthly') ])

@run_form.route('/', methods=['GET','POST'])
def index():
  form = RunForm()
  if form.validate_on_submit():  
    # 307=preserve method=POST
    return redirect('/run_form', code=307)
  tables = helpers.get_tables(app.config['TSLFOLDER'], app.config['TSLDBNAME'], app.config['TSLBACKEND'])
  tables = [x[0] for x in tables]
  scripts = helpers.read_tsl(f'{app.config["TSLSCRIPT"]}.tsl')
  return render_template('run_form.html', form=form, tables=tables, scripts=scripts)

