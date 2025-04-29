#!/usr/bin/env python3

import os
import sys
import glob
import argparse
import zipfile
import requests
import datetime

from giquant.tsl.helpers import *


# Main
# ======

# Download cot data
# -----------------

def dwnl_file(url, save_as):
  if url == '':
    return

  print(f'Download: {url} and save as: {save_as}')

  r = requests.get(url, allow_redirects=True)
  if(r.status_code == 200):
    with open(save_as, 'wb') as f:
        f.write(r.content)
  else:
    print('Unsucsessfull! Status code:' + r.status_code)


def dwnl_and_unzip(url, save_as, unzip_folder):
  #print(f'url:{url}\n  save_as:{save_as}\n  unzip_folder:{unzip_folder}')
  if os.path.isfile(save_as+'.zip'):
    os.remove(save_as+'.zip')

  dwnl_file(url, save_as+'.zip')

  #print(f'Unzip to: {unzip_folder}')
  with zipfile.ZipFile(save_as+'.zip', 'r') as zip_ref:
      zip_ref.extractall(unzip_folder)

  os.remove(save_as+'.zip')


def url(cmdtys, date, opt):
  if cmdtys == 'disagg':
    return f'https://www.cftc.gov/files/dea/history/{"com" if opt else "fut"}_disagg_txt_{date.strftime("%Y")}.zip'
  elif cmdtys == 'fin':
    return f'https://www.cftc.gov/files/dea/history/{"com" if opt else "fut"}_fin_txt_{date.strftime("%Y")}.zip'
  elif cmdtys == 'dea':
    return f'https://www.cftc.gov/files/dea/history/dea{"histfo" if opt else "cot"}{date.strftime("%Y")}.zip'
  else:
    print('Unknown group', cmdtys)
    sys.exit(0)

def dwnl(cmdtys, date, opt):
  if cmdtys == 'disagg':
    create_folder(COT_DISAGG_FOLDER)
    folder = f'{COT_DISAGG_FOLDER}/{date.strftime("%Y")}'
  elif cmdtys == 'fin':
    create_folder(COT_FIN_FOLDER)
    folder = f'{COT_FIN_FOLDER}/{date.strftime("%Y")}'
  elif cmdtys == 'dea':
    create_folder(COT_DEA_FOLDER)
    folder = f'{COT_DEA_FOLDER}/{date.strftime("%Y")}'
  else:
    print('Unknown COT type:', cmdtys)
    sys.exit(0)

  create_folder(folder)
  target_folder = os.path.expanduser(folder)

  dwnl_and_unzip(url(cmdtys, date, opt),
                 target_folder,              # save_as filename
                 target_folder)              # unzip_folder


def dwnl_hist(cmdtys, opt=False):
  for dt in [datetime.datetime(yr,1,1) for yr in range(2010,TO_YEAR)]:
    dwnl(cmdtys, dt, opt)

def dwnl_current(cmdtys, opt=False):
  dwnl(cmdtys, datetime.datetime.now(), opt)

def main0(opt=False):
  dwnl_current('disagg', opt)
  dwnl_current('fin', opt)
  dwnl_current('dea', opt)

def main(args):
  global COT_DISAGG_FOLDER, COT_FIN_FOLDER, COT_DEA_FOLDER, SEP, CSV_PATH, FUT_ONLY_PREFIX, FUT_OPT_PREFIX 
  
  TO_YEAR = datetime.datetime.now().year #2024

  COT_DISAGG_FOLDER = f'{args.dest}/{args.da}'   # '~/aws-s3/gizur-trade-csv/fut-disagg'
  COT_FIN_FOLDER    = f'{args.dest}/{args.fin}'  # '~/aws-s3/gizur-trade-csv/fut-fin'
  COT_DEA_FOLDER    = f'{args.dest}/{args.dea}'  # '~/aws-s3/gizur-trade-csv/fut-dea'
  SEP               = args.sep                   # ','

  CSV_PATH        =  args.dest                   # '~/aws-s3/gizur-trade-csv'
  FUT_ONLY_PREFIX = args.fut_only_prefix         # ''
  FUT_OPT_PREFIX  = args.opt_prefix              # 'futopt/'

  def cot_disagg_folder(opt=False):
    return f'{CSV_PATH}/{FUT_ONLY_PREFIX if not opt else FUT_OPT_PREFIX}fut-disagg'

  def cot_fin_folder(opt=False):
    return f'{CSV_PATH}/{FUT_ONLY_PREFIX if not opt else FUT_OPT_PREFIX}fut-fin'

  def cot_dea_folder(opt=False):
    return f'{CSV_PATH}/{FUT_ONLY_PREFIX if not opt else FUT_OPT_PREFIX}fut-dea'

  #conf = read_config()
  #DISAGG = conf['cot']['disagg']
  #FIN = conf['cot']['fin']

  
  if args.dataset in ['cot', 'cotopt']:
    if args.dataset == 'cot':
      print('Update futures COT data')
      opt = False

    if args.dataset == 'cotopt':
      print('Update combined futures and options COT data')
      opt = True
      
    COT_DISAGG_FOLDER = cot_disagg_folder(opt)
    COT_FIN_FOLDER = cot_fin_folder(opt)
    COT_DEA_FOLDER = cot_dea_folder(opt)

    main0(opt)

  elif args.dataset in ['cothist', 'cotopthist']:
    if args.dataset == 'cothist':
      print('Downloading full COT Futures history')
      opt = False
    if args.dataset == 'cotopthist':
      opt = True
      print('Downloading full combined Futures and Options COT history')
    
    COT_DISAGG_FOLDER = cot_disagg_folder(opt)
    COT_FIN_FOLDER = cot_fin_folder(opt)
    COT_DEA_FOLDER = cot_dea_folder(opt)
     
    dwnl_hist('disagg', opt)
    dwnl_hist('fin', opt)
    dwnl_hist('dea', opt)
   
  else:
    print(f'ERROR: unknown dataset {args.dataset}')


desc_ = 'Download COT data.'

def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='cot.py', description=desc_)
  parser.add_argument('dataset', choices=['cot', 'cotopt', 'cothist', 'cotopthist'])
  parser.add_argument('dest')
  parser.add_argument('--da',              help='Folder for disaggregated COT reports. Default is fut-disagg', default='fut-disagg')
  parser.add_argument('--fin',             help='Folder for fiancial COT reports. Default is fut-fin',         default='fut-fin')
  parser.add_argument('--dea',             help='Folder for legacy COT reports. Default is fut-dea',           default='fut-dea')
  parser.add_argument('--fut_only_prefix', help='Prefix for futures only data. Default is none.',              default='')
  parser.add_argument('--opt_prefix',      help='Prefix for options data. Defaut is fut-opt/',                 default='fut-opt/')
  parser.add_argument('--sep',             help='Separator. Comma is default',                                 default=',')
  return parser
  
if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)

  main(args)


