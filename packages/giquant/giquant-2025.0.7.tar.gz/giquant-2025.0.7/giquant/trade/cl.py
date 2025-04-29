#!/usr/bin/env python3
#
# 240407
#
# TODO: In need to cleanup! A lot of duplication (in main & get_cals).
#

__author__ = 'Jonas Colmsjö'

import sys
import datetime
import argparse

import numpy as np
import pandas as pd

# TODO: should cleanup trade.helpers!!
from giquant.tsl.helpers import *


FROM = dt2int(datetime.date.today() - datetime.timedelta(days=(30*365.24)))
TO   = dt2int(datetime.date.today() + datetime.timedelta(days=(5*365.24)))

CONTRACT_CODE2MONTH = {'F':1, 'G':2, 'H':3, 'J':4, 'K':5,  'M':6, 'N':7, 'Q':8, 'U':9, 'V':10, 'X':11, 'Z':12}

# Number of expirations
NO_EXP = 4
COLUMNS = list(map(lambda x: f'{x[0]}{x[1]}', list(zip(['exp']*NO_EXP, range(1,NO_EXP+1)))))

# Skip this and use get_cals + get_exps below?
# --------------------------------------------

def get_cal(contract, grp_ccode):
  grp_ccode = {k: v.split(',') for k,v in grp_ccode.items()}
  grp = None
  for k in grp_ccode.keys():
    if contract in grp_ccode[k]:
      grp = k
  return grp

def get_exp(ccode_, conf_file='contracts', cals_='calF', src_='sc'):
  if src_=='sc':
    root_contract = ccode_[0:2]
    year = int(ccode_[3:5])
    if year < 50:
      year = 2000 + year
    else:
      year = 1900 + year
    exp_code = ccode_[2:3]
  elif src=='ng':
    print('NOT IMPLEMENTED!')
    sys.exit(1)
  else:
    print(f'Unknown source: {src_}')

  print(root_contract, year, exp_code)
  yaml_ = read_yaml(conf_file)
  cal = get_cal(root_contract, yaml_[f'{cals_}_fut'])

  cals = yaml_[cals_]
  dts =  pd.DataFrame(pd.date_range(str(year), str(year+1), freq=cals[cal]['freq']), columns=['exp'])

  # NOTE: should not be necessary if freq was correct. Need to approx. sometime though.
  dts['contract_code'] = dts.exp.map(lambda x: list(CONTRACT_CODE2MONTH.keys())[x.month-1])
  if not cals[cal]['months'] is None:
    dts['check'] = dts.contract_code.map(lambda x: x in cals[cal]['months'])
    dts = dts[dts.check]

  dts.exp = dts.exp.map(dt2int)
  dts['year'] = dts.exp // 10000

  return dts.loc[dts.contract_code==exp_code]['exp'].values[0]


# Get expirations for all root symbols in a calendar 
# --------------------------------------------------

def get_cals(conf):
  l  = [ (k,v.split(',')) for k,v in conf.items()]
  res = []
  for i in l:
    for j in i[1]:
      res.append( (i[0],j) )
  return pd.DataFrame(data=res, columns=['cal','root_symbol'])

def get_exps(conf_file, cals_, from_, to_):
  yaml_ = read_yaml(conf_file)
  cals = yaml_[cals_]  
  res = None
  for cal in cals:
    dts =  pd.DataFrame(pd.date_range(str(from_), str(to_), freq=cals[cal]['freq']), columns=['exp'])

    # NOTE: should not be necessary if freq was correct. Need to approx. sometime though.
    dts['contract_code'] = dts.exp.map(lambda x: list(CONTRACT_CODE2MONTH.keys())[x.month-1])
    if not cals[cal]['months'] is None:
      dts['check'] = dts.contract_code.map(lambda x: x in cals[cal]['months'])
      dts = dts[dts.check]

    dts.exp = dts.exp.map(dt2int)
    dts['year'] = dts.exp // 10000
    dts['cal'] = cal

    if res is None:
      res = dts
    else:
      res = pd.concat([res, dts], axis=0)

  res = res.merge(get_cals(yaml_[f'{cals_}_fut']), left_on='cal', right_on='cal')
  
  assert (res['check']==True).all()
  del res['check']
  
  return res


