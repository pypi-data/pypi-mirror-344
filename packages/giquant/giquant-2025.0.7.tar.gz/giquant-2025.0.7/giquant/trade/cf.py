import re
import sys
import glob
import math
import argparse
import datetime

import giquant.trade.cl
from giquant.tsl.helpers import *


def create_args_parser():
    parser = argparse.ArgumentParser(
        prog="cf.py",
        description="Create Forward. Create futures time series with forward contracts using a calendar",
    )
    parser.add_argument("price_folder", help="Folder with SierraChart price files.")
    parser.add_argument("tsl_folder", help="Folder with tsl data.")
    parser.add_argument(
        "outfile", help="Name of output (parquet/csv-file or duckdb table)"
    )
    parser.add_argument(
        "--backends",
        help="Comma separated list with backends to use. Supported are: parquet, duckdb and csv (default=parquet,csv).",
        default="parquet,csv",
    )
    parser.add_argument(
        "--dbname",
        help="Name of database (used as filename in duckdb). default=tsldb",
        default="tsldb",
    )
    parser.add_argument(
        "--config", help="Yaml file with contracts (default=contracts)", default="contracts"
    )
    parser.add_argument(
        "--symbols", help="Symbols to include. Default is all.", default=""
    )
    parser.add_argument("--cal", help="Calendar group in config file (default=calF)", default="calF")
    parser.add_argument(
        "--years_back", help="Maximum number of years history to inclucde (default=30)", default=30, type=int
    )
    parser.add_argument(
        "--years_forward", help="Maximum number of future year deliveries to include (default=5)", default=5, type=int
    )
    parser.add_argument(
        "--file_naming", help="File naming approach. For SierraChart use:'{root_symbol}{month}{yy}*.dly', For NorgateData use:{root_symbol}-{yyyy}{month}.csv",
        default='{root_symbol}{month}{yy}*.dly'
    )

    return parser


def create_all_contract_months(
        price_folder, df_cal, from_dt, to_dt, root_symbols_to_incl, glob_pattern
):
    df_res = None
    for root_symbol in df_cal.root_symbol.unique():
        if (
            not root_symbols_to_incl == ""
            and not root_symbol in root_symbols_to_incl.split(",")
        ):
            continue

        print(f"{root_symbol}...", end="", flush=True)
        months = df_cal[df_cal.root_symbol == root_symbol].contract_code.unique()
        for month in sorted(months):
            df_cal_sel = df_cal[
                (df_cal.root_symbol == root_symbol) & (df_cal.contract_code == month)
            ]
            i = 1
            while i < df_cal_sel.shape[0]:
                year = df_cal_sel.iloc[i].year
                year2 = year % 100
                
                #if glob_pattern.find('{yy}') > 0:
                if glob_pattern.find('02d') > 0:
                  year = year2
                
                sel_from_dt = int2dt(df_cal_sel.iloc[i - 1].exp) + datetime.timedelta(
                    days=1
                )
                sel_to_dt = int2dt(df_cal_sel.iloc[i].exp)
                i += 1

                # NOTE: ugly hack!! apply f-string dynamically using eval
                filename = r"{price_folder}/" + glob_pattern
                filename = eval(f'f{filename!r}')
                files = glob.glob(filename)

                if len(files) == 0:
                    continue
                if len(files) > 1:
                    print(f"ERROR: found several files matching {filename} ({files})")
                    sys.exit(1)

                df_ = pd.read_csv(files[0], parse_dates=["Date"])
                df_.columns = list(map(lambda x: x.replace(' ',''), df_.columns))
                
                if df_.shape[0] == 0 or df_.isna().all().all():
                    continue

                df_.columns = list(map(lambda x: x.strip(), df_.columns))
                df_["symbol"] = f"{root_symbol}{month}{year2}"
                df_["ContSymbol"] = f"{root_symbol}{month}"
                df_ = df_[(df_.Date >= sel_from_dt) & (df_.Date <= sel_to_dt)]

                #print(df_cal_sel.iloc[i].year)
                #print(year)
                #print(filename)
                #print(files)
                #print(df_)
                #sys.exit(1)

                if df_.shape[0] == 0:
                    print(f"WARNING: Empty file {filename}")
                    continue
                if df_res is None:
                    df_res = df_
                else:
                    df_res = pd.concat([df_res, df_], axis=0, ignore_index=True)

    if df_res is None:
        print("Empty res")
        return pd.DataFrame()

    df_ = df_res.melt(
        id_vars=["Date", "ContSymbol"],
        value_vars=["Open", "High", "Low", "Close", "Volume", "OpenInterest"],
    )
    df_.Date = df_.Date.map(dt2int)
    df_ = df_.pivot(
        index=["Date"], columns=["ContSymbol", "variable"], values=["value"]
    )
    df_.columns = df_.columns.to_series().str.join("_")
    df_.columns = list(map(lambda x: x.removeprefix("value_"), df_.columns))
    df_ = df_[df_.columns.sort_values()]
    return df_


