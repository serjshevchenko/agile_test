import os
import typing as t

import yaml
import argparse


def get_config() -> t.Dict[str, t.Any]:
    config_filename = os.environ.get('APP_CONFIG')
    if not config_filename:
        args = args_parse()
        config_filename = args.config

    return read_config(filename=config_filename)


def read_config(*, filename: t.Optional[str]) -> t.Dict[str, t.Any]:
    if not filename:
        return {}
    with open(filename) as f:
        config = yaml.load(f)
    return config


def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='configuration .yml file')
    return parser.parse_args()
