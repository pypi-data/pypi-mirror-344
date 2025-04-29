#
# 241212, Jonas C.
#
# Form to us tsl.expr
# usage: expr.py [-h] [--parse-only | --no-parse-only] [--debug | --no-debug] [--py PY] [--yaml YAML] [--backend BACKEND] [--dbname DBNAME]
#                folder infile outfile stmts      
#

from flask import Blueprint
from flask import current_app as app

import giquant.tsl.helpers as helpers


# Scaffolding
# ===========

pr_form=Blueprint(
  'pr_form',
  __name__,
  static_folder='static',
  template_folder='templates',
  url_prefix='/pr_form'
)

# Used by tsl.server to register the Blueprint
route = pr_form


# Form
# =====
#

from urllib.parse import urlencode
from wtforms import Form, BooleanField, StringField, validators

from flask import Flask, render_template, request, render_template_string, send_from_directory, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField
from wtforms.validators import InputRequired

class PrForm(FlaskForm):
  pos2 = StringField('Input file', validators=[InputRequired()])


@pr_form.route('/', methods=['GET','POST'])
def index():
  form = PrForm()
  if form.validate_on_submit():
    # 307=preserve method=POST
    return redirect('/pr', code=307)

  tables = helpers.get_tables(app.config['TSLFOLDER'], app.config['TSLDBNAME'], app.config['TSLBACKEND'])
  tables = [x[0] for x in tables]
  return render_template('pr_form.html', form=form, tables=tables)

