import argparse
import json
from pathlib import Path
import sys

from .debian_packages import get_debian_packages

COMMAND_NAME = 'rosdeps_descriptions'


def main(sysargs=None):
    # Assign sysargs if not set
    sysargs = sys.argv[1:] if sysargs is None else sysargs

    print(" can you handle unicode? Å")
    # Create a top level parser
    parser = argparse.ArgumentParser(
        prog='rosdeps_descriptions',
        description='Generate description summaries for ros dependencies using upstream sources'
    )

    parser.add_argument('-o', '--output_dir', default='./outdir', help='Directory containing output files')
    # parser.add_argument('-h', '--help', action='store_true')

    args = parser.parse_args()
    print(f'args: {args}')

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    debian_packages = get_debian_packages()
    with open(outdir / 'debian_packages.json', 'w', encoding ='utf8') as json_file:
        json.dump(debian_packages, json_file, ensure_ascii=True, indent=1)

    print(f'found {len(debian_packages)} debian packages')

if __name__ == '__main__':
    main()
