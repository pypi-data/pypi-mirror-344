import re
import os
import sys
import time
import argparse
import requests

import duckdb

import numpy as np
import pandas as pd
import polars as pl

from giquant.tsl.helpers import dal_save_df

BASE_URL = "https://apiservice.borsdata.se/v1"

ALL = 'bdall'
TALL = 'borsdata_tall'
WIDE = 'borsdata'
INSTR = 'bdinstr'
DUCKDB = 'borsdata.duckdb'
REPORTS = 'bdreports'
BASE_DATA = 'bdbasedata'

# Columns to save in the final table
COLS=[ 'year', 'yahoo',  'revenues', 'profit_Before_Tax',
       'current_Assets', 'non_Current_Assets', 'current_Liabilities', 'non_Current_Liabilities', 'tangible_Assets', 'total_Assets', 'total_Equity',
       'number_Of_Shares', 'earnings_Per_Share', 'dividend', 'profit_To_Equity_Holders',
       'stock_Price_Average', 'stock_Price_High', 'stock_Price_Low'
      ]

# Do not infer schema when combing report-csv files into one large file. Problem with implicit cast.
# Use explicit cast instead.
dtypes_ = {
  'year' : pl.Int64,
  'period' : pl.Int64,
  'revenues' : pl.Float64,
  'gross_Income' : pl.Float64,
  'operating_Income' : pl.Float64,
  'profit_Before_Tax' : pl.Float64,
  'profit_To_Equity_Holders' : pl.Float64,
  'earnings_Per_Share' : pl.Float64,
  'number_Of_Shares' : pl.Float64,
  'dividend' : pl.Float64,
  'intangible_Assets' : pl.Float64,
  'tangible_Assets' : pl.Float64,
  'financial_Assets' : pl.Float64,
  'non_Current_Assets' : pl.Float64,
  'cash_And_Equivalents' : pl.Float64,
  'current_Assets' : pl.Float64,
  'total_Assets' : pl.Float64,
  'total_Equity' : pl.Float64,
  'non_Current_Liabilities' : pl.Float64,
  'current_Liabilities' : pl.Float64,
  'total_Liabilities_And_Equity' : pl.Float64,
  'net_Debt' : pl.Float64,
  'cash_Flow_From_Operating_Activities' : pl.Float64,
  'cash_Flow_From_Investing_Activities' : pl.Float64,
  'cash_Flow_From_Financing_Activities' : pl.Float64,
  'cash_Flow_For_The_Year' : pl.Float64,
  'free_Cash_Flow' : pl.Float64,
  'stock_Price_Average' : pl.Float64,
  'stock_Price_High' : pl.Float64,
  'stock_Price_Low' : pl.Float64,
  'report_Start_Date' : pl.String,
  'report_End_Date' : pl.String,
  'broken_Fiscal_Year' : pl.Boolean,
  'currency' : pl.String,
  'currency_Ratio' : pl.Float64,
  'net_Sales' : pl.Float64,
  'report_Date' : pl.String
}


# Helpers
# -------

def save_pl_df(df_, folder_, file_, show_=False):
  df_.write_csv(f'{folder_}/{file_}.csv')
  df_.write_parquet(f'{folder_}/{file_}.parquet')

  con = duckdb.connect(f'{folder_}/{DUCKDB}')
  con.sql(f"CREATE OR REPLACE TABLE {REPORTS} AS SELECT * FROM df_;")
  con.close()

  if show_:
    print(f'Result saved to {folder_}/{file_}')

def get(func_):
  url = f"{BASE_URL}{func_}"
  r = requests.get(url)
  res = None
  if int(r.status_code)==200:
    res = r.json()
  else:
    print(f'ERROR {r.status_code}!')
    #sys.exit(1)
  return res


# Get Instruments
# ---------------

def get_all_instr(args):
  if args.apikey is None:
    print('--apikey is mandatory')
    sys.exit(1)

  df0 = pd.DataFrame(get(f"/instruments?authKey={args.apikey}")['instruments'])
  df1 = pd.DataFrame(get(f"/instruments/global?authKey={args.apikey}")['instruments'])
  df = pd.concat([df0, df1])
  #dal_save_df(df, args.folder, 'instr_all', args.backend, args.dbname)
  return df

def get_instr(args):
  res = None
  cnt_dbl = 0
  cnt = 0
  df = get_all_instr(args)
  #path_ = f'{args.folder}/{INSTR_CSV}'
  print(f'#tickers:{df.shape[0]}')
  df = pl.from_pandas(df)
  res = df

  save_pl_df(res, args.folder, INSTR, show_=True)
  get_sectors(args)
  return res


# Get Reports
# -----------