def add_front_contract(df_, tickers):
    df_res = None
    for ticker in tickers:
        print(ticker, end="...", flush="True")
        sel = df_.columns[
            list(
                map(
                    lambda x: not re.search(f"{ticker}._Volume", x) is None, df_.columns
                )
            )
        ]
        df0 = df_[sel]
        if df0.shape[1] == 0:
            print(f"Ticker {ticker} has no data (ie. no columns named {ticker}_.*)")
            continue

        idx = df0.index[df0.isnull().all(1)]
        if len(idx) != 0:
            print(f"There are rows with all NaNs:{df0.columns} {df0.loc[idx].shape} {idx}")

        df0.columns = list(map(lambda x: x.split("_")[0], df0.columns))
        pd.options.mode.chained_assignment = None
        df0.loc[:, f"{ticker}_Maxvol"] = df0.idxmax(axis="columns", skipna=True)

        if df_res is None:
            df_res = df0[f"{ticker}_Maxvol"]
        else:
            df_res = pd.concat([df_res, df0[f"{ticker}_Maxvol"]], axis=1)

    df_res = pd.concat([df_, df_res], axis=1)
    return df_res


def check_valid_roll(from_to, month_codes):
    res = False
    if (
        from_to[0] == ""
        or from_to[1] == ""
        or from_to[0] == "nan"
        or from_to[1] == "nan"
        or pd.isna(from_to[0])
        or pd.isna(from_to[1])
    ):
        res = True
    else:
        from_ = from_to[0][-1]
        to_ = from_to[1][-1]
        if from_ == month_codes[-1] and to_ == month_codes[0]:
            res = True
        elif from_ == to_:
            res = True
        else:
            idx_from = month_codes.index(from_)
            if idx_from == len(month_codes) - 1:
                res = False
            res = (idx_from + 1) < len(month_codes) and month_codes[idx_from + 1] == to_

    return res

def add_cont_contract(df_, root_symbols):
    for root_symbol in root_symbols:
        print(f"{root_symbol}", end="...", flush=True)
        cols = df_.columns[
            list(
                map(
                    lambda x: not re.search(f"^{root_symbol}._Volume", x) is None,
                    df_.columns,
                )
            )
        ]
        month_codes = sorted(list(map(lambda x: x.split("_")[0][-1], cols)))

        sel = df_.columns[
            list(
                map(
                    lambda x: not re.search(f"{root_symbol}_(Maxvol|ValidRoll)", x)
                    is None,
                    df_.columns,
                )
            )
        ]
        df0 = df_[sel]
        if df0.shape[1] == 0:
            continue
        i = 0
        for idx, row in df0.iterrows():
            if i == 0:
                df_.loc[idx, f"{root_symbol}_CC"] = (
                    row[f"{root_symbol}_Maxvol"]
                    if not pd.isna(row[f"{root_symbol}_Maxvol"])
                    else ""
                )
            else:
                valid_roll = check_valid_roll(
                    (prev_row, row[f"{root_symbol}_Maxvol"]), month_codes
                )
                df_.loc[idx, f"{root_symbol}_ValidRoll"] = valid_roll
                df_.loc[idx, f"{root_symbol}_CC"] = (
                    (
                        row[f"{root_symbol}_Maxvol"]
                        if not pd.isna(row[f"{root_symbol}_Maxvol"])
                        else ""
                    )
                    if valid_roll
                    else prev_row
                )
            i += 1
            prev_row = (
                df_.loc[idx, f"{root_symbol}_CC"]
                if not pd.isna(df_.loc[idx, f"{root_symbol}_CC"])
                else ""
            )
    return df_

