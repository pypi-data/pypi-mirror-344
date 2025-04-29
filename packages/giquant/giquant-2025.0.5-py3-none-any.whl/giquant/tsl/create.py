#!/usr/bin/env python3
#
# 240325 Jonasd C.
#
#

import re
import os
import ast
import sys
import yaml
import glob
import argparse
import datetime

import pathlib 
from collections import defaultdict

import numpy as np
import pandas as pd
import duckdb

import giquant.tsl.helpers as helpers



def summarize(df_, id_var, index_var, value_var, filename, year_week):
  if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
    
  if year_week:
    df['year'] = df.index // 100
  else:
    df['year'] = df.index // 10000
  df_long = pd.melt(df, id_vars=[id_var,'year'], value_vars=[value_var])
  #df_long = df_long.drop_duplicates([id_var,'year','variable'])   # Below works better!
  df_long = df_long.groupby([id_var,'year','variable'], as_index=False).first()
  df_wide = df_long.pivot(index=id_var, columns=['variable','year'], values='value')
  df_res = (~df_wide.isnull()).applymap(lambda x: 'X' if x else '')
  df_res = df_res.sort_index(axis=1)
  summary_path = f'{OUTPUT_PATH}/{filename}.txt'
  df_res.to_csv(summary_path, sep='\t', index=True)
  print(df_res)
  print(f'Summary saved to {summary_path}\n')

# NOTE: Not used, remove
def get_from_to_per_ticker(df_, ticker_col, time_col):
  df1 = df_.groupby(ticker_col)[time_col].agg([min,max])
  df1 = df1.reset_index()
  df1 = df1.sort_values('min')
  return df1

def fix_column_names(df_):
  if any(map(lambda x: ' ' in x, df_.columns)):
    print(f'!!!Space not allowed in columns names!!!\n{list(df_.columns)}')
    df_.columns = list(map(lambda x: x.replace(' ','_'), df_.columns))
    print(f'New columns names:\n{list(df_.columns)}')
  if any(map(lambda x: '(' in x or ')' in x, df_.columns)):
    print(f'!!!Parenthesis not allowed in columns names!!!\n{list(df._columns)}')
    df_.columns = list(map(lambda x: x.replace('(',''), df_.columns))
    df_.columns = list(map(lambda x: x.replace(')',''), df_.columns))
    print(f'New columns names:\n{list(df_.columns)}')
  return df_
    
def pivot(df, index_var, id_var, value_vars):
  df = df.reset_index()
  df = df.melt(id_vars=[index_var, id_var], value_vars=value_vars)

  print('--- Duplicated rows (keep first only) ---')
  df1 = df[df.duplicated(subset=[index_var,id_var,'variable'])].sort_values([index_var,id_var,'variable'])
  df1.to_csv(f'{OUTPUT_PATH}/duplicates.csv')
  print(f'Duplicates saved to {OUTPUT_PATH}/duplicates.csv ({df1.shape[0]} rows)')
  
  print(f'before dropping duplicates in long format shape:{df.shape}')
  df = df.drop_duplicates(subset=[index_var,id_var,'variable'], keep='last')
  print(f'after dropping duplicates in long format shape:{df.shape}')

  df = df.pivot(index=[index_var], columns=[id_var,'variable'], values=['value'])
  df.columns = df.columns.to_series().str.join('_')
  df.columns = list(map(lambda x: x.removeprefix('value_'), df.columns))
  df = df[df.columns.sort_values()]
  return df

def save_df(df_, backends, folder, filename, dbname):
  # path_ = f'{folder}/{filename}'
  for backend in backends:
    helpers.dal_save_df(df_, folder, filename, backend, dbname)

    '''
    if backend == 'csv':
      df.to_csv(f'{path_}.csv', index=True)
      print(f'Results saved in {path_}.csv')
      
    if backend == 'parquet':
      df.to_parquet(f'{path_}.parquet', index=True)
      print(f'Results saved in {path_}.parquet.')

    if backend == 'duckdb':
      df_ = df_.reset_index()
      path_ = f'{folder}/{dbname}.duckdb'
      con = duckdb.connect(database = path_, read_only = False)
      con.sql(f"DROP TABLE IF EXISTS {filename}; CREATE TABLE {filename} AS SELECT * FROM df_")
      con.close()
      print(f'Results saved in {path_}.')
    '''


