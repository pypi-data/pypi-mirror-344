#
# 241212, Jonas C.
#
# Form to us tsl.expr
# usage: expr.py [-h] [--parse-only | --no-parse-only] [--debug | --no-debug] [--py PY] [--yaml YAML] [--backend BACKEND] [--dbname DBNAME]
#                folder infile outfile stmts      
#

from flask import Blueprint
from flask import current_app


# Scaffolding
# ===========

expr_form=Blueprint(
  'expr_form',
  __name__,
  static_folder='static',
  template_folder='templates',
  url_prefix='/expr_form'
)

# Used by tsl.server to register the Blueprint
route = expr_form


# Form
# =====
#

from urllib.parse import urlencode
from wtforms import Form, BooleanField, StringField, validators

from flask import Flask, render_template, request, render_template_string, send_from_directory, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField
from wtforms.validators import InputRequired

class ExprForm(FlaskForm):
  pos2 = StringField('Input file', validators=[InputRequired()])
  pos3 = StringField('Output file', validators=[InputRequired()])
  pos4 = TextAreaField('Statements', validators=[InputRequired()])


@expr_form.route('/', methods=['GET','POST'])
def index():
  form = ExprForm()
  if form.validate_on_submit():
    # 307=preserve method=POST
    return redirect('/expr', code=307)
  return render_template('expr_form.html', form=form)

