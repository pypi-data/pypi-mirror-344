import sys
import argparse
import pandas as pd

from sqlalchemy import *


desc_='Query database with sql-like code. SQLAlchemy Core is used to run the code.'

def create_args_parser(parser=None):
  if parser is None:
    parser = argparse.ArgumentParser(prog='sql.py', description=desc_)
  parser.add_argument('folder',      help='Location of database file')
  parser.add_argument('tables',      help='Comma separated list of tables that are used in the sql')
  parser.add_argument('outfile',     help='Where to save the result')
  parser.add_argument('sql',         help='sql-code to run')
  parser.add_argument('--backend',   help='Comma separated list with backends to use. Only duckdb is supported at the moment.', default='duckdb')
  parser.add_argument('--dbname',    help='Name of database (used as filename in duckdb)', default='tsldb')
  parser.add_argument('--outformat', help='Format for outfile. csv and parquet is supported.', choices=['csv','parquet'], default='csv')
  return parser

def main(args):
  global metadata, engine, conn
  
  if args.backend == 'duckdb':
    if args.folder is None:
      print(f'ERROR: --folder must be specified with the duckdb backend!')

    conn_str = f'duckdb:///{args.folder}/{args.dbname}.duckdb'
    metadata = MetaData()
    engine = create_engine(conn_str, echo=False)
    conn = engine.connect()
    print(f'Using {conn_str}')

    for table in args.tables.split(','):
      py = f'{table} = Table("{table}", metadata, autoload_with=engine);'
    
    py += f's = "{args.sql}";'
    py += 'rp = conn.execute(text(s));'
    py += 'res = rp.fetchall();'
    py += 'df = pd.DataFrame(res, columns=rp.keys());'

    print(py)
    exec(py, globals())

    if args.outformat=='csv':
      df.to_csv(f'{args.outfile}.csv', index=True)

    if args.outformat=='parquet':
      df.to_parquet(f'{args.outfile}.parquet', index=True)

    return df

  else:
    print(f'ERROR: Unknown backend {args.backend}')
    sys.exit(1)

if __name__ == '__main__':
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)

  df = main(args)
  print(df)
