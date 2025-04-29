#!/usr/bin/env python3
#
# 240113, Jonas C.
#
# Basic merge/join of two parquet files
#

import re
import sys
import duckdb
import argparse
import pandas as pd

import giquant.tsl.helpers as helpers


def my_merge(df1, df2, idx, how):
  df = df1.merge(df2, how=how, left_on=idx, right_on=idx, suffixes=['','_dup'])
  df = df.iloc[:,list(map(lambda x: re.search('_dup',x) is None, df.columns))]
#  if 'Date_dt_x' in df.columns:
#    df = df.drop(['Date_dt_x'], axis=1)
#  if 'Date_dt_y' in df.columns:
#    df = df.drop(['Date_dt_y'], axis=1)
  return df

def merge_files(files, idx, how):
  file1, file2, *files = files
  df1 = pd.read_parquet(f'{SAVE_FOLDER}/{file1}.parquet')
  df2 = pd.read_parquet(f'{SAVE_FOLDER}/{file2}.parquet')
  df = my_merge(df1, file2df2, idx, how)
  while len(files) > 0:
    file, *files = files
    df2 = pd.read_parquet(f'{SAVE_FOLDER}/{file}.parquet')
    df = my_merge(df, df2, idx, how)
  return df


def cmp_tickers(df1, df2):
  ticks1 = set(list(map(lambda x: x.split('_')[0], df1.columns)))
  ticks2 = set(list(map(lambda x: x.split('_')[0], df2.columns)))

  if ticks1 != ticks2:
    #print(f'ERROR! tickers differ: {ticks1.symmetric_difference(ticks2)}. In df1 but not df2: {ticks1.difference(ticks2)}. In df2 but not df1: {ticks2.difference(ticks1)}')
    print(f'ERROR! tickers differ. In df1 but not df2: {ticks1.difference(ticks2)}. In df2 but not df1: {ticks2.difference(ticks1)}')
    return False

  return True

desc_='Merge files. Parquet and CSV is supported.'
def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='merge.py', description=desc_)
  parser.add_argument('folder',    help='Folder with tsl data.')
  parser.add_argument('infile1',   help='Parquet-file or table with data')
  parser.add_argument('infile2',   help='Parquet/CSV-file or table with data')
  parser.add_argument('outfile',   help='Filename or table to save the result in')
  parser.add_argument('--files',   help='Comma separated list of files to merge (infile1 & infile2 is ignored')
  parser.add_argument('--folder',  help='Folder with input and put files', default='~/aws-s3/gizur-trade-csv/wide')  # TODO: Remove default
  parser.add_argument('--tickers', help='Regex qwith tickers to keep')
  parser.add_argument('--index',   help='Column to use in merge/join. Default is Date', required=False, default='Date')
  parser.add_argument('--csv2',    help='Infile2 is a csv file.', action=argparse.BooleanOptionalAction)
  parser.add_argument('--how',     help='Inner or outer join. default=inner', choices=['inner','outer'], default='inner')
  parser.add_argument('--cmp-tickers',  help='Compare tickers of the two files', action=argparse.BooleanOptionalAction, default=True)
  parser.add_argument('--backend',      help='Backend to use. Supported are: parquet, duckdb and csv]', default='parquet')
  parser.add_argument('--dbname',       help='Name of database (used as filename in duckdb)', default='tsldb')
  return parser

def main(args):
  global SAVE_FOLDER
  
  SAVE_FOLDER = args.folder   # helpers.read_config()['config']['WIDE_FOLDER']
  #SIG_FOLDER = helpers.read_config()['config']['SIG_FOLDER']

  if not args.files is None:
    df = merge_files(args.files.split(','), args.index, args.how)
  else:
    if not args.csv2 is None:
      df1 = helpers.dal_read_df(args.folder, args.infile1, args.backend, args.dbname) # pd.read_parquet(f'{SAVE_FOLDER}/{args.infile1}.parquet')
      df2 = pd.read_csv(f'{SAVE_FOLDER}/{args.infile2}.csv')
      df2 = df2.set_index('Date')
    else:
      df1 = helpers.dal_read_df(args.folder, args.infile1, args.backend, args.dbname)
      df2 = helpers.dal_read_df(args.folder, args.infile2, args.backend, args.dbname)

      #df1 = pd.read_parquet(f'{SAVE_FOLDER}/{args.infile1}.parquet')
      #df2 = pd.read_parquet(f'{SAVE_FOLDER}/{args.infile2}.parquet')

    if args.cmp_tickers:
      if cmp_tickers(df1, df2):
        print(f'{args.infile1} and {args.infile2} have the same tickers')
      else:
        print(f'ERROR: {args.infile1} and {args.infile2} *do not* have the same tickers!')
        sys.exit(1)

    if not args.tickers is None:
      cols1 = df1.columns[list(map(lambda x: not re.search(f'^Date|^YearWeek|^({args.tickers})_.*', x) is None, df1.columns))]
      cols2 = df2.columns[list(map(lambda x: not re.search(f'^Date|^YearWeek|^({args.tickers})_.*', x) is None, df2.columns))]
      df1 = df1[cols1]
      df2 = df2[cols2]
      
    df = my_merge(df1, df2, args.index, args.how)

  df = df[sorted(list(df.columns))]
    
  helpers.dal_save_df(df, args.folder, args.outfile, args.backend, args.dbname)
  #  helpers.save_df(df, f'{SAVE_FOLDER}/{args.outfile}')
  
if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)
  main(args)
