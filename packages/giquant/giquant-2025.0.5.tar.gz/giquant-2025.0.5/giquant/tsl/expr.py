#!/usr/bin/env python3
# /usr/bin/pypy3
#
# 240321, Jonas C.
#
# Perform calculations using the columns of tickers. Each expression is applied to all tickers
# (which all must have the columns used in the expression).
#
# TERMINOLOGY: (parquet) files consists of columns. Columns contain variables for tickers and
#              are named <ticker>_<variable>
#
# NOTE: np.na_to_num is used in get_matrix - 240530 removed this, need NaN when plotting!
#       and pd.fillna(np.nan) when reading the parquet file.
#
# RESOURCES: https://xmonader.github.io/letsbuildacompiler-pretty/
#

import os
import re
import ast
import sys
import builtins
import argparse
import numpy as np
import pandas as pd

from inspect import signature
from lark import Lark, Tree, Token

import giquant.tsl.helpers as helpers

DEBUG = False

def debug(*args, **kwargs):
  if DEBUG:
    print(*args, **kwargs)

    
# Globals
# =======
    
tokens = []
stack = []

df = None
df_ctx = None   # Additional context that is used for := expressions

# dict with tuples containing ndarray and list of column names
matrix = {}
mcnt = 0

# For expr: save any valid list of column names here. Will only use the the prefix (before the first underscore)
tickers = None

# for texpr: save an valid list of column names here. Will only use the suffix (after the first underscore)
columns = None

yaml_files = {}

# Parser for expr.py
# ==================
#
# NOTE: There is 'full' support for variables.
#       For tickers is only assignments and filtering possible at the moment. More operations
#       could be of use for funds etc.
#

grammar = r'''?stmts: stmt ";"           -> stmt
                  | stmt ";" stmts       -> seq

             ?stmt: VAR ":=" expr        -> assign_ctx
                 | TICK "=" texpr        -> assignt
                 | VAR "=" expr          -> assign
                 | COL "=" expr          -> assign
                 | "t" /[^; ]+/          -> filtert
                 | "v" /[^; ]+/          -> filterv
                 | "r" /[^; ]+/          -> renamet
                 | "s" /[^; ]+/          -> renamev
                 | FUNC "(" [NUMBER|BCONST|STRING]* ["," (NUMBER|BCONST|STRING)]* ")"  -> applydf

             ?texpr: tterm
             ?tterm: titem
             ?titem: TICK                 -> tick

             ?expr: term
                  | expr "+" term        -> add
                  | expr "-" term        -> sub
                  | bexpr

             ?term: item
                  | term "*" item        -> mul
                  | term "/" item        -> div
 
             ?item: NUMBER               -> number
                  | STRING               -> string
                  | VAR                  -> var
                  | COL                  -> col
                  | DICT                 -> dict
                  | MAP                  -> map
                  | "-" item             -> neg
                  | expr "if" bexpr "else" expr -> ifexpr
                  | FUNC "(" expr ["," expr]* ")" -> apply
                  | "(" expr ")"

             ?bexpr:  bterm              
                   |  bexpr "or" bterm     -> or
                   |  bexpr "and" bterm    -> and
                   |  expr  "=="  expr     -> eq
                   |  expr  "!="  expr     -> ne
                   |  expr  "<"  expr      -> lt
                   |  expr  "<=" expr      -> le
                   |  expr  ">"  expr      -> gt
                   |  expr  ">=" expr      -> ge

             ?bterm:  bitem 
                   |  bterm "and" bitem  -> and

             ?bitem:  BCONST             -> bconst
                   |  VAR                -> bvar
                   |  DICT               -> bdict
                   |  "not" bitem        -> not
                   |  "(" bexpr ")"

             BCONST: "True" | "False"

             TICK: "T" /\w/+ "$"*
             COL:  "C" /\w/+ "$"*
             VAR:  "V" /\w/+ "$"*
             FUNC: "F" (/\w/ "."*)+
             DICT: "D" /\w/+ "." /\w/+ "." /\w/+
             MAP:  "M" /\w/+ "." /\w/+ "." /\w/+
             COMMENT: "#" /[\w \.]/+ ";"

             %import common.SIGNED_NUMBER -> NUMBER
             %import common.ESCAPED_STRING -> STRING
             %import common.WS
             %ignore WS
             %ignore COMMENT
         '''

