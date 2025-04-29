import argparse
import logging

from dar_utilities.curator import _configure_creator_subparser

def _prepare_parser():
    arg_parser = argparse.ArgumentParser(prog="dar_utilities", description="eLTER Data Archive and Repository (DAR) Utilities")
    subparsers = arg_parser.add_subparsers(required=True)

    creator_parser = subparsers.add_parser(
        "curator",
        help="Utilities for dataset curators",
    )

    _configure_creator_subparser(creator_parser)

    return arg_parser


if __name__ == "__main__":
    parser = _prepare_parser()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as e:
        exit(1)