def new_col_names(x):
    contract, var = x.split('_')
    return f"{contract[:-1]}_{var}"

def create_cc_df(df_, root_symbols):
    df_res = pd.DataFrame(index=df_.index)
    for root_symbol in root_symbols:
        print(root_symbol, end='...', flush=True)
        sel = df_.columns[list(map(lambda x: not re.search(f"^{root_symbol}(.|)_.*", x) is None, df_.columns))]
        df0 = df_[sel]
        contract = prev_contract = None
        for idx, row in df0.iterrows():
            if not f'{root_symbol}_CC' in row:
                continue
            contract = row[f'{root_symbol}_CC']
            if contract is None or len(contract)==0:
                continue
            cols = row.index[list(map(lambda x: not re.search(f'{contract}_.*',x) is None, row.index))].tolist()
            new_cols = list(map(new_col_names, cols))
            df_res.loc[idx,new_cols] = row[cols].values
            df_res.loc[idx,f"{root_symbol}_roll"] = (contract!=prev_contract)*1
            prev_contract = contract
        # defragment df
        df_res = df_res.copy()
    return df_res


def main(args):
    from_dt = dt2int(
        datetime.date.today() - datetime.timedelta(days=(args.years_back * 365.24))
    )
    to_dt = dt2int(
        datetime.date.today() + datetime.timedelta(days=(args.years_forward * 365.24))
    )

    df_cal = giquant.trade.cl.get_exps(args.config, args.cal, from_dt, to_dt)

    # parse file_naming string and create glob-pattern for the price files
    valid_tokens = [r'{root_symbol}',r'{month}',r'{yy}',r'{yyyy}',r'-',r'_',r'*',r'.csv',r'.dly']
    s,res,found_token = args.file_naming, [], True
    while found_token and len(s) > 0:
        found_token = False
        for token in valid_tokens:
            if s.startswith(token):
                res.append(token)
                found_token = True
                s = s[len(token):]
                continue

    if not found_token:
        print(f'ERROR: file_naming {args.file_naming} not supported! Parse failed at {s}')
        sys.exit(1)
    
    glob_pattern = r''
    for part in res:
        if part=='{yy}':
            glob_pattern += r'{year:02d}'
        elif part=='{yyyy}':
            glob_pattern += r'{year:04d}'
        else:
            glob_pattern += part
    df = create_all_contract_months(
        args.price_folder, df_cal, from_dt, to_dt, args.symbols, glob_pattern
    )
    symbols = df_cal.root_symbol.unique()
    if args.symbols != "":
        symbols = list(set(symbols).intersection(set(args.symbols.split(","))))

    df = add_front_contract(df, symbols)
    df = add_cont_contract(df, symbols)
    df_cc = create_cc_df(df, symbols)

    df = df[sorted(df.columns)]
    df_cc = df_cc[sorted(df_cc.columns)]
    #df.index.names = ["Date"]

    for backend in args.backends.split(","):
        dal_save_df(df, args.tsl_folder, args.outfile, backend, args.dbname)
        dal_save_df(df_cc, args.tsl_folder, f"{args.outfile}_cc", backend, args.dbname)


if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()
    print(args)

    main(args)