from pathlib import Path
import json
def get_reports(id, args):
  if args.apikey is None:
    print('--apikey is mandatory')
    sys.exit(1)
  url = f'/instruments/{id}/reports?authKey={args.apikey}&maxYearCount=20&maxR12QCount=40&original=0'
  if args.quarters:
    url = f'/instruments/{id}/reports/quarter?authKey={args.apikey}&maxYearCount=20&maxR12QCount=40&original=0'
  data = get(url)

  if args.save_json:
    Path(f'{args.folder}.json').mkdir(parents=True, exist_ok=True)
    with open(f'{args.folder}.json/{id}.json', 'w') as outfile:
      outfile.write(json.dumps(data))
    
  if not data is None:
    if not args.quarters:
      if args.R12:
        df = pd.DataFrame(data['reportsR12'])
      else:
        df = pd.DataFrame(data['reportsYear'])
    else:
      df = pd.DataFrame(data['reports'])
    path_ = f'{args.folder}/{id}.csv'
    df.to_csv(path_, index=False)
    print(f'Result saved to {path_}')
    return df
  else:
    print(f'Unable to fetch instrument {id}')
  return None

def get_all_reports(args):
  df = pl.read_csv(f'{args.folder}/{INSTR}.csv')
  df = df.filter(pl.col('insId')%2==args.even)
  cnt = 0
  for row in df.iter_rows():
    if cnt>0 and cnt%100==0:
      print(cnt, end='...', flush=True)
      time.sleep(5)
      
    df0 = get_reports(row[0], args)

    if cnt >= 9500:
      print(f'ERROR: Almost reached limit of 10k API calls! Exiting at insId:{row[0]}!')
      sys.exit(1)

    cnt += 1
  
def print_hist(col_, log_=False):
  col_ = col_.to_numpy()
  if log_:
    col_ = np.log(col_)
  col_ = np.nan_to_num(col_, nan=0, posinf=0, neginf=0)
  print(np.histogram(col_))

def check_reports(args):
  instr = pd.read_csv(f'{args.folder}/{INSTR_CSV}')
  files = [f for f in os.listdir(args.folder) if re.search(r'[1-9].*\.csv$', f)]
  instr_ids = set(instr.insId)
  files_ids = set(map(lambda x: int(x.removesuffix('.csv')), files))
  
  diff_ = instr_ids.symmetric_difference(files_ids)
  if len(diff_)!=0:
    print('Found these differences', diff_)
    print(f'In total ({len(diff_)} differences!')
  print(f'#instruments:{len(instr_ids)}')
  print(f'#files with reports:{len(files_ids)}')

  return diff_

def get_missing_reports(args):
  instr = pd.read_csv(f'{args.folder}/{INSTR}.csv')
  diff_ = check_reports(args)
  cnt = 0
  for insid in diff_:
    print(f'Fetching insid:{insid} ticker:{instr[instr.insId==insid]["yahoo"]}')
    if not get_reports(insid, args) is None:
      cnt += 1
  print(f'Fetched {cnt} reports out of {len(diff_)}')

def instr_ev(args):
  base_data = pl.read_csv(f'{args.folder_}/{BASE_DATA}.csv')
  instr = pl.read_csv(f'{args.folder}/{INSTR}.csv')
  df = instr.join(base_data, left_on='insId', right_on='Börsdata ID')
  df.sort(by='EV - Senaste', descending=True)
  save_pl_df(df, args.folder, f'{INSTR}_ev', show_=True)

  # Some stats
  print_hist(df['EV - Senaste'], log_=True)
  df0 = df.filter((pl.col('Info - Lista')!=pl.lit('NYSE')) & (pl.col('Info - Lista')!=pl.lit('Nasdaq')))
  print_hist(df0['EV - Senaste'], log_=True)
  return df
  
def tots0(folder_, quarters=False):
  #path_ = f'{folder_}/{ALL_CSV}'
  cnt = 0
  res = None
  files = [f for f in os.listdir(folder_) if re.search(r'[1-9].*\.csv$', f)]
  incorrect_files=[]
  if len(files)==0:
    print('ERROR: No report files found!')
    sys.exit(1)
  print(f'#files:{len(files)}')
  for f in files:
    if cnt>0 and cnt%100==0:
      print(cnt, end='...', flush=True)
      save_pl_df(res, folder_, ALL)
    try:
      df = pl.read_csv(f'{folder_}/{f}', infer_schema=False)
      if quarters:
        df = df.with_columns( (pl.col('year').cast(pl.Int32)*10 + pl.col('period').cast(pl.Int32) ).alias('year'))
    except:
      print(f'Error reading {f}!')
      incorrect_files.append(f)
      continue
    df = df.with_columns( pl.col('broken_Fiscal_Year').replace_strict( {'null':0, 'False':0, 'True': 1 },)
                          .cast(pl.Boolean))
    df = df.cast(dtypes_)
    df = df.with_columns(insId = pl.lit(int(f.removesuffix('.csv'))))
    df = df.with_columns(  pl.col('year')*10 +  pl.col('period'))           # JC, 250425 - allow multiple rows per year
    if res is None:
      res = df
    else:
      res = pl.concat([res, df])
    cnt += 1
  save_pl_df(res, folder_, ALL, show_=True)
  print(f'These files could not be read: {incorrect_files}!')
  return df

