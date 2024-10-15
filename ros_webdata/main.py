# Copyright 2024 R. Kent James <kent@caspia.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
from pathlib import Path
import sys

from .debian_packages import get_debian_packages
from.package_downloads import get_package_downloads
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
    parser.add_argument('-t', '--types', default='debian,pip,downloads', help='Types to run, default is debian,pip,downloads')
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
    if 'downloads' in args.types:
        get_package_downloads(outdir)

if __name__ == '__main__':
    main()
