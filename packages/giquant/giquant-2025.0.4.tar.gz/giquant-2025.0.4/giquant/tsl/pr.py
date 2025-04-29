#!/usr/bin/env python3

import re
import pandas as pd
import argparse

import giquant.tsl.helpers as helpers

bcolors = helpers.bcolors
pd.options.display.float_format = '{:,.2f}'.format

def print_cmdty(df_, cmdty_, cols_, colors, color_lims, color_cols, n=10, save_df=None):
  cols = df_.columns[list(map(lambda x: not re.search(f'^{cmdty_}.*({cols_})', x) is None, df_.columns))]
  df1 = df_.loc[:,cols]
  try:
    res = '\n'
    if df1.shape[1] > 0:
      color = ''
      df_col = df1
      if not color_cols is None:
        cols = df1.columns[list(map(lambda x: not re.search(color_cols, x) is None, df1.columns))]
        df_col = df1.loc[:,cols]
      if colors:
        if ((df_col.tail(1) <= -1*color_lims[2]) | (df_col.tail(1) >= color_lims[2])).all(axis=1).tolist()[0]:
          color = bcolors.OKCYAN
        if ((df_col.tail(1) <= -1*color_lims[1]) | (df_col.tail(1) >= color_lims[1])).all(axis=1).tolist()[0]:
          color = bcolors.OKBLUE
        if ((df_col.tail(1) <= -1*color_lims[0]) | (df_col.tail(1) >= color_lims[0])).all(axis=1).tolist()[0]:
          color = bcolors.OKGREEN
      res += f'{color}{df1.tail(n).T}{bcolors.ENDC}'
      if not save_df is None:
        df1.to_csv(f'./{save_df}.csv')
      res += '\n----'
    return res
  except Exception as e:
    print(f'ERROR: Check that all columns are numeric when using --colors')
    print(e)
    return ''

def print_summary(df_):
  return df_.to_string()
  
def create_args_parser():
  parser = argparse.ArgumentParser(prog='print.py', description='Print data from ind parquet files')
  parser.add_argument('folder',       help='Folder with tsl data.')
  parser.add_argument('files',        help='Parquet files (comma-separated) to look for commodity in')
  parser.add_argument('--tickers',    help='Commodity code (ZC etc.)')
  parser.add_argument('--vars',       help='Subset of variables (Net, Long, Short etc.)')
  parser.add_argument('--colors',     help='Colorize on/off. Default=on', action=argparse.BooleanOptionalAction, default=True)
  parser.add_argument('--color-lims', help='Comma separated list with limits for colors cyan/blue/green (default: 0.85,0.9,0.95)', default='0.85,0.9,0.95')
  parser.add_argument('--color-cols', help='Columns to aplly colors to. Default=all')
  parser.add_argument('--set-index',  help='Change index column before printing')
  parser.add_argument('--no-dates',   help='Number of dates to print per ticker', type=int, default=10)
  parser.add_argument('--save',       help='Save result in CSV-file', action=argparse.BooleanOptionalAction, default=False)
  parser.add_argument('--summary',    help='Summary files with one row per ticker and one column per varaible.', action=argparse.BooleanOptionalAction, default=False)
  parser.add_argument('--output_folder', help='Save summary of processing here', default='./output')
  parser.add_argument('--backend',    help='Backend to use. Supported are: parquet, duckdb and csv]', default='parquet')
  parser.add_argument('--dbname',     help='Name of database (used as filename for duckdb)', default='tsldb')
  return parser

def main(args):
  SAVE_FOLDER = args.folder
  OUTPUT_FOLDER = args.output_folder

  color_lims = list(map(float, args.color_lims.split(',')))
  files = args.files.split(',')
  vars_ = args.vars if not args.vars is None else ''

  res = ''
  for file in files:
    da = helpers.dal_read_df(args.folder, file, args.backend, args.dbname)

    if not args.summary:
      if args.tickers is None:
        cmtdys = list(set(list(map(lambda x: x.split('_')[0], da.columns))))
      else:
        cmtdys = args.tickers.split(',')

      if not args.set_index is None:
        da = da.set_index(args.set_index)

      res += f'==== {file} =====\n'
      for cmdty in cmtdys:
        res += print_cmdty(da, cmdty, vars_, args.colors, color_lims, args.color_cols, args.no_dates, cmdty if args.save else None)
        if args.save:
          res += f'Result saved in {cmdty}.csv.'
    else:
      res += print_summary(da)
  return res

if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)
  print(main(args))