# Not used: crashed the memory!
def tots(args):
  if not args.use_cached_all:
    tots0(args.folder)
  else:
    print(f'Using cached {ALL}')
  df = pl.read_csv(f'{args.folder}/{ALL}.csv', infer_schema=True)
  instr = pl.read_csv(f'{args.folder}/{INSTR}.csv')
  print(f'shapes - {ALL}:{df.shape}, {INSTR}:{instr.shape}')
  df = df.join(instr.select(['insId','yahoo']), left_on='insID', right_on='insId')
  print(f'- joined:{df.shape}')
  df = df.select(COLS)
  save_pl_df(df, args.folder, 'borsdata0', show_=True)
  df.columns = list(map(lambda x: x.replace('_',''), df.columns))

  df = df.unpivot(index=['year','yahoo'])
  df = df.with_columns(pl.format("{}_{}", "yahoo", "variable").alias("on"))
  df = df.pivot(index='year'
                , on='on'              #get nice column names - ['yahoo','variable']
                , values='value'
                , aggregate_function='mean'
                , sort_columns=True)
  df = df.sort(by='year')
  
  #save_pl_df(df, f'{args.folder_}/borsdata.csv', show_=True)
  dal_save_df(df.to_pandas(), args.folder, WIDE, args.backend, args.dbname)

# Use less memory
def totall(args):
  if not args.use_cached_all:
    tots0(args.folder, quarters=args.quarters)
  else:
    print(f'Using cached {ALL}.csv')
  df = pl.read_csv(f'{args.folder}/{ALL}.csv', infer_schema=True)
  instr = pl.read_csv(f'{args.folder}/{INSTR}.csv')
  print(f'shapes - {ALL}.csv:{df.shape}, {INSTR}.csv:{instr.shape}')
  df = df.join(instr.select(['insId','yahoo']), left_on='insId', right_on='insId')
  print(f'- joined:{df.shape}')
  df = df.select(COLS)
  df.columns = list(map(lambda x: x.replace('_',''), df.columns))
  save_pl_df(df, args.folder, REPORTS, show_=True)

  print(f'MEMORY USAGE: {df.estimated_size(unit="mb")} MB')

  res = None
  cnt = 0
  print(f'shape:{df.shape}', flush=True)
  fyears = df['year'].unique()
  df = df.to_pandas()
  
  for fyear in fyears:
    if cnt%10 == 0:
      print(cnt, end='...', flush=True)

    df0 = df[df.year==fyear]
    df0 = df0.melt(id_vars=['year','yahoo'])
    df0 = df0.pivot_table(index=['yahoo','variable'], columns='year', values='value')
    df0 = df0.reset_index()
    cnt += 1

    if res is None:
      res = df0
    else:
      res = res.merge(df0, left_on=['yahoo','variable'], right_on=['yahoo','variable'], how='outer')

  res['key'] = res.yahoo.astype(str) + '_' + res.variable
  res = res.set_index('key')
  res = res[fyears]

  dal_save_df(res, args.folder, TALL, args.backend, args.dbname)


# Get prices
# ----------

def get_lastprice(args):
  if args.apikey is None:
    print('--apikey is mandatory')
    sys.exit(1)
  
  df = None
  data = get(f'/instruments/stockprices/last?authKey={args.apikey}')
  if not data is None:
    df = pd.DataFrame(data['stockPricesList'])
  else:
    print(f'Unable to fetch nordic stock prices')
    
  data = get(f'/instruments/stockprices/global/last?authKey={args.apikey}')
  if not data is None:
    df0 = pd.DataFrame(data['stockPricesList'])
    if df is None:
      df = df0
    else:
      df = pd.concat([df,df0])
  else:
    print(f'Unable to fetch global stock prices')
    
  path_ = f'{args.folder}/bdlast.csv'
  df.columns = list(map(lambda x: x.strip(), df.columns))
  df.to_csv(path_, index=False)
  print(f'Result saved to {path_}')

  instr = pd.read_csv(f'{args.folder}/bdinstr.csv')
  df = df.merge(instr[['insId','ticker', 'yahoo']], right_on='insId', left_on='i')
  df.columns = ['i','Date','High','Low','Close','Open','Volume','insId','ticker','yahoo']
  df = df[['Date','insId','ticker','yahoo','Open','High','Low','Close','Volume']]
  
  path_ = f'{args.folder}/bdlast_ticker.csv'
  df.to_csv(path_, index=False)
  print(f'Result saved to {path_}')
  
  return df


