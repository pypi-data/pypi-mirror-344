from flask import Blueprint


# Scaffolding
# ===========

sql_form=Blueprint(
  'sql_form',
  __name__,
  static_folder='static',
  template_folder='templates',
  url_prefix='/sql_form'
)

# Used by tsl.server to register the Blueprint
route = sql_form


# Form
# =====
#
# Generate this type of URL:
# sql?yffut&select(yffut).where(yffut.c.Date%3E20231231)&yffut_&--folder=/home/me/aws-s3/gizur-trade-csv/wide&--backend=duckdb)
#

from urllib.parse import urlencode
from wtforms import Form, BooleanField, StringField, validators

from flask import Flask, render_template, request, render_template_string, send_from_directory, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField
from wtforms.validators import InputRequired

class SQLForm(FlaskForm):
  table    = StringField('Table', validators=[InputRequired()])
  sql      = TextAreaField('sql', validators=[InputRequired()])


@sql_form.route('/', methods=['GET', 'POST'])
def index():
  form = SQLForm()
  if form.validate_on_submit():
    url = f'/sql?{form.table.data}&{form.table.data}_&{form.sql.data}'
    print(url)
#    return render_template_string(url)
    return redirect(url)
  return render_template('sql_form.html', form=form)

