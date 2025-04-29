# Helpers
# =======

import re
import os
import sys
import yaml
import duckdb
import datetime
import numpy as np
import pandas as pd
import requests

from pathlib import Path
parent = Path(__file__).resolve().parent
CONFIG_PATH   = f'{parent}/../../config.yaml'


# Network
# ========

def dwnl_file(url, save_as):
  if url == '':
    return

  print('Download: ' + url + ' and save as: ' + save_as)

  r = requests.get(url, allow_redirects=True) 
  if(r.status_code == 200):
    with open(save_as, 'wb') as f:
        f.write(r.content)
  else:
    print('Unsucsessfull! Status code:' + r.status_code)

def dwnl_and_unzip(url, save_as, unzip_folder):
  #print('url', url, 'save_as', save_as, 'unzip_folder', unzip_folder)
  if os.path.isfile(save_as+'.zip'):
    os.remove(save_as+'.zip')

  dwnl_file(url, save_as+'.zip')

  print('Unzip to:' + unzip_folder)
  with zipfile.ZipFile(save_as+'.zip', 'r') as zip_ref:
      zip_ref.extractall(unzip_folder)

  os.remove(save_as+'.zip')

def save_df(df, path_):
#  if 'Date' in df.columns:
#    df['Date_dt'] = pd.to_datetime(df.Date, format='%Y%m%d')
  df.to_csv(f'{path_}.csv', index=True)
  print(f'\nResults saved in {path_}.csv')
  df.to_parquet(f'{path_}.parquet', index=True)
  print(f'Results saved in {path_}.parquet.')


# YAML files
# ==========

def read_yaml(filename):
  with open(f'{filename}.yaml', 'r') as file:
    co = yaml.safe_load(file)
  return co

def read_config():
  with open(CONFIG_PATH, 'r') as file:
    co = yaml.safe_load(file)
  return co

def read_strategy():
  with open(STRATEGY_PATH, 'r') as file:
    co = yaml.safe_load(file)
  return co

def shrink_dict0(opt2fut, dict_name):
  conf = helpers.read_config()
  d = conf[dict_name]
  futs = functools.reduce(add, list(map(lambda x: x.split(','), list(conf[opt2fut].values()))))
  to_del = set(list(d.keys())).difference(set(futs))
  for key in to_del:
    del d[key]
  return d

def shrink_dict(cols, d):
  to_del = set(list(d.keys())).difference(set(cols))
  for key in to_del:
    del d[key]
  return d

def shrink_ndarray(target_cols, src_cols, df1):
  # check for duplicates
  assert len(set(target_cols)) == len(target_cols)
  assert len(set(src_cols)) == len(src_cols)
  assert df1.shape[1] == len(src_cols)
  
  src_cols = list(map(lambda x: x.split('_')[0], src_cols))
  target_cols = list(map(lambda x: x.split('_')[0], target_cols))
  to_del = set(src_cols).difference(set(target_cols))
  idx_to_del = list(map(lambda x: src_cols.index(x), to_del))
  df1 = np.delete(df1, idx_to_del, 1)
  
  return df1

def strategy_tickers_re(strategy):
  strat = read_strategy()[strategy]
  conf = read_config()
  fut = ','.join(list(conf[strat['optcal2fut']].values()))
  return '|'.join(fut.split(','))



# Files and folders
# =================

def create_folder(folder):
  target_folder = os.path.expanduser(folder)
  if not os.path.isdir(target_folder):
    os.makedirs(target_folder)


# Dates
# =================

def dt2int(dt, format_='%Y%m%d'):
  return int(datetime.datetime.strftime(dt, format=format_))

def int2dt(dt, format_='%Y%m%d'):
  return datetime.datetime.strptime(str(dt), format_)

def month2date(dt, dayofmonth=1):
  return dt2int(datetime.datetime.strptime(str(dt*10+dayofmonth),'%Y%m%d'))
  
# 240329 - Change from %W to %V
def week2date(dt, dayofweek=1):
  return dt2int(datetime.datetime.strptime(str(dt*10+dayofweek),'%G%V%w'))

def date2week_(dt, format_='%Y%m%d'):
  return int(datetime.datetime.strftime(int2dt(dt, format_), format='%Y%V'))

def date2week(dt):
  return dt.isocalendar().year*100 + dt.isocalendar().week

def add_days(dt, n=7, format_='%Y%m%d'):
  return dt2int(int2dt(dt, format_) + datetime.timedelta(days = n))


# DataFrames
# =============

# dataframe must have the Date_dt column
def dt2YearWeek(df_, format_='%Y%m%d'):
  df_['Date'] = df_.index.map(lambda x: int2dt(x, format_))
  df_['YearWeek'] = df_.Date.dt.isocalendar().year*100 + df_.Date.dt.isocalendar().week
  df_ = df_.set_index('YearWeek')
  return df_


