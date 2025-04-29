import sys
import pprint
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from lark import Lark, Tree, Token

from giquant.tsl.helpers import *


# TODO: stat, sfunc and tfunc currently allow any functions (using the notation Ffunction_name.
#       Implement the functions actually used in the grammar at some point!
# NOTE: The geoms: line, interval and point are mapped to lines, histogram and scatter plots.
# TODO: guides, ie. labels, legends, etc. are not implemed in the grammer yet. Aestithics will
#       be implemented here.
#
grammar = '''?stmts: stmt ";"
                  | stmt ";" stmts       -> seq

             ?stmt: data                 -> data
                 |  trans                -> trans
                 |  element              -> element
                 |  guide                -> guide

             ?data: "levels" "=" variable ("," variable)*    -> levels

             ?trans: variable "=" tfunc "(" variable ")"     -> trans_

             ?element: geom "(" gargs ")"                    -> element_

             !geom: "line" | "interval" | "point"            -> geom

             ?gargs: garg ( "," garg )*                      -> gargs

             !garg: ("pos"|"aes") "(" paargs ")"             -> pos_aes

             !paargs: dim "=" paargv ("," dim "=" paargv)*   -> paargs

             !paargv: stat "(" sargv ")"                     -> paargv

             !sargv: sfunc "(" sargv ")"                     -> sargv
                   | variable

             ?guide: STRING

             stat:  func
             sfunc: func
             tfunc: func
             dim:      "D" /\w+/                             -> dim
             variable: "V"  /\w+/                            -> variable
             func:     "F" (/\w+/ "."*)+                     -> func

             %import common.SIGNED_NUMBER -> NUMBER
             %import common.ESCAPED_STRING -> STRING
             %import common.WS
             %ignore WS
         '''

desc_ = f"""
Create plots using a grammar inspired by Wilksinsons Grammar For Graphics.

BNF (used by Lark)
------------------

            {grammar}

Example 'levels = Vticker , Vgroup , Vvar; line(pos(Dx=FI(VDate), Dy=FI(VNet)), aes(Dcolor=FI(Vgroup)));'

         levels are used to give names to the column structure. It must always have one 
         (and only one) `var` value which holds the actual values of the column.
         An example is: 6E_Comm_Net -> ticker=6E, group=Comm, var=the values of the Net column
         The index of the data is typically used for the x-axis using its name (Date, YearWeek etc.).

"""

d_ = {
  'data'    :  {},
  'trans'   :  {},
  'elements' : [],
  'guide'   :  {},
}

curr_element = None
curr_posaes = None
curr_paargv = None

class Paarg:
  def __init__(self, dim_, val_):
    self.dim = dim_
    self.val = val_
  def __repr__(self):
    return f'Paarg(dim={self.dim},val={self.val})'

class PosAes:
  def __init__(self):
    self.type_ = ''
    self.args = []
    
  def __repr__(self):
    res = ''
    for arg in self.args:
      res += f'\n\t\t\t{str(arg)},'
    return f'\n\t\tPosAes(type_={self.type_},\n\t\t\targs=[{res}])'

class Element:
  def __init__(self):
    self.geom = ''
    self.args = []
  def __repr__(self):
    res = ''
    for arg in self.args:
      res += str(arg) + ','
    return f'Element(geom={self.geom},\n\targs=[{res}])'

def visit(t_):
  global curr_element, curr_posaes, curr_paargv, d_
  if isinstance(t_, Tree):
    if t_.data=='seq':
      for x in t_.children:
        visit(x)
        
    if t_.data=='data':
      visit(t_.children[0])
      
    if t_.data=='levels':
      res = []
      for child in t_.children:
        assert child.data=='variable'
        res.append(str(child.children[0]))
      d_['data']['levels'] = res
      
    if t_.data=='element':
      assert t_.children[0].data=='element_'
      curr_element = Element()
      d_['elements'].append(curr_element)
      for child in t_.children[0].children:
        visit(child)
      
    if t_.data=='geom':
      assert len(t_.children)==1
      curr_element.geom = str(t_.children[0])

    if t_.data=='gargs':
      for child in t_.children:
        visit(child)

    # ("pos"|"aes") "(" paargs ")"
    if t_.data=='pos_aes':
      ch = t_.children
      assert ch[0] in ['pos','aes'] and ch[1]=='(' and ch[2].data=='paargs' and ch[3]==')'
      curr_posaes = PosAes()
      curr_posaes.type_ = str(ch[0])
      curr_element.args.append(curr_posaes)
      visit(ch[2])
        
    # paargs: dim "=" paargv ("," dim "=" paargv)* 
    if t_.data=='paargs':
      ch = t_.children
      i = 0
      while i < len(ch):
        assert ch[i].data=='dim' and str(ch[i+1])=='=' and ch[i+2].data=='paargv'
        curr_paargv = []
        visit(ch[i+2])
        curr_posaes.args.append(Paarg(str(ch[i].children[0]), curr_paargv))
        i += 4
        
    if t_.data=='paargv':
      ch = t_.children
      assert ch[0].data=='stat' and str(ch[1])=='(' and ch[2].data=='sargv' and str(ch[3])==')'
      visit(ch[0].children[0])
      visit(ch[2].children[0])

    if t_.data=='func':
      curr_paargv.append(f'F{str(t_.children[0])}')

    if t_.data=='variable':
      curr_paargv.append(f'V{str(t_.children[0])}')

  elif isinstance(t_, Token) and t_.type=='STRING':
    print('ERROR Found STRING')
    sys.exit(1)
    
  elif isinstance(t_, Token):
    print('ERROR FOUND', Token, t_)
    sys.exit(1)

  elif t_ is None:
    print('ERROR FOUND None')    
    sys.exit(1)
    return
    
  else:
    print(f'Unknown - tree:{t_}')
    sys.exit(1)


