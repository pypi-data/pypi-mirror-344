#!/usr/bin/env python3

import argparse
import logging
import os
import shlex
import shutil
import sys
from pathlib import Path

from . import conf

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default='')
    parser.add_argument('-r', '--remove', action='store_true')
    parser.add_argument('-p', '--private', action='store_true')
    parser.add_argument('-o', '--overlay', action='store_true')
    parser.add_argument('-c', '--current-dir', action='store_true')
    parser.add_argument('--storage', type=Path, default='~/.local/state/wraplify')
    parser.add_argument('--config', type=Path, default='~/.config/wraplify')
    parser.add_argument('--net', action='store_true')
    parser.add_argument('--bwrap', type=str)
    parser.add_argument('--clean-envs', action='store_true')
    parser.add_argument('--clean-all', action='store_true')
    parser.add_argument('inner', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    if not args.inner:
        args.inner = ['bash']
    if args.name == '':
        args.name = Path(args.inner[0]).name
    args.config = args.config.expanduser()
    args.storage = args.storage.expanduser()
    args.path = args.storage / args.name
    return args


def rm_recursive(path: Path):
    if path.exists():
        if input(f"Remove directory '{path}'? [y/N] ").lower() == 'y':
            os.system(f'chmod -R 777 {path}')  # ._.
            shutil.rmtree(path)


def check_bwrap():
    if not shutil.which('bwrap'):
        print('Bubblewrap is required but not installed', file=sys.stderr)
        exit(1)


def main():
    check_bwrap()

    args = parse_args()

    if args.clean_all:
        rm_recursive(args.config)
        rm_recursive(args.storage)
        exit(0)

    if args.clean_envs:
        rm_recursive(args.storage)
        exit(0)

    if args.remove:
        rm_recursive(args.path)
        exit(0)

    if not args.path.exists():
        args.path.mkdir(parents=True)

    flags = [
        '--unshare-user',
        '--unshare-ipc',
        '--unshare-pid',
        '--unshare-net',
        '--unshare-uts',
        '--die-with-parent',
    ]

    # fmt:off
    special_dirs = [
        '--ro-bind', '/', '/',
        '--proc', '/proc',
        '--dev', '/dev',
    ]
    # fmt:on

    if args.net:
        flags.append('--share-net')

    home_dirs = []
    if args.private:
        home_dirs.extend(['--tmpfs', os.environ['HOME']])
    elif args.overlay:
        upper_path = args.path / 'upper'
        upper_path.mkdir(exist_ok=True)
        work_path = args.path / 'work'
        work_path.mkdir(exist_ok=True)
        home_dirs.extend(
            [
                '--overlay-src',
                os.environ['HOME'],
                '--overlay',
                upper_path.as_posix(),
                work_path.as_posix(),
                os.environ['HOME'],
            ]
        )
    else:
        home_path = args.path / 'home'
        home_path.mkdir(exist_ok=True)
        home_dirs.extend(['--bind', home_path.as_posix(), os.environ['HOME']])

    other_dirs = []
    if args.current_dir:
        home_dirs.extend(['--bind', os.getcwd(), os.getcwd()])

    run_dirs = ['--tmpfs', '/run']
    if 'XDG_RUNTIME_DIR' in os.environ:
        xdg_runtime_dir = os.environ['XDG_RUNTIME_DIR']
        run_dirs.extend(['--dir', xdg_runtime_dir])

    include_paths = []
    for path in conf.load_config(args.config, args.name):
        include_paths.extend(['--bind', path.as_posix(), path.as_posix()])

    passthrough_args = []
    if args.bwrap is not None:
        passthrough_args.extend(shlex.split(args.bwrap))

    bwrap_args = [
        'bwrap',
        *flags,
        *special_dirs,
        *home_dirs,
        *run_dirs,
        *other_dirs,
        *include_paths,
        *passthrough_args,
        *args.inner,
    ]

    logging.info(' '.join(bwrap_args))
    os.execvp(bwrap_args[0], bwrap_args)


if __name__ == '__main__':
    main()
