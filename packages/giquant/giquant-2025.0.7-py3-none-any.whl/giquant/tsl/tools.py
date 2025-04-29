import io
import re
import sys
import argparse

import numpy as np
import pandas as pd
import polars as pl

import giquant.tsl.merge as merge
from giquant.tsl.helpers import dal_read_df, dal_save_df


# filter
# ======

def filter(args):
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  print(f'infile shape:{df.shape}')
  df = df[df.index.str.contains(args.regex)]
  dal_save_df(df, args.folder, args.outfile, args.backend, args.dbname)
  print(f'outfile shape:{df.shape}')

def search(args):
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  print(f'infile shape:{df.shape}')
  df = df[df.index.str.contains(args.regex)]
  print('\n'.join(df.index.unique().tolist()))

def wide(args):
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  print(f'infile shape:{df.shape}')
  df = df.transpose()
  dal_save_df(df, args.folder, args.outfile, args.backend, args.dbname)
  print(f'outfile shape:{df.shape}')
  
def tall(args):
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  print(f'infile shape:{df.shape}')
  df = df.melt(id_vars=['year',args.index_col])

  dal_save_df(df, args.folder, args.outfile, args.backend, args.dbname)
  print(f'outfile shape:{df.shape}')

# TODO: remove this, have convert now!
def csv(args):
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  print(f'infile shape:{df.shape}')
  dal_save_df(df, args.folder, args.outfile, 'csv', args.dbname)

def name_index_col(args):
  if args.name is None:
    print('ERROR: --name is madatory in name_index_col')
    sys.exit(1)
  df = dal_read_df(args.folder, args.infile, args.backend, args.dbname)
  print(f'infile shape:{df.shape}')
  df.index.name = args.name
  dal_save_df(df, args.folder, args.outfile, args.backend, args.dbname)

def filter_main(args):
  print(args)
  if args.action=='filter':
    if args.regex is None:
      print('--regex must be specified')
      sys.exit(1)
    filter(args)
  elif args.action=='search':
    if args.regex is None:
      print('--regex must be specified')
      sys.exit(1)
    search(args)
  elif args.action=='tall':
    tall(args)
  elif args.action=='wide':
    wide(args)
  elif args.action=='csv':
    csv(args)
  elif args.action=='name_index_col':
    name_index_col(args)
  else:
    print(f'Unknown action {args.action}')

  
# csvtool
# ======
  
def read_stdin():
  input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
  d = input_stream.read()
  d = d.split('\n')
  res = []
  for l in d:
    l = l.replace('"','')
    res.append(tuple(l.split(args.sep)))
  df = pd.DataFrame(res)
  return df

def str2ints(s):
  return list(map(lambda x: int(x), s.split(',')))

def csvtool_main(args):
  df = read_stdin()
  df.columns = df.iloc[0]
  df = df.iloc[1:]
  if args.action=='getcols':
    if args.arg1 is None:
      print(f'ERROR: arg1 is mandatory for getcol!')
      sys.exit(1)

    df = df.iloc[:,str2ints(args.arg1)]

  elif args.action=='pivot':
    if args.index is None or args.columns is None or args.values is None:
      print(f'ERROR: index, columns and values are mandatory for pivot!')
      sys.exit(1)
    df = df.dropna()
    df = df.loc[df[args.index]!='']
    df = df.pivot_table(index=args.index, columns=args.columns, values=args.values, aggfunc='first')
    if not args.suffix is None:
      df.columns = list(map(lambda x: f'{x}_{args.suffix}', df.columns))
    df = df.reset_index()
  
  elif args.action=='melt':
    if args.id_vars is None or args.value_vars is None:
      print(f'ERROR: id_vars and value_vars are mandatory for melt!')
      sys.exit(1)
    df = pd.melt(df, id_vars=args.id_vars.split(','), value_vars=args.value_vars.split(','))
    
  elif args.action=='split':
    df[args.arg4] = df.loc[:,args.arg1].str.split(args.arg2, expand=True)[int(args.arg3)]
 
  elif args.action=='sum':
    df[args.arg2] =  pd.to_numeric(df[args.arg2] )
    df = df.groupby(args.arg1).agg( { args.arg2 : 'sum' }).reset_index()
    
  else:
    print(f'ERROR:Unknown action {args.action}')
    sys.exit(1)

  df.to_csv(sys.stdout, index=False)


# convert
# ========
  
