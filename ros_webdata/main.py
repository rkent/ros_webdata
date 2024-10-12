import argparse
import json
from pathlib import Path
import sys

from .debian_packages import get_debian_packages
from .pip_packages import get_pip_names, get_pip_descriptions

COMMAND_NAME = 'rosdeps_descriptions'


def main(sysargs=None):
    # Assign sysargs if not set
    sysargs = sys.argv[1:] if sysargs is None else sysargs

    # Create a top level parser
    parser = argparse.ArgumentParser(
        prog='rosdeps_descriptions',
        description='Generate description summaries for ros dependencies using upstream sources'
    )

    parser.add_argument('-o', '--output_dir', default='./outdir', help='Directory containing output files')
    parser.add_argument('-t', '--types', default='debian,pip', help='Types to run, default is debian,pip')
    # parser.add_argument('-h', '--help', action='store_true')

    args = parser.parse_args()
    print(f'args: {args}')

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    if 'debian' in args.types:
        get_debian_packages(outdir)
    if 'pip' in args.types:
        pip_package_names = get_pip_names(outdir)
        get_pip_descriptions(outdir, pip_package_names)

if __name__ == '__main__':
    main()
