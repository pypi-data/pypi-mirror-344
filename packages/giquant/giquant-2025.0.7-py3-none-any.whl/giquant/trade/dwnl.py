import sys
import argparse

import giquant.trade.yf as yf
import giquant.trade.cot as cot
import giquant.trade.fred as fred
import giquant.trade.finra as finra
import giquant.trade.mywrds as mywrds
import giquant.trade.borsdata as bd


def create_args_parser():
    parser = argparse.ArgumentParser(prog='dwnl.py', description='Download files.')
    subparsers = parser.add_subparsers(help='GiQuant Trade Download Command help.')

    parser_yf = subparsers.add_parser('yf', description=yf.desc_)
    parser_yf = yf.create_args_parser(parser_yf)
    parser_yf.set_defaults(main=yf.main)

    parser_cot = subparsers.add_parser('cot', description=cot.desc_)
    parser_cot = cot.create_args_parser(parser_cot)
    parser_cot.set_defaults(main=cot.main)

    parser_wrds = subparsers.add_parser('wrds', description=mywrds.desc_)
    parser_wrds = mywrds.create_args_parser(parser_wrds)
    parser_wrds.set_defaults(main=mywrds.main)

    parser_fred = subparsers.add_parser('fred', description=fred.desc_)
    parser_fred = fred.create_args_parser(parser_fred)
    parser_fred.set_defaults(main=fred.main)

    parser_finra = subparsers.add_parser('finra', description=finra.desc_)
    parser_finra = finra.create_args_parser(parser_finra)
    parser_finra.set_defaults(main=finra.main)

    parser_bd = subparsers.add_parser('borsdata', description=bd.desc_)
    parser_bd = bd.create_args_parser(parser_bd)
    parser_bd.set_defaults(main=bd.main)

    return parser


def main(args):
    if bool(set(['main']) & set(args.__dict__.keys())):
      args.main(args)
    else:
        print('Please select a program to run: borsdata,cot,finra,fred,wrds,yf')

if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()
    print(args)
    main(args)





