from flask import Blueprint
from flask import current_app

# Scaffolding
# ===========

gg_form=Blueprint(
  'gg_form',
  __name__,
  static_folder='static',
  template_folder='templates',
  url_prefix='/gg_form'
)

# Used by tsl.server to register the Blueprint
route = gg_form


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

class GGForm(FlaskForm):
  pos2      = StringField('Table', validators=[InputRequired()])
  index_type = RadioField('Index', choices=[('daily', 'daily'), ('weekly', 'weekly'), ('monthly','monthly') ])
  pos3     = TextAreaField('ggstmt', validators=[InputRequired()])


@gg_form.route('/', methods=['GET','POST'])
def index():
  form = GGForm()
  if form.validate_on_submit():
    
#    return render_template_string(url)
    # 307=preserve method=POST
    return redirect('/gg', code=307)
  return render_template('gg_form.html', form=form)