# Get Sectors etc
# ---------------

def gg(key):
  df = None
  data = get(f'/{key}?authKey={args.apikey}')
  if not data is None:
    df = pd.DataFrame(data[key])
  else:
    print(f'Unable to fetch {key}')

  path_ = f'{args.folder}/bd{key}.csv'
  df.to_csv(path_, index=False)
  print(f'Result saved to {path_}')
  

def get_sectors(args):
  if args.apikey is None:
    print('--apikey is mandatory')
    sys.exit(1)
  
  gg('branches')  
  gg('sectors')  
  gg('markets')  

  # insId,name,urlName,instrument,isin,ticker,yahoo,sectorId,marketId,branchId,countryId,listingDate,stockPriceCurrency,reportCurrency
  instr    = pd.read_csv(f'{args.folder}/{INSTR}.csv')
  branches = pd.read_csv(f'{args.folder}/bdbranches.csv')
  sectors  = pd.read_csv(f'{args.folder}/bdsectors.csv')
  markets  = pd.read_csv(f'{args.folder}/bdmarkets.csv')

  branches['branchName'] = branches.name
  sectors['sectorName'] = sectors.name
  markets['marketName'] = markets.name
  
  df = instr.merge(branches, left_on='branchId', right_on='id', suffixes=('','_y'))
  df = df.merge(sectors, left_on='sectorId', right_on='id', suffixes=('','_y'))
  df = df.merge(markets, left_on='marketId', right_on='id', suffixes=('','_y'))
  
  df = df[list(filter(lambda x: not (x.endswith('_y') or x=='id' or x=='isIndex'), df.columns))]

  save_pl_df(pl.from_pandas(df), args.folder, INSTR, show_=True)

  
  
# Main
# ===

def main(args):
  if args.action in ['instr','instr_ev','reports'] and args.apikey is None:
    print(f'ERROR: API Key must be specified for action {args.action}')
  
  if args.action=='instr':
    get_instr(args)
  elif args.action=='report':
    if args.insId is None:
      print('ERROR: insId is mandatory')
      sys.exit(1)
    get_reports(args.insId, args)
  elif args.action=='reports':
    get_all_reports(args)
  elif args.action=='check_reports':
    check_reports(args)
  elif args.action=='get_missing_reports':
    get_missing_reports(args)
  elif args.action=='instr_ev':
    instr_ev(args)
  elif args.action=='ts':
    tots(args)
  elif args.action=='tall':
    totall(args)
  elif args.action=='last':
    get_lastprice(args)
  elif args.action=='sectors':
    get_sectors(args)
  else:
    print(f'Unknown action {args.action}')

  
desc_ = 'Fetch fundamental data and prices from borsdata.se'
def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='borsdata.py', description=desc_)
  parser.add_argument('action',            help=f'What to do. instr_ev requires {BASE_DATA}.csv', choices=['instr','instr_ev','reports','check_reports','get_missing_reports','ts','tall','last','sectors','report'])
  parser.add_argument('folder',            help='Where to save the data')
  parser.add_argument('--apikey',          help='Börsdata API Key')
  parser.add_argument('--insId',           help='Börsdata Intrument ID')
  parser.add_argument('--use-cached-all',  help=f'Use exising {ALL}.csv (previously created by tots)', default=True, action=argparse.BooleanOptionalAction)
  parser.add_argument('--save-json',       help=f'Save full json data in <folder>.json', default=False, action=argparse.BooleanOptionalAction)
  parser.add_argument('--R12',             help=f'Use rolling 12 months of quarterly data', default=True, action=argparse.BooleanOptionalAction)
  parser.add_argument('--quarters',        help=f'Download and use data pre quarter', default=False, action=argparse.BooleanOptionalAction)
  parser.add_argument('--even',            help='Set to 0 or 1 (default). Download data for instruments Id that are even. Börsdata allows 10k API calls per day and has ~14k unique stocks.', type=int, default=1)
  parser.add_argument("--backend",
        help="Backends to use. Supported are: parquet, duckdb and csv (default=parquet).",
        default="parquet")
  parser.add_argument("--dbname",
        help="Name of database (used as filename in duckdb). default=tsldb",
        default="tsldb")
  return parser


if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)
  main(args)
