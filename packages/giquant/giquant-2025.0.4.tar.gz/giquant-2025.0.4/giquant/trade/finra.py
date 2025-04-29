#!/usr/bin/env python3

import os
import argparse
import requests

import pandas as pd

EXCHANGES = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']
BASE_URL  = 'https://cdn.finra.org/equity/regsho/daily/'

def main0(start_date, end_date, exchanges, sdir):
  x = pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y%m%d')
  print(f'Downloading dates: {x}')
  output_dir = sdir + '/' # format it up for writing to the correct Place
  postfix = '.txt'

  for exchange in exchanges:
    exchange_dir = output_dir + exchange + '/'
    print(exchange_dir)
    for idx in range(len(x)):
      url = ""
      pulldate = x[idx] # get the date to pull
      filename = exchange+'shvol'+pulldate+postfix  # CNMSshbvol20190101.txt
      url = BASE_URL + filename
      print(filename)
      r = requests.get(url)

      if r.status_code != 200:
        print('\t :: Error reading {}'.format(filename))
      else:
        s = requests.get(url).content
        f=open(exchange_dir+filename,'wb')
        f.write(s)
        f.close
  return

desc_ = 'Download short volume data from FINRA (www.finra.org)'

def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='finra.py', description=desc_)
  parser.add_argument('folder', help='Save the result in')
  parser.add_argument('start',  help='From date, YYYYmmdd')
  parser.add_argument('end',    help='To date, YYYYmmdd')
  return parser

def main(args):
  for exchange in EXCHANGES:
    try:
      path = os.path.join(output_dir, exchange)
      os.makedirs(path)
    except:
      print('Directorys exist')

  success = main0(args.start, args.end, EXCHANGES, args.folder)

if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)
  main(args)
