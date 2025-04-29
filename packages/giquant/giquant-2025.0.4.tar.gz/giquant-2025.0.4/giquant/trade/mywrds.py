#
# 241228 Jonas C.
#


import sys
import wrds
import argparse

import pandas as pd
#import polars as pl


COLS=['fyr','SALE','INDFMT','DATAFMT','POPSRC','CONSOL',
      'GVKEY','DATADATE','FYEAR','AT','LT','SEQ','MIB',
      'CSHO','SALE','COGS','OPINI','IB','PI','RE', 'NI',
      'DVT','FOPT','IBC','DP','EMP','CH','CHE',
      'PRCC_C','PRCC_F','ACT','LCT','EBIT','EBITDA','BKVLPS',
      'UXINTD','UXINST','DLTT','DLC','MKVALT','PPENT',
      'XRD','PRSTKC','ICAPT','APC','PSTKC'
      ]

IDX_COLS = ['gvkey','fyear']

VAL_COLS=['SALE','INDFMT','DATAFMT','POPSRC','CONSOL',
          'AT','LT','SEQ','MIB',
          'CSHO','SALE','COGS','OPINI','IB','PI','RE', 'NI',
          'DVT','FOPT','IBC','DP','EMP','CH','CHE',
          'PRCC_C','PRCC_F','ACT','LCT','EBIT','EBITDA','BKVLPS',
          'UXINTD','UXINST','DLTT','DLC','MKVALT','PPENT',
          'XRD','PRSTKC','ICAPT','APC','PSTKC'
          ]

VAL_COLS = list(map(lambda x: x.lower(), VAL_COLS))
VAL_COLS2=['SALE','AT','LT','SEQ','MIB','CSHO'
          ]
VAL_COLS = list(map(lambda x: x.lower(), VAL_COLS2))
ALL_COLS = IDX_COLS + VAL_COLS


def show_table(table_='funda', library_='comp'):
  db = wrds.Connection()
  print(db.list_libraries())
  print(db.list_tables(library=library_))
  print(db.describe_table(library=library_, table=table_))
  rows = db.get_table(library=library_, table=table_, columns=COLS, rows=1000)
  print(rows)
  db.close()


def get_table(folder_, cols_=COLS, table_='funda', library_='comp', max_rows=902644):
  db = wrds.Connection()

  no_rows = 100000
  cnt = 0
  offset = no_rows * cnt

  while offset < max_rows:
    print(offset, end='...', flush=True)
    df = db.get_table(library=library_, table=table_, columns=cols_, rows=no_rows, offset=offset)
    if cnt==0:
      print(df)
    df.to_csv(f'{folder_}/{library}_{table_}_sel{cnt}.csv', header=(cnt==0))
    cnt += 1
    offset += no_rows

  db.close()
  print(f'Result saved in {folder_}/{library}_{table_}_selX.csv. Concat these files into one csv-file using cat etc.')


def tots(folder_, usecols_=ALL_COLS, table_='funda', library_='comp'):
  
  df = pd.read_csv(f'{folder_}/{library}_{table_}_sel.csv'
                   , usecols=usecols_
                   , dtype={'fyear': 'float64'}
      )

  df = df[df.notnull()]
  df['fyear'] = df['fyear'].fillna(0)
  df = df.astype({'fyear': 'int32'})

  fyears = df.fyear.unique()
  df = df.set_index(df.fyear)
  df = df.sort_index()

  print(f'MEMORY USAGE: {df.memory_usage().sum() / 1e6} MB')
  print(df.columns)
  print(df.index)

  res = None
  cnt = 0
  print(f'shape:{df.shape}', flush=True)
  for fyear in fyears:
    if cnt%10 == 0:
      print(cnt, end='...', flush=True)

    df0 = df[df.fyear==fyear]
    df0 = df0.melt(id_vars=IDX_COLS)
    df0 = df0.pivot_table(index=['gvkey','variable'], columns='fyear', values='value')
    df0 = df0.reset_index()
    cnt += 1

    if res is None:
      res = df0
    else:
      res = res.merge(df0, left_on=['gvkey','variable'], right_on=['gvkey','variable'], how='outer')

  res['key'] = res.gvkey.astype(str) + '_' + res.variable
  res = res.set_index('key')
  res = res[fyears]

  res.to_csv(f'{folder_}/{library}_{table_}_sel_ts0.csv', index=True)
  res = res.transpose()
  res.to_csv(f'{folder_}/{library}_{table_}_sel_ts.csv.csv', index=True)

  print(f'Result saved in {folder_}/{library}_{table_}_sel_ts0.csv and {folder_}/{library}_{table_}_sel_ts.csv')

desc_='Download Compustat data from WRDS/CRSP. A WRDS login is required!'
  
def create_args_parser(parser):
  if parser is None:
    parser = argparse.ArgumentParser(prog='wrds.py', description=desc_)
  parser.add_argument('action',      help='Show extract from a table. Save a table. Convert compustat table to time series (indexed by gvkey and fyear).',
                      choices=['show_table','get_table','tots'])
  parser.add_argument('--folder',    help='Folder for data (default=./data)', default='./data')
  parser.add_argument('--cols',      help=f'Columns to use (default={",".join(COLS)})', default=COLS)
  parser.add_argument('--table',     help='Table in library (default=funda)', default='funda')
  parser.add_argument('--library',   help='Library to use (default=comp)', default='comp')
  parser.add_argument('--max_rows',  help='Used with get_table (default=1000000)', default=1000000)
#  parser.add_argument('--backend',   help='Comma separated list with backends to use. Only duckdb is supported at the moment.', default='duckdb')
#  parser.add_argument('--dbname',    help='Name of database (used as filename in duckdb)', default='tsldb')
#  parser.add_argument('--outformat', help='Format for outfile. csv and parquet is supported.', choices=['csv','parquet'], default='csv')
  return parser                                                                                                                      
                                                                                                                                     
def main(args):
  if args.action=='show_table':
    show_table(table_=args.table, library_=args.library)
    
  elif args.action=='get_table':
    get_table(args.folder_, cols_=args.cols, table_=args.table, library_=args.library, max_rows=args.max_rows)

  elif args.action=='tots':
    tots(args.folder_, usecols_=args.cols, table_=args.table, library_=args.library, max_rows=args.max_rows)

  else:
    print(f'Unknown action {args.action}')    
    
if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)

  main(args)