def create_args_parser():
  parser = argparse.ArgumentParser(prog='create.py', description='Create times series in backend using CSV-files')
  parser.add_argument('folder',          help='Folder with tsl data.')
  parser.add_argument('infiles',         help='Filenames of CSV input file (comma separated)')
  parser.add_argument('index',           help='Name of column for time axis, i.e. dates, year and week etc.')
  parser.add_argument('id',              help='Column identifying a row, typically symbol or ticker. "__filename__" will use the filename.')
  parser.add_argument('values',          help='Columns with values, for instance Open,High,Low,Close,Volume etc. Columns not listed are ignored.')
  parser.add_argument('outfile',         help='Name of parquet file to create')
  parser.add_argument('--date_format',   help='Format to use when parsing date-col', default='%y%m%d')
  parser.add_argument('--index_name',    help='Name of index column', default='Date')
  parser.add_argument('--id_name',       help='Name of id column', default='ticker')
  parser.add_argument('--col_names',     help='New names to give the columns')
  parser.add_argument('--header',        help='Header with column labels to use (typically when there is no header in the file)')
  parser.add_argument('--non_num',       help='Non-numeric columns (regex)')
  parser.add_argument('--save_summary',  help='Save summary of data to file')
  parser.add_argument('--use_ffill',     help='Pad empty field with most recent non-null value', action=argparse.BooleanOptionalAction, default=False)
  parser.add_argument('--YearWeek',      help='Convert date column to year and week', action=argparse.BooleanOptionalAction, default=False)
  parser.add_argument('--py',            help='Python file with functions used. See --func and --func2.')
  parser.add_argument('--func',          help='Function to apply to DataFrame created from infiles (must take one argument)')
  parser.add_argument('--func2',         help='Function to apply to resulting DataFrame (must take one argument)')
  parser.add_argument('--symbols',       help='Symbols to include (regex). Is performed before --func function is called.')
  parser.add_argument('--tickers',       help='Tickers to include (regex)')
  parser.add_argument('--from_dt',       help='From date Ymd', type=int)
  parser.add_argument('--to_dt',         help='To date Ymd', type=int)
  parser.add_argument('--output_folder', help='Save summary of processing here', default='./output')
  parser.add_argument('--backends',      help='Comma separated list with backends to use. Supported are: parquet, duckdb and csv]', default='parquet,csv')
  parser.add_argument('--dbname',        help='Name of database (used as filename in duckdb)', default='tsldb')
   
  return parser
  
def main(args):
  global OUTPUT_PATH, SAVE_FOLDER, df

  OUTPUT_PATH = args.output_folder
  SAVE_FOLDER = args.folder

  
  # Parse imports 
  # --------------
  if not args.py is None:
    from pathlib import Path
    parent = Path(__file__).resolve().parent
