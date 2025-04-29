import sys
import argparse

import giquant.tsl.gg as gg
import giquant.tsl.sql as sql
import giquant.tsl.expr as expr
import giquant.tsl.helpers as helpers

def create_args_sub_parser(parser):
    parser.add_argument('tslfile',      help='File with tsl-code.')
    parser.add_argument('script',       help='Name of script to run in tsl-file.')
    parser.add_argument('--folder',     help='Folder with tsl data.')
    parser.add_argument('--infile',     help='Parquet/CSV-file or table with data')
    parser.add_argument('--outfile',    help='Parquet/CSV-file or table to store the result')
    parser.add_argument('--parse-only', help='Only parse the input and show tokens in postfix notation.',
                        action=argparse.BooleanOptionalAction, default=False) 
    parser.add_argument('--debug',      help='Print debug messages', action=argparse.BooleanOptionalAction, default=False) 
    parser.add_argument('--py',         help='Python file to import. Functions that can be used in FUNC items (as part of expressions)')
    parser.add_argument('--yaml',       help='YAML file to import. Load dicts that can be used in items (as part of expressions)')
    parser.add_argument('--backend',    help='Backend to use. Supported are: parquet, duckdb and csv]', default='parquet')
    parser.add_argument('--dbname',     help='Name of database (used as filename for duckdb)', default='tsldb')
    return parser

def create_args_parser():
    parser = argparse.ArgumentParser(prog='run.py', description='Run GiQuant command.')
    subparsers = parser.add_subparsers(help='GiQuant Command help.')

    parser_tsl = subparsers.add_parser('tsl', description='Run tsl-file. See help for expr,gg and sql for details.')
    parser_tsl = create_args_sub_parser(parser_tsl)
    parser_tsl.set_defaults(main=main)

    parser_expr = subparsers.add_parser('expr', description=expr.desc_, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_expr = expr.create_args_parser(parser_expr)
    parser_expr.set_defaults(main=expr.main)

    parser_gg = subparsers.add_parser('gg', description=gg.desc_, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_gg = gg.create_args_parser(parser_gg)
    parser_gg.set_defaults(main=gg.main)

    parser_sql = subparsers.add_parser('sql', description=sql.desc_, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_sql = sql.create_args_parser(parser_sql)
    parser_sql.set_defaults(main=sql.main)

    return parser

from argparse import Namespace

def main(args):
    tsl = helpers.read_tsl_(args.tslfile)
    if args.script not in tsl:
        print(f'ERROR: {args.script} not found in {args.tslfile}!')
        sys.exit(1)
    tsl = tsl[args.script]

    args_ = dict(args.__dict__)
    for key in tsl.keys():
        argv = tsl[key]
        if key=='script':
            args_['stmts'] = argv
        elif not argv is None and key!='type':
            args_[key] = argv

    args_ = Namespace(**args_)
    print(args_)
    if tsl['type'] == 'expr':
        expr.main(args_)
        pass
    elif tsl['type'] == 'gg':
        pass
    elif tsl['type'] == 'sql':
        pass
    else:
        print(f'Unknown script type {args.type}')
    
if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()
    print(args)

    if 'main' in args.__dict__.keys():
        args.main(args)
    else:
        print('Select an action: tsl, expr, gg, sql')