def print_state():
  debug(f'---\nstack:{stack}\ntokens:{tokens}\nmatrix:{matrix}\n---')

def pop_token():
  global tokens
  if len(tokens)==0:
    return None
  res = tokens[0]
  tokens = tokens[1:]
  debug(f'pop_token:{res}')
  return res

def add_token(t):
  debug(f'add_token:{t}')
  tokens.append(t)
  
def visit(t_):
  if isinstance(t_, Tree):
    if t_.data=='stmt':
      visit(t_.children[0])

    if t_.data=='assign_ctx':
      visit(t_.children[1])
      add_token(f':=[{t_.children[0].value}]')

    if t_.data=='assignt':
      visit(t_.children[1])
      add_token(f't=[{t_.children[0].value}]')
      
    if t_.data=='assign':
      visit(t_.children[1])
      add_token(f'=[{t_.children[0].value}]')
      
    if t_.data=='filtert':
      add_token(f't{t_.children[0].value}')
      
    if t_.data=='filterv':
      add_token(f'v{t_.children[0].value}')

    if t_.data =='renamet':
      add_token(f'r{t_.children[0].value}')
      
    if t_.data =='renamev':
      add_token(f's{t_.children[0].value}')
      
    if t_.data=='seq':
      for x in t_.children:
        visit(x)
        
    if t_.data=='neg':
      visit(t_.children[0])
      add_token('N')
      
    if t_.data=='add':
      visit(t_.children[1])
      visit(t_.children[0])
      add_token('+')
      
    if t_.data=='sub':
      visit(t_.children[1])
      visit(t_.children[0])
      add_token('-')
      
    if t_.data=='mul':
      visit(t_.children[1])
      visit(t_.children[0])
      add_token('*')
      
    if t_.data=='div':
      visit(t_.children[1])
      visit(t_.children[0])
      add_token('/')
      
    if t_.data in ['eq','ne','lt','le','gt','ge']:
      visit(t_.children[1])
      visit(t_.children[0])
      add_token(t_.data)

    if t_.data=='ifexpr':
      visit(t_.children[2])
      visit(t_.children[0])
      visit(t_.children[1])
      add_token('ifexpr')

    if t_.data=='apply' or t_.data=='applydf':
      for i in range(len(t_.children)-1, 0, -1):
        visit(t_.children[i])
      visit(t_.children[0])
      add_token(t_.data)
      
    if t_.data=='var' or t_.data=='dict' or t_.data=='map' or t_.data=='tick' or t_.data=='col':
      visit(t_.children[0])

    if t_.data=='not':
      visit(t_.children[0])
      add_token('not')
      
    if t_.data=='or':
      visit(t_.children[1])
      visit(t_.children[0])
      add_token('or')
      
    if t_.data=='and':
      visit(t_.children[1])
      visit(t_.children[0])
      add_token('and')
      
    if t_.data=='bconst' or t_.data=='bvar' or t_.data=='bdict' or t_.data=='number' or t_.data=='string':
      visit(t_.children[0])
      
  elif isinstance(t_, Token) and t_.type=='STRING':
    add_token(t_.value)
    
  elif isinstance(t_, Token) and t_.type=='NUMBER':
    add_token(float(t_.value))

  elif isinstance(t_, Token) and t_.type=='BCONST':
    add_token(bool(t_.value=='True'))

  elif isinstance(t_, Token):
    add_token(t_.value)

  elif t_ is None:
    return
    
  else:
    print(f'Unknown - tree:{t_}')
    sys.exit(1)


# Evaluate tokens (in postfix structure)
# =====================================