#    with open(f'{parent}/../../{args.py}', 'r') as f:
    # TODO: Changed after switching to python modules. This is not tested!!
    with open(f'{args.py}', 'r') as f:
      py = f.read()

      # Check the code for name clashes before loading it
      a = ast.parse(py)
      for el in ast.walk(a):
        if isinstance(el, ast.FunctionDef):
          if el.name in list(locals().keys()) or el.name in dir(__builtins__):
            print(f'ERROR: `{el.name}` is a reserved word and cannot be used as a function!')
            sys.exit(0)

      exec(py)

      
  # Read files
  # -------------

  types = defaultdict(lambda: 'float', {args.id:'str', args.index: 'str'})
  non_num = args.non_num.split(',') if not args.non_num is None  else []
  types.update(dict(zip(non_num, ['str']*len(non_num))))

  cols = [args.index,args.id] + args.values.split(',')
  if args.id == "__filename__":
    cols = [args.index] + args.values.split(',')
    
  df = None
  for infile in args.infiles.split(','):
    if infile == '':
      continue
    print(f'{infile}...')
    if not args.header is None:
      df1 = pd.read_csv(infile,
                        index_col=False,
                        low_memory=False,
                        # header=0,
                        names=args.header.split(','),
                        usecols=cols,
                        skipinitialspace=True,
                        on_bad_lines='warn',
                        dtype=types)
    else:
      df1 = pd.read_csv(infile,
                        index_col=False,
                        low_memory=False,
                        usecols=cols,
                        skipinitialspace=True,
                        on_bad_lines='warn',
                        dtype=types)
    
    if args.id == "__filename__":
      ticker = infile.split("/")[-1].split('.')[0]
      print(f'Use {ticker} as id for {infile}')
      df1['ticker'] = ticker
      
    if df is None:
      df = df1
    else:
      df = pd.concat([df, df1], axis=0)
    
  # Check that we have some data
  # -----------------------------

  if df is None:
    print(f'ERROR: No data found in: {args.infiles}!')
    sys.exit(1)
  
  # Fix column names and set time as index
  # ---------------------------------------

  df = fix_column_names(df)

  # assign new names to columns
  if not args.col_names is None:
    d = {}
    d[args.id] = args.id_name
    d[args.index] = args.index_name
    d.update(zip(args.values.split(','), args.col_names.split(',')))
    df = df.rename(d, axis=1)

  df[args.id_name]    = df[args.id_name].astype(str)
  df[args.id_name]    = df[args.id_name].str.strip()

  if df[args.id_name].str.contains('+', regex=False).any():
    print(f'The id column ({args.id_name}) cannot contain entries with the "+" sign. The "+" sign will be replaced with a "p"')
    df[args.id_name] = df[args.id_name].str.replace('+', 'p')

  df[args.index_name] = df[args.index_name].astype(str)
  df[args.index_name] = df[args.index_name].str.strip()
  
  
  # Filter symols
  # --------------

  if not args.symbols is None:
    print(f'Regex used for filtering: ^({args.symbols})$')
    print(f'symbols found before filtering:\n{sorted(df[args.id_name].unique())}')
    df = df.loc[df[args.id_name].str.match(f'^({args.symbols})$')]
    print(f'symbols remaining after filtering:\n{sorted(df[args.id_name].unique())}')

    
  # Run functions in imports
  # ------------------------
  
  if not args.func is None:
    f = eval(args.func)
    df = f(df)

    
  # Filter tickers
  # --------------

  if not args.tickers is None:
    df = df.loc[df[args.id_name].str.match(f'^({args.tickers})$')]
    print(f'tickers found after filtering:\n{sorted(df[args.id_name].unique())}')


  # Set time as index
  # -----------------

  if args.YearWeek:
    df['YearWeek'] = df[args.index_name].map(lambda x: helpers.date2week_(x, args.date_format))
    df = df.set_index('YearWeek')
    args.index_name = 'YearWeek'                              # Hack! Not great, fix at some point!!
  else:
    print(f'before dropping rows with incorrect dates - shape:{df.shape}')
    df['dt'] = pd.to_datetime(df[args.index_name], format=args.date_format, errors='coerce')
    if df.dt.isnull().sum() > 0:
      df1 = df.loc[df.dt.isnull()]
      print(f'Rows with incorrect dates:{df1.shape[0]}. Tickers with incorrect dates: {df1.ticker.unique()}')
      try:
        print(f'Date conversion failed using format {args.date_format}!')
        for k in df[args.index_name].values:
          import datetime
          dt_ = datetime.datetime.strptime(k, args.date_format)
      except Exception as e:
        print(e)
          
    df = df[~df.dt.isnull()]
    df[args.index_name] = df.dt.map(helpers.dt2int)
    df = df.set_index(args.index_name)
    print(f'after dropping rows with incorrect dates - shape:{df.shape}')

  # TODO: Simple drop don't work. Cannot see why...
  df = df[list(filter(lambda x: x!='dt', df.columns))]
