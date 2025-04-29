#!/usr/bin/env python3

import re
import os
import sys
import argparse
import pandas as pd

# TODO: should cleanup trade.helpers!!
from giquant.tsl.helpers import *

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='cc.py', description='Create continuous contract from parquet file with all contracts. Use the column with max Open Interest.')
  parser.add_argument('folder',       help='Save output here')
  parser.add_argument('infile',       help='Input file')
  parser.add_argument('outfile',      help='Save the result in')
  parser.add_argument('--cols',       help='Columns to include', default='Open,High,Low,Close,Volume,OpenInterest')
  parser.add_argument('--argmax_col', help='Column to use when selecting contract', default='OpenInterest')
  parser.add_argument('--backend',    help='Backends to use. Supported are: parquet, duckdb and csv]', default='parquet,csv')
  parser.add_argument('--dbname',     help='Name of database (used as filename in duckdb)', default='tsldb')

  args = parser.parse_args()
  print(args)

  cols = args.cols.split(',')
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  
  oi_cols = df.columns[list(map(lambda x: not re.search(args.argmax_col, x) is None, df.columns))]
  df['max_oi_col'] = df[oi_cols].idxmax(axis=1, skipna=True)
  df['max_oi_col'] = df.max_oi_col.apply((lambda x: x.split('_')[0]))

  res = []
  for idx, row in df.iterrows():
    ncols = list(map(lambda x: f'{row.max_oi_col}_{x}', cols))
    nrow = [idx] + row[ncols].values.tolist() + [row.max_oi_col]
    res.append(nrow)

  res = pd.DataFrame(res, columns=['Date']+cols+['Contract'])
  res['ticker'] = res.Contract.map(lambda x: x.split('-')[0])
  res['ticker'] = res.ticker.map(lambda x: x[0:(len(x)-3)])
  res = res.set_index('Date')
  
  dal_save_df(res, args.folder, args.outfile, args.backend, args.dbname)