def push_stack(t):
  debug(f'push_stack:{t}')
  stack.insert(0, t)

def pop_stack():
  global stack
  if len(stack)==0:
    print(f'ERROR: pop on empty stack. tokens:{tokens}')
    sys.exit(1)
  res = stack[0]
  stack = stack[1:]
  debug(f'pop_stack:{res}')
  return res

def get_matrix(k_):
  global tickers, columns
  cols = None
  if isinstance(k_, float) or isinstance(k_, bool) or k_[0]=='"':
    return k_  
  if k_[0] == 'C':
    m0 = df.loc[:,k_[1:]].to_numpy()
  elif k_[0] == 'T':
    cols = sorted(df.columns[list(map(lambda x: not re.search(f'^{k_[1:]}_.*', x) is None, df.columns))])
    columns = cols
    m0 = df.loc[:,cols].to_numpy()
  elif k_[0] == 'V':
    if k_[1:] == 'index':
      m0 = df.index.to_numpy()
      m0 = np.tile(m0, (len(tickers),1)).T
    else:
      cols = sorted(df.columns[list(map(lambda x: not re.search(f'^.*_{k_[1:]}', x) is None, df.columns))])
      tickers = list(map(lambda x: x.split('_')[0], cols))
      m0 = df.loc[:,cols].to_numpy()
  elif k_[0] == 'D':
    t = k_[1:].split('.')
    d  = yaml_files[t[0]][t[1]]
    cols = sorted(d.keys())
    res = list(map(lambda x: d[x][t[2]], cols))
    m0 = np.stack([res]*df.shape[0])

    if tickers is None:
      print(f'ERROR tickers are not known when processing dict {t[0]}. Expressions must contain at least one column before dicts. State tokens:{tokens} stack:{stack}')
      sys.exit(1)

    m0 = helpers.shrink_ndarray(tickers, cols, m0)
  elif k_[0] == 'M':
    t = k_[1:].split('.')
    d  = yaml_files[t[0]][t[1]]
    col = t[2]
    dft = pd.DataFrame(index=df.index)
    for i in d.keys():
      for j in d[i].split(','):
        dft[f'{j}_{col}'] = df[f'{i}_{col}']
    cols = sorted(dft.columns)
    tickers = cols
    m0 = dft.loc[:,cols].to_numpy()
  elif k_[0] == 'm':
    if not k_ in matrix.keys():
      print(f'ERROR: get_matrix on non-existing key {k_}')
      sys.exit(1)
    m0 = matrix[k_]
  else:
    print(f'ERROR: Invalid identifier {k_} current stack: {stack}. Identifiers are prefixed with C=columns, T=tickers, V=variable, D=dict (and temporary matrices with M).')
    sys.exit(1)

  debug(f'get_matrix({k_}):{m0}')
    
#  return np.nan_to_num(m0)
  return m0

def save_matrix(m_):
  global mcnt
  k = f'm{mcnt}'
  mcnt = mcnt + 1
  matrix[k] = m_
  return k