#  df = df.drop(columns=['dt'])


  # Fix types for value columns
  # --------------------------
  
  non_num = [args.id_name]
  if not args.non_num is None:
    non_num = non_num + args.non_num.split(',')

  cols1 = df.columns[list(map(lambda x: re.search(f'^{"|".join(non_num)}', x) is None, df.columns))]
  print(f'Convert these columns to number:{cols1}')
  df1 = df[cols1].apply(pd.to_numeric, errors='coerce')
  
  cols2 = df.columns[list(map(lambda x: not re.search(f'^{"|".join(non_num)}', x) is None, df.columns))]
  print(f'Do not convert these columns to number:{cols2}')
  df2 = df[cols2]
  df = pd.concat([df2, df1], axis=1)

  
  # Filter selected dates
  # ---------------------
  
  if not args.from_dt is None:
    if args.to_dt is None:
      print('ERROR: both from_dt and to_dt must be supplied!')
      sys.exit(1)
      
    print(f'shape before filtering dates ({args.from_dt}-{args.to_dt}): {df.shape}')
    df = df.loc[(df.index>=args.from_dt) & (df.index<=args.to_dt)]
    print(f'shape after filtering dates: {df.shape}')

  
  # Print summary (if requested)
  # ----------------------------

  if not args.save_summary is None:
    print('--- Summary ---')
#    print(get_from_to_per_ticker(df, args.id_name, args.index_name))
    summarize(df, args.id_name, args.index_name,
              args.col_names.split(',')[0] if not args.col_names is None else 'Close',
              args.save_summary,
              args.YearWeek)
  
  # Transform to wide format
  # -------------------------

  print(f'shape before converting to wide:{df.shape}')
  # print(f'columns:{df.columns}\ntypes:{df.dtypes}')
  df = pivot(df, args.index_name, args.id_name,
             args.col_names.split(',') if not args.col_names is None else list(df.columns))
  df = df.sort_index()


  # Handle missing data
  # -------------------
  
  if args.use_ffill:
    if args.YearWeek:
      print('use_ffill and YearWeek not supported together')
      sys.exit(1)
    df = df.sort_index()
    df['dt'] = pd.to_datetime(df.index, format='%Y%m%d', errors='coerce')
    df = df.set_index('dt')
    df.index.names = [args.index_name]
    df1 = pd.DataFrame(data=pd.date_range(df.index.min(), df.index.max(), freq='B'), columns=['Date'])
    df = df.merge(df1, left_index=True, right_on='Date', how='outer')
    df = df.set_index(args.index_name)
    df = df.ffill()
    df.index = df.index.map(helpers.dt2int)

  df[df.isnull()] = np.nan


  # Run functions in imports on the final df
  # ------------------------
  
  if not args.func2 is None:
    f = eval(args.func2)
    df = f(df)

  
  # Save result
  # -----------
  
  df = df.sort_index()

#  print(f'{df.dtypes}')
#  num_cols = list(map(lambda x: re.search(f'{args.non_num}', x) is None, df.columns))
#  if not all(df.dtypes[num_cols]==[float]*len(num_cols)):
#    print(f'ERROR" Non-numeric columns: {df.columns[(df.dtypes[num_cols]==[float]*len(num_cols))]}')
#    sys.exit(1)

  pathlib.Path(SAVE_FOLDER).mkdir(parents=True, exist_ok=True)

  save_df(df, args.backends.split(','), SAVE_FOLDER, args.outfile, args.dbname)

  
if __name__ == '__main__':
  print(f'Current Working Directory: {os.getcwd()}')
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)

  main(args)