def read_data(args):
  df = dal_read_df(args.folder, args.table, args.backend, args.dbname)

  if args.index_type=='weekly':
    print('Using YearWeek as index')
    df['Date']  = df.index.map(lambda x: int2dt(week2date(x)))
    df = df.set_index('Date')
  elif args.index_type=='monthly':
    print('Using YearMonth as index')
    df['Date']  = df.index.map(lambda x: int2dt(month2date(x)))
    #df.index = df.Date
    df = df.set_index('Date')
  else:
    df.index = pd.to_datetime(df.index, format='%Y%m%d') #, errors='ignore')

  return df            #.reset_index()

def create_levels(df_, levels_):
  df_ = df_.reset_index()
  df_ = pd.melt(df_, id_vars=['Date'], var_name='Variable0')
  df_levels = df_.Variable0.str.split('_', n=len(levels_)-1, expand=True)
  df_levels.columns = levels_
  df_ = pd.concat([df_,df_levels], axis=1)
  df_ = df_.dropna()  
  df_ = df_.pivot(index=['Date']+levels_[:-1], columns=[levels_[-1]], values='value').reset_index()
  return df_

# TODO: Old code...
def filter_data(df_, levels_):
  if not args.tickers is None:
    df_ = df_.loc[df_.ticker.str.match(args.tickers)]
  
  if not args.level2_filter is None:
    df_ = df_.loc[df_[levels_[1]].str.match(args.level2_filter)]
  
  print('Result of filter operations:')
  for level in levels_[:-1]:
    print(f'- Unique values in the level {level}:{df_[level].unique()}')

  return df_

def I(df_, x):
  return x

def myeval(df_, new_col_, expr_):
  expr_.reverse()
  stack = None
  for e in expr_:
    if e[0]=='F':
      func = eval(e[1:])
      stack = func(df_, stack)
    if e[0]=='V':
      if not e[1:] in df_.columns:
        print(f'ERROR: {e[1:]} not a column. Columns:{df_.columns}')
        sys.exit(1)
      stack = e[1:]
  return df_, stack
  
def to_sns_dims(kwargs_):
  res = {}
  for key in kwargs_.keys():
    new_key = key
    if key=='color':
      new_key = 'hue'
    res[new_key] = kwargs_[key]
  return res

def myplot(df_):
  res = []
  for element in d_['elements']:
    kwargs = {}
    for pos_aes in element.args:
      for paarg in pos_aes.args:
        df_, val_ = myeval(df_, paarg.dim, paarg.val)
        kwargs[paarg.dim] = val_

    kwargs = to_sns_dims(kwargs)

    if element.geom=='line':
      kwargs['kind'] = 'line'

    if element.geom=='point':
      kwargs['kind'] = 'scatter'

    if element.geom=='interval':
      pass

    print(f'myplot geom:{element.geom} args:{kwargs}')
    rel_plot = sns.relplot(df_, **kwargs)

    # TESTING
    #plt.axvline(x=pd.to_datetime("20200101", format="%Y%m%d"))

    res.append(rel_plot._figure)
  return res


def main(args):
  l = Lark(grammar, start='stmts')
  tree = l.parse(args.stmts)  
  visit(tree)  
  df = read_data(args)
  df = filter_df(df, args.from_, args.to, None, args.tickers)
  df = create_levels(df, d_['data']['levels'])
  
#  print(tree.pretty())
#  pprint.pprint(d_)
  
  return myplot(df)
  

def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='gg.py', description=desc_, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('folder',            help='Folder with input files (for csv & parquet) or database (for duckdb)')
  parser.add_argument('table',             help='File (for csv & parquet) or Table (for duckdb) to use.')
  parser.add_argument('outfile',           help='Currently not used! Here for consistent argumets with expr and sql.')
  parser.add_argument('stmts',             help='Plotting statements using the graphics grammer')
  parser.add_argument('--index_type',      help='Index consists of Dates, YearWeek or YearMonth', choices=['daily','weekly','monthly'], default='daily')
  parser.add_argument('--backend',         help='Backends to use.', choices=['parquet','csv','duckdb'], default='parquet')
  parser.add_argument('--dbname',          help='Name of database (used as filename for duckdb).', default='tsldb')

  parser.add_argument('--tickers',         help='Tickers to include (regexp is used)', required=False)
  parser.add_argument('--from_',           help='From date (Ymd)', required=False, type=lambda d: datetime.datetime.strptime(d, '%Y%m%d'))
  parser.add_argument('--to',              help='To date (Ymd)',   required=False, type=lambda d: datetime.datetime.strptime(d, '%Y%m%d'))
  
  return parser

if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)
  main(args)
  plt.show()

  