def process_tokens():
  global df, df_ctx, tickers
  try:
    t = pop_token()
    while not t is None:
      if isinstance(t, bool) or isinstance(t, float) or t[0]=='"':
        push_stack(t)

      elif t[0]=='V' or t[0]=='D' or t[0]=='M' or t[0]=='F' or t[0]=='T' or t[0]=='C':
        push_stack(t)

      elif t=='N':
        n1 = pop_stack()
        m1  = get_matrix(n1)
        m0 = m1*-1
        n0 = save_matrix(m0)
        push_stack(n0)

      elif t[0:2]=='t=':
        n1 = pop_stack()
        cols = df.columns[list(map(lambda x: not re.search(f'{n1[1:]}_.*',x) is None, df.columns))]
        newcols = list(map(lambda x: t[4:-1] + '_' + x.split('_',1)[-1], df.columns))
        df1 = df.loc[:,cols]
        df1.columns = newcols
        df = pd.concat([df,df1], axis=1)
        
      elif t[0]=='=':
        n1 = pop_stack()
        m1 = get_matrix(n1)
        if t[2]=='V':
          colname = t[3:-1]
          newcols = list(map(lambda x: x.split('_')[0] + '_' + colname, tickers))
          debug('Assign to',newcols)
          df.loc[:,newcols] = m1   # 240905 Changed from df[newcols] = m1, and also below!
        elif t[2]=='C':
          df.loc[:,t[3:-1]] = m1
        else:
          print('ERROR! Unknown type in assignment {t[2]}')
          
      elif t[0:2]==':=':
        n1 = pop_stack()
        m1 = get_matrix(n1)
        if t[3]=='V':
          colname = f'CTX_{t[4:-1]}'
          df1 = pd.DataFrame(m1, columns=[colname], index=tickers)
          if df_ctx is None:
            df_ctx = df1
          else:
            df_ctx = pd.concat([df_ctx, df1], axis=1)   
        else:
          print(f'ERROR! Unknown type in assignment: {t[3]}')

      elif t[0]=='t':
        tickers = t[1:]
        cols = df.columns[list(map(lambda x: not re.search(f'^(Date|YearWeek)|^({tickers}_.*)', x) is None, df.columns))]
        df = df.loc[:,cols]

      elif t[0]=='v':
        variables = t[1:]
        cols = df.columns[list(map(lambda x: not re.search(f'^(Date|YearWeek)|^(.*_{variables})', x) is None, df.columns))]
        df = df.loc[:,cols]

      # TODO: Skip this and only use s (below)? Perhaps call it r.
      elif t[0]=='r':
        print('r not used anymore. Use s for renaming tickers and variables!')
        sys.exit(1)
        for r in t[1:].split(','):
          src, target = r.split('>')
          src_cols = df.columns[list(map(lambda x: not re.search(f'^{src}_.*', x) is None, df.columns))]
          target_cols = list(map(lambda x: f"{target}_{x.split('_')[1:][0]}", src_cols))
          df[target_cols] = df[src_cols]
          keep_cols = df.columns[list(map(lambda x: re.search(f'Date|^YearWeek|^{src}_.*', x) is None, df.columns))]
          df = df.loc[:,keep_cols]
        df = df.copy()

      elif t[0]=='s':
        for r in t[1:].split(','):
          src, target = r.split('>')
          df.columns = list(map(lambda x: re.sub(src, target, x), df.columns))

      elif t=='ifexpr':
        n3 = pop_stack()
        n2 = pop_stack()
        n1 = pop_stack()
        m3 = get_matrix(n3)
        m2 = get_matrix(n2)
        m1 = get_matrix(n1)
        m0 = np.where(m3, m2, m1)
        n0 = save_matrix(m0)
        push_stack(n0)

      elif t=='apply':
        n1 = pop_stack()
        g = eval(n1[1:])
        if g.__doc__ is None:
          no_args = len(signature(g).parameters.values())
        else:
          doc = list(filter(lambda x: x!='', g.__doc__.split('\n')))
          no_args = len(doc)
        debug(f'{g} takes {no_args} arguments. stack:{stack}')
        gargs = []
        shapes = []
        for i in range(0, no_args):
          n0 = pop_stack()
          garg =  get_matrix(n0)
          gargs.append( garg )
          if isinstance(garg, np.ndarray):
            shapes.append(garg.shape)
          
        if not all(list(map(lambda x: x[1]==len(tickers), shapes))):
          print(f'ERROR: mismatch between matrix size and number of argument. shapes:{shapes}. Number of tickers:{len(tickers)}.\nPerhaps the $ is missing in Vxxx$?')
          sys.exit(1)
        
        m0 = []
        for i in range(0, len(tickers)):
          print(f'{tickers[i]}..', end='', flush=True)
          args = []
          for k in range(0, len(gargs)):
            if isinstance(gargs[k], str):
              args.append(gargs[k][1:-1])
            elif isinstance(gargs[k], float):
              args.append(gargs[k])
            else:
              args.append(gargs[k][:,i])
          m0.append( g(*args) )
        m0 = np.tile(m0, (1,1)).T
        n0 = save_matrix(m0)
        push_stack(n0)
          
      elif t=='applydf':
        n1 = pop_stack()
        g = eval(n1[1:])
        if g.__doc__ is None:
          no_args = len(signature(g).parameters.values())
        else:
          doc = list(filter(lambda x: x!='', g.__doc__.split('\n')))
          no_args = len(doc)
        debug(f'{g} takes {no_args} arguments. stack:{stack}')
        gargs = [df]
        for i in range(1, no_args):
          n0 = pop_stack()
          m0 = get_matrix(n0)
          if isinstance(m0, str):
            gargs.append(m0[1:-1])
          elif isinstance(m0, float):
            gargs.append(m0)
          else:
            gargs.append(m0)
        df = g(*gargs)

      elif t in ['+', '-', '*', '/', 'eq', 'ne', 'lt', 'le', 'gt', 'ge', 'and', 'or']:
        n1 = pop_stack()
        n2 = pop_stack()
        m1 = get_matrix(n1)
        m2 = get_matrix(n2)

        if isinstance(m1, np.ndarray) and isinstance(m2, np.ndarray) and  m1.shape != m2.shape:
          print(f'ERROR: the matrix dimensions for {n1} and {n2} differ [{m1.shape} vs {m2.shape}]')
          sys.exit(1)
        
        if t=='+':
          m0 = np.add(m1, m2)
        elif t=='-':
          m0 = np.subtract(m1, m2)
        elif t=='*':
          m0 = np.multiply(m1, m2)
        elif t=='/':
          m0 = np.divide(m1, m2)

        elif t=='eq':
          m0 = np.equal(m1, m2)
        elif t=='ne':
          m0 = np.not_equal(m1, m2)
        elif t=='lt':
          m0 = np.less(m1, m2)
        elif t=='le':
          m0 = np.less_equal(m1, m2)
        elif t=='gt':
          m0 = np.greater(m1, m2)
        elif t=='ge':
          m0 = np.greater_equal(m1, m2)

        elif t=='and':
          m0 = np.logical_and(m1, m2)
        elif t=='or':
          m0 = np.logical_or(m1, m2)

        debug('process_tokens m1:', m1)
        debug('process_tokens m2',  m2)
        debug('process_tokens t',   t)
        debug('process_tokens m0',  m0)

        n0 = save_matrix(m0)
        push_stack(n0)

      elif t=='not':
        n = pop_stack()
        push_stack(not n)

      elif t=='or':
        n1 = pop_stack()
        n2 = pop_stack()
        push_stack(n1 or n2)

      elif t=='and':
        n1 = pop_stack()
        n2 = pop_stack()
        push_stack(n1 and n2)

      else:
        print(f'ERROR: unknown operator {t}')

      t = pop_token()

      
  #except Exception as e:
  except BufferError as e:  # match some uncommon exception in order not to catch exceptions
    print(f'ERROR in process_tokens. stack:{stack}, tokens:{tokens}')
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    sys.exit(1)