# Main
# =====

def main2(args):
  return main(args.folder, args.config, args.cals, args.from_, args.to, args.backend, args.outfile, args.dbname, no_exp_)

def main(save_folder_, config_, config_cal_, from_, to_, backend_,  outfile_, dbname_, no_exp_):
  SAVE_FOLDER = save_folder_         # args.folder
  yaml_ = read_yaml(config_)         # read_yaml(args.config)

  cals = yaml_[config_cal_]          # yaml_[args.cals]

  df1 = pd.DataFrame(pd.date_range(start=str(from_), end=str(to_)), columns=['Date'])
  
  df1 = df1.set_index('Date')
  df1.index = df1.index.map(dt2int)
  
  df = None
  df_cal = None
  for cal in cals:
    dts =  pd.DataFrame(pd.date_range(str(FROM), str(TO), freq=cals[cal]['freq']), columns=['exp'])

    # NOTE: should not be necessary if freq was correct. Need to approx. sometime though.
    dts['contract_code'] = dts.exp.map(lambda x: list(CONTRACT_CODE2MONTH.keys())[x.month-1])
    if not cals[cal]['months'] is None:
      dts['check'] = dts.contract_code.map(lambda x: x in cals[cal]['months'])
      dts = dts[dts.check]

    dts.exp = dts.exp.map(dt2int)
    dts['year'] = dts.exp // 10000
    for backend in backend_.split(','):        # args.backend.split(','):
      dal_save_df(dts[['year','contract_code','exp']], save_folder_, f'{cal}_{outfile_}', backend, dbname_)

    dts['cal'] = cal
    if df_cal is None:
      df_cal = dts[['cal','year','contract_code','exp']].copy()
    else:
      df_cal = pd.concat([df_cal, dts[['cal','year','contract_code','exp']].copy() ], axis=0)
    
    res = []
    for i in range(0, dts.shape[0] - no_exp_):
      row = list(dts.iloc[i:i+no_exp_].exp)
      row.insert(0, row[0])
      res.append(row)

    res = pd.DataFrame(res, columns=['Date']+list(map(lambda x: f'{cal}_{x}', COLUMNS)))
    res = res.set_index('Date')

    df1 = df1.loc[0:res.iloc[-1].name]
    res = res.loc[0:df1.iloc[-1].name]
    df1 = df1.loc[0:res.iloc[-1].name]
    
    res = res.merge(df1, how='outer', left_index=True, right_index=True)
    for col in res.columns:
      res[col] = res[col].bfill()
      #res[col] = res[col].fillna(method='bfill')

    if df is None:
      df = res
    else:
      df = df.merge(res, right_index=True, left_index=True, how='inner')
      
  df = df.astype(int)

  return df, df_cal

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='cl.py', description='Calculate futures and options expiration calendar')
  parser.add_argument('cals',     help='Calendar group (in contracts.yaml)')
  parser.add_argument('folder',   help='Folder to save calendar in.')
  parser.add_argument('outfile',  help='Where to save the calendar')
  parser.add_argument('--from_',  help='From date (Ymd)', type=int, default=FROM)
  parser.add_argument('--to',     help='To date (Ymd)', type=int, default=TO)
  parser.add_argument('--no_exp', help='Number of expirations', type=int, default=NO_EXP)
  parser.add_argument('--src',    help='ng=NorgateData, sc=SierraChart', default='ng')
  parser.add_argument('--config', help='Yaml file with contracts', default='contracts')
  parser.add_argument('--backend',    help='Backends to use. Supported are: parquet, duckdb and csv]', default='parquet,csv')
  parser.add_argument('--dbname',     help='Name of database (used as filename in duckdb)', default='tsldb')

  args = parser.parse_args()
  print(args)

  df, df_cal = main2(args)
  print(df_cal)
  
  for backend in args.backend.split(','):
    dal_save_df(df, args.folder, args.outfile, backend, args.dbname)
    
  #helper.save_df(df, f'{SAVE_FOLDER}/{args.outfile}')