# Index must be time, ie. Date or YearWeek, and from_/to must adhere to the index
def filter_df(df, from_, to, variable, tickers):
  if not from_ is None:
    df = df.loc[from_:]

  if not to is None:
    df = df.loc[:to]

  df_var = df
  if not variable is None:
    sel = list(map(lambda x: not re.search(f'^.*({variable}).*', x) is None, df.columns))
    df_var = df.iloc[:,sel]

  if not tickers is None:
    sel = list(map(lambda x: not re.search(f'^{tickers}.*', x) is None, df_var.columns))
    df_var = df_var.iloc[:,sel]

  return df_var

# Like np.roll but first (or last) row(s) get a fill_value
def shift_elements(arr, num, fill_value):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


# Data Access "Layer"
# ==================

# tables cannot start with a number in duckdb
def fix_table_name(infile_):
  if infile_[0].isnumeric():
    infile_ = f'n{infile_}'
  return infile_

def dal_read_df(folder_, infile_, backend_, dbname_):
  if backend_ == 'parquet':
    df = pd.read_parquet(f'{folder_}/{infile_}.parquet')
    
  if backend_ == 'csv':
    df = pd.read_csv(f'{folder_}/{infile_}.csv')
    df = df.set_index(df.columns[0])
    
  if backend_ == 'duckdb':
    assert not dbname_ is None
    infile_ = fix_table_name(infile_)
      
    con = duckdb.connect(database = f'{folder_}/{dbname_}.duckdb', read_only = False)
    df = con.sql(f"SELECT * FROM {infile_}").df()
    con.close()

    # NOTE: This is not tested!!
    df = df.set_index(df.columns[0])

  return df

def dal_save_df(df_, folder_, outfile_, backend_, dbname_):
  if backend_ == 'parquet':
    df_.to_parquet(f'{folder_}/{outfile_}.parquet', index=True)
    print(f'Results saved in {folder_}/{outfile_}.parquet.')
    #save_df(df_, f'{folder_}/{outfile_}')
    
  elif backend_ == 'csv':
    df_.to_csv(f'{folder_}/{outfile_}.csv', index=True)
    print(f'Results saved in {folder_}/{outfile_}.csv.')

  elif backend_ == 'duckdb':
    assert not dbname_ is None
    outfile_ = fix_table_name(outfile_)
    
    df_ = df_.reset_index()
    path_ = f'{folder_}/{dbname_}.duckdb'
    con = duckdb.connect(database = path_, read_only = False)
    con.sql(f"DROP TABLE IF EXISTS {outfile_}; CREATE TABLE {outfile_} AS SELECT * FROM df_")
    con.close()
    print(f'Results saved in {path_}.')
    print(df_)

  else:
    print(f'Unknown backend {backend_}')


import datetime
import subprocess

def get_tables(TSLFOLDER_, TSLDBNAME_, TSLBACKEND_):
  res = None
  if TSLBACKEND_=='parquet':
    res = []
    for item in os.scandir(TSLFOLDER_):
      if item.name.split('.')[-1]=='parquet':
        res.append([item.name.removesuffix(".parquet"), item.stat().st_size, datetime.datetime.fromtimestamp(item.stat().st_atime)])
  elif TSLBACKEND_=='duckdb':
    res = subprocess.check_output(f'echo ".tables" | duckdb {TSLFOLDER_}/{TSLDBNAME_}.duckdb', shell=True).decode("utf-8")
    res = [ (x, '', '') for x in res.split() ]
  else:
    res = f'Backend {TSLBACKEND_} not supported'
  return res

def read_tsl(filename):
  f = open(filename, 'r')

  lines = f.readlines()
  res = {}

  name = ''
  script = ''
  for line in lines:
    line = line.strip()
    if line[0:4] == '#~~~':
      if name != '':
        res[name] = script
      line = line[4:]
      line = line.strip('~').strip()
      name = line
      script = ''
    elif len(line)>0 and line[0] == "#":
      continue
    else:
      script += line + '\n'

  return res

def read_tsl_(filename):
  f = open(filename, 'r')

  lines = f.readlines()
  res = {}

  name = ''
  script = ''
  for line in lines:
    line = line.strip()
    if line[0:4] == '#~~~':
      if name != '':
        parts = name.split(' ')
        name_ = parts[0].split(':')[0]
        script_args = {'type' : parts[0].split(':')[1]}
        for part in parts[1:]:
          script_args[part.split(':')[0]] = part.split(':')[1]
        script_args['script'] = script
        res[name_] = script_args
      line = line[4:]
      line = line.strip('~').strip()
      name = line
      script = ''
    elif len(line)>0 and line[0] == "#":
      continue
    else:
      script += line + '\n'

  return res


# Colors
# ======

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