def main(args):
  global df, df_ctx, DEBUG
  
  DEBUG = args.debug
  SAVE_FOLDER = args.folder #helpers.read_config()['config']['WIDE_FOLDER']

  
  if not args.yaml is None:
    yaml_files[args.yaml] = helpers.read_yaml(args.yaml)
    
  if not args.py is None:
    from pathlib import Path
    parent = Path(__file__).resolve().parent
    
    # pyfilename = f'{parent}/../../{args.py}.py'
    #pyfilename = f'{os.getcwd()}/{args.py}.py'
    pyfilename = f'{args.py}.py'
    with open(pyfilename, 'r') as f:
      py = f.read()

      # Check the code for name clashes before loading it
      a = ast.parse(py)
      for el in ast.walk(a):
        if isinstance(el, ast.FunctionDef):
          if el.name in list(locals().keys()) or el.name in dir(__builtins__):
            print(f'ERROR: `{el.name}` is a reserved word and cannot be used as a function!')
            sys.exit(1)
    
      exec(py, globals())
      debug(f'These functions are currently defined: {sorted([item for item in list(locals().keys()) if not item.startswith("__")])}')
  
  # conf = helpers.read_config()
  l = Lark(grammar, start='stmts')
  tree = l.parse(args.stmts)
  visit(tree)
  if args.parse_only:
    print(f'parse tree:\n{tree.pretty()}')
    print(f'stmts:{args.stmts}')
    print(f'tokens:{tokens}')
  else:
    '''
    # NOTE: tokens and df are global variables
    if args.infile.endswith('.csv'):
      df = pd.read_csv(f'{SAVE_FOLDER}/{args.infile}')
      df = df.set_index('Date')
    else:
      df = pd.read_parquet(f'{SAVE_FOLDER}/{args.infile}.parquet')
    '''
    df = helpers.dal_read_df(args.folder, args.infile, args.backend, args.dbname)

    df.columns = list(map(lambda x: x.strip(), df.columns))
    df = df[sorted(df.columns)]
    df = df.fillna(np.nan)
    process_tokens()
    if not df is None:
      df = df[sorted(df.columns)]
      # helpers.save_df(df, f'{SAVE_FOLDER}/{args.outfile}')
      helpers.dal_save_df(df, args.folder, args.outfile, args.backend, args.dbname)

      if not df_ctx is None:
        df_ctx = df_ctx.sort_index()
        # helpers.save_df(df_ctx, f'{SAVE_FOLDER}/{args.outfile}_ctx')
        helpers.dal_save_df(df_ctx, args.folder, f'{args.outfile}_ctx', args.backend, args.dbname)

  return 'Finished processing statements.'