def convert_main(args):
  print(args)
  from_format = args.infile.split('.')[-1]
  from_file   = '.'.join(args.infile.split('.')[:-1])
  
  to_format = args.outfile.split('.')[-1]
  to_file   = '.'.join(args.outfile.split('.')[:-1])
  
  print(f'Converting {from_file} in format {from_format} to {to_file} in format {to_format}')
  
  df = dal_read_df(args.folder, from_file, from_format, args.dbname)
  dal_save_df(df, args.folder, to_file, to_format, args.dbname)

  
# Main
# ====

filter_desc_ = 'Filter file/table and save in wide/time-series format'
def create_args_sub_parser_filter(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='filter.py', description=filter_desc_)
  parser.add_argument('folder',            help='Folder with  data')
  parser.add_argument('infile',            help='Input file/table')
  parser.add_argument('outfile',           help='Output file/table')
  parser.add_argument('action',            help='What to do', choices=['filter','wide','tall','search','csv','name_index_col'])
  parser.add_argument('--regex',           help='Regex for tickers to filter')
  parser.add_argument('--index_col',       help='Used in tall, default=yahoo', default='yahoo')
  parser.add_argument('--name',            help='Used in name_index_col')
  parser.add_argument("--backend",
        help="Backends to use. Supported are: parquet, duckdb and csv (default=parquet).",
        default="parquet")
  parser.add_argument("--dbname",
        help="Name of database (used as filename in duckdb). default=tsldb",
        default="tsldb")
  return parser

csvtool_desc_='Manipulate stdin csv-data and print to stdout.'
def create_args_sub_parser_csvtool(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='csvtool.py', description=csvtool_desc_)
  parser.add_argument('action',          help='Action: getcol.', choices=['getcols','pivot','melt','split','sum'])
  parser.add_argument('--arg1',          help='Action argument 1. getcol: comma seprated list of columns to get. split: column to split')
  parser.add_argument('--arg2',          help='Action argument 2. split: char to split on.')
  parser.add_argument('--arg3',          help='Action argument 3. split: index of item to get.')
  parser.add_argument('--arg4',          help='Action argument 4. split: name of new column.')
  parser.add_argument('--id_vars',       help='Comma separated column names. id_vars in melt')
  parser.add_argument('--value_vars',    help='Comma separated column names. value_vars in melt.')
  parser.add_argument('--index',         help='Column for index n pivot.')
  parser.add_argument('--columns',       help='Column to for columns in pivot.')
  parser.add_argument('--values',        help='Column for values in pivot.')
  parser.add_argument('--suffix',        help='Add suffix when doing pivot.')
  parser.add_argument('--sep',           help='separator', default=',')
  return parser

convert_desc_ = 'Convert between file formats using filename suffixes. Use <table>.duckdb for tables in DuckDb. '
def create_args_sub_parser_convert(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='convert.py', description=convert_desc_)
  parser.add_argument('folder',            help='Folder with  data')
  parser.add_argument('infile',            help='Input file/table')
  parser.add_argument('outfile',           help='Output file/table')
  parser.add_argument("--backend",
        help="Backends to use. Supported are: parquet, duckdb and csv (default=parquet).",
        default="parquet")
  parser.add_argument("--dbname",
        help="Name of database (used as filename in duckdb). default=tsldb",
        default="tsldb")
  return parser

def create_args_parser():
    parser = argparse.ArgumentParser(prog='tools.py', description='Misc GiQuant tools.')
    subparsers = parser.add_subparsers(help='GiQuant Command help.')

    parser_filter = subparsers.add_parser('filter', description=filter_desc_)
    parser_filter = create_args_sub_parser_filter(parser_filter)
    parser_filter.set_defaults(main=filter_main)

    parser_csvtool = subparsers.add_parser('csvtool', description=csvtool_desc_)
    parser_csvtool = create_args_sub_parser_csvtool(parser_csvtool)
    parser_csvtool.set_defaults(main=csvtool_main)

    parser_merge = subparsers.add_parser('merge', description=merge.desc_)
    parser_merge = merge.create_args_parser(parser_merge)
    parser_merge.set_defaults(main=merge.main)

    parser_convert = subparsers.add_parser('convert', description=convert_desc_)
    parser_convert = create_args_sub_parser_convert(parser_convert)
    parser_convert.set_defaults(main=convert_main)

    return parser
  
if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()

  if 'main' in args.__dict__.keys():
    args.main(args)
  else:
    print('Select an action: filter, csvtool, merge, convert')
