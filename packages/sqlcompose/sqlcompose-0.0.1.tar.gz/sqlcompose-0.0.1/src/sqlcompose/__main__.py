from os import path
from sys import exit
from argparse import ArgumentParser

from sqlcompose.core.functions import load, loads


def main():
    try:
        parser = ArgumentParser(prog = "sqlcompose")
        parser.add_argument("input", type=str, help = "SQL expression or location of an SQL file")
        pargs = parser.parse_args()

        if path.isfile(pargs.input):
            sql = load(pargs.input)
        else:
            sql = loads(pargs.input)

        print(sql)

        return
    except SystemExit:
        raise # let argparse print error(s)
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        exit(1)


if __name__ == "__main__":
    main()