desc_ = f"""
Create new column from existing columns using an expression. Applied to all tickers in the file.

BNF (used by Lark)
------------------

            {grammar}

Example: C4=C1+C2/-C3; F[T4|T1] => 
         F is a filter operation applied to tickers (using a regexp). It is possible to exclude specific tickers using the format F[~(T1|T2)].
         = is an operator with the side effect of creating a new column.

Note: Column names are regular expressions. Columns in the filemust have the format ticker_variable. variable$ should be
      used when several variables have the same suffix. For instance Close$ should be used when both ticker_Close and 
      ticker_Close_hv20 exists.

!!! Gotchas !!!
      1) Vx is a regular expression. Vx will alao match Vxy. Use Vx$ if Vxy also exists.
      2) Always use parenthesis around boolean expressions, eg. Vz if (Vx<Vy)... *not* if Vx<Vy
      3) Negative numbers also need parenthesis, eg (-1) if (Vx<Vy)... *not -1 if (Vx<Vy)
"""

def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='expr.py', description=desc_, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('folder',       help='Folder with tsl data.')
  parser.add_argument('infile',       help='Parquet/CSV-file or table with data')
  parser.add_argument('outfile',      help='Parquet/CSV-file or table to store the result')
  parser.add_argument('stmts',        help='Statements to parse. Use --help for full BNF.')
  parser.add_argument('--parse-only', help='Only parse the input and show tokens in postfix notation.', action=argparse.BooleanOptionalAction, default=False) 
  parser.add_argument('--debug',      help='Print debug messages', action=argparse.BooleanOptionalAction, default=False) 
  parser.add_argument('--py',         help='Python file to import. Functions that can be used in FUNC items (as part of expressions)')
  parser.add_argument('--yaml',       help='YAML file to import. Load dicts that can be used in items (as part of expressions)')
  parser.add_argument('--backend',    help='Backend to use. Supported are: parquet, duckdb and csv]', default='parquet')
  parser.add_argument('--dbname',     help='Name of database (used as filename for duckdb)', default='tsldb')
  return parser


if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)

  main(args)
