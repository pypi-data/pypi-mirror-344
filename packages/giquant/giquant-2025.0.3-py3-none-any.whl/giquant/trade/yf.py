#!/usr/bin/env python3
#
# Install/upgrade with: pip install yfinance --upgrade --no-cache-dir
#

import os
import argparse
import yfinance as yf


desc_='Download csv-files from yahoo-finance'

def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='yf.py', description=desc_)
  parser.add_argument('action',      help='ohlc,funda', choices=['ohlc','funda','info','sbx'])
  parser.add_argument('ticker_file', help='Files with tickers (one ticker per line)')
  parser.add_argument('output_path', help='Folder to save csv-files in.')
  return parser


def ohlc(tick, save_file):
  data = yf.download(tick) #, start="2000-01-01")
  data.to_csv(f'{save_file}.csv')

def funda(tick, save_file):
  meta = yf.Ticker(tick)
  meta.get_financials().to_csv(f'{save_file}-funda.csv')
  meta.earnings_history.to_csv(f'{save_file}-eps_hist.csv')
  meta.get_dividends().to_csv(f'{save_file}-dps.csv')
  meta.get_mutualfund_holders().to_csv(f'{save_file}-mfholders.csv')
  meta.get_balance_sheet().to_csv(f'{save_file}-bal.csv')

def info(tick, save_file):
  meta = yf.Ticker(tick)
  print(dir(meta))

def sbx(tick, save_file):
  meta = yf.Ticker(tick)
  print(dir(meta))

def main(args):
  file = open(args.ticker_file,'r')
  csv_path = os.path.expanduser(args.output_path)

  for tick in file.readlines():
    tick = tick.strip()
    save_file = f'{csv_path}/{tick}'
    print(tick, '(', save_file, ')')
    if args.action=='ohlc':
      ohlc(tick, save_file)
    elif args.action=='funda':
     funda(tick, save_file)
    elif args.action=='info':
     info(tick, save_file)
    elif args.action=='sbx':
     sbx(tick, save_file)
    else:
      print(f'Unknown actioin {args.action}')

      
if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)
  
  main(args)


# From: https://analyzingalpha.com/yfinance-python
#
#def history(self, period="1mo", interval="1d",
#            start=None, end=None, prepost=False, actions=True,
#            auto_adjust=True, back_adjust=False,
#            proxy=None, rounding=False, tz=None, timeout=None, **kwargs):
"""
    :Parameters:
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        prepost : bool
            Include Pre and Post market data in results?
            Default is False
        auto_adjust: bool
            Adjust all OHLC automatically? Default is True
        back_adjust: bool
            Back-adjusted data to mimic true historical prices
        proxy: str
            Optional. Proxy server URL scheme. Default is None
        rounding: bool
            Round values to 2 decimal places?
            Optional. Default is False = precision suggested by Yahoo!
        tz: str
            Optional timezone locale for dates.
            (default data is returned as non-localized dates)
        timeout: None or float
            If not None stops waiting for a response after given number of
            seconds. (Can also be a fraction of a second e.g. 0.01)
            Default is None.
        **kwargs: dict
            debug: bool
                Optional. If passed as False, will suppress
                error message printing to console.
 """


