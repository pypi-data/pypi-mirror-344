import re
import base64
from io import BytesIO
from matplotlib.figure import Figure

from flask import Flask, Blueprint, render_template, request, render_template_string, send_from_directory
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField 
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField 
from wtforms.validators import InputRequired 
from werkzeug.security import generate_password_hash 

from flask_misaka import Misaka
from ansi2html import Ansi2HTMLConverter

# My modules
import giquant.tsl.gg as tsl_gg
import giquant.tsl.pr as tsl_pr
import giquant.tsl.expr as tsl_expr
import giquant.tsl.sql as tsl_sql
import giquant.tsl.helpers as helpers

from flask import current_app as app


# Helpers
# =======

def myargparse(l, parser):
  args = None
  try:
    args = parser.parse_args(l)
  except:
    print(f'ERROR: invalid arguments! {l}')
  return args


def parse_get_args(request_args, parser):
  d = request_args.to_dict(flat=True)
  l = [ (x,d[x]) for x in d.keys()]
  l = list(sum(l, ()))
  l = list(filter(lambda x: x!='', l))
  return l

def parse_post_args(d_, parser):
  res = [f'$1={app.config["TSLFOLDER"]}', f'--backend={app.config["TSLBACKEND"]}', f'--dbname={app.config["TSLDBNAME"]}']
  for key in d_.keys():
    if key=='csrf_token':
      continue
    elif key[0:3]=='pos':
      res.append(f'${key[3]}={d_[key]}')
    else:
      res.append(f'--{key}={d_[key]}')
  res.sort()
  res = [x[3:] if x[0]=='$' else x for x in res]
  return res

def parse_args(request_, parser):
  # parse multipart/form-data;
  if request_.method=='POST':
    data =  request_.get_data().decode('utf-8')
    content_type =  request_.headers.get('Content-Type')
    boundary = '--' + content_type.split(';')[1].split('=')[1]
    res = {}
    for part in data.split(boundary):
      print(part)
      name = re.findall('name=\"(.*)\"', part)
      if len(name)>0:
        res[name[0]] = ''.join(part.split('\r\n')[3:])
        print(part.split('\r\n'))
    args = parse_post_args(res, parser)
  else:
    args = parse_get_args(request_.args, parser)

  if not parser is None:
    return myargparse(args, parser)
  return args



# Main
# ====

index_page=Blueprint(
  'index_page',
  __name__,
  static_folder='static',
  template_folder='templates',
  url_prefix='/'
)

# Used by tsl.server to register the Blueprint
route = index_page

@index_page.route("/db")
def db():
  import glob
  import tabulate

  res = helpers.get_tables(app.config['TSLFOLDER'], app.config['TSLDBNAME'], app.config['TSLBACKEND'] )

  res = f'<pre>{tabulate.tabulate(res, headers=["File/Table","Size","Date"])}</pre>'
  return render_template('db.html',md_text=res)

# NOTE: Not able to make this work!
  res = list(map(lambda x: (x[0].replace('_',''),x[1],x[2]), res))
  res1 = '\n'.join([f'| {f} | {s} | {d} |' for f,s,d in res ])
  res = f'''
| File/Table  | Size  | Date |
| ----------- | ----- | ---- |
{res1}
'''
  return render_template('db.html',md_text=res)


@index_page.route("/pr", methods=['GET', 'POST'])
def pr_():
  res = None
  parser = tsl_pr.create_args_parser()
  args   = parse_args(request, parser)
  if args is None:
    return 'ERROR: invalid arguments! Check server output for details!'
  else:
    res = tsl_pr.main(args)
    conv = Ansi2HTMLConverter()
    res = conv.convert(res)
  return f'args:{args}<br>{res}'


@index_page.route("/gg", methods=['GET', 'POST'])
def plot():
  parser = tsl_gg.create_args_parser()
  args = parse_args(request, parser)  
  print(args)
  
  if args is None:
    return 'ERROR: invalid arguments! Check server output for details!'

  figs = tsl_gg.main(args)
  res = ''
  for fig in figs:
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    res += f"<br/><img src='data:image/png;base64,{data}'/>"

  return res

@index_page.route("/expr", methods=['GET', 'POST'])
def expr():
  parser = tsl_expr.create_args_parser()
  args = parse_args(request, None)
  args.append(f'--py={app.config["PYFILE"]}')
  args = myargparse(args, parser)
  
  if args is None:
    return 'ERROR: invalid arguments! Check server output for details!'

  res = tsl_expr.main(args)
  return f'{res}<br><a href="/">Home</a>'

@index_page.route("/sql")
def sql():
  res = None

  # Add the folder and dbname arguments that are necessary for sql
  from werkzeug.datastructures import MultiDict
  d = MultiDict()
  d.add(TSLFOLDER,'')
  for key in request.args.keys():
    d.add(key, request.args[key])
  d.add(f'--dbname={app.config["TSLDBNAME"]}','')
  request.args = d

  parser = tsl_sql.create_args_parser()
  args   = parse_args(request, parser)
  if args is None:
    return 'ERROR: invalid arguments! Check server output for details!'
  else:
    outfile = args.outfile
    outpath = f'{app.root_path}/{app.static_url_path}'
    args.outfile = f'{outpath}/{outfile}'
    tsl_sql.main(args)
    return send_from_directory(outpath, f'{outfile}.{args.outformat}', as_attachment=True)

@index_page.route('/', methods=['GET', 'POST']) 
def index(): 
  return render_template('index.html',md_text=app.config['INDEX_PAGE'])
