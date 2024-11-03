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

import gzip
import io
import json
import requests


DEBIAN_URL = 'https://packages.debian.org/stable/allpackages?format=txt.gz'
def get_debian_packages(outdir):
    print('get_debian_packages')
    response = requests.get(DEBIAN_URL)

    if response.status_code == 200:
        # Decompress the gzipped content
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
            content = gz.read().decode('utf-8')
    else:
        raise Exception(f"Invalid reponse code: {response.status_code}")

    line_count = 0
    packages = {}
    for line in content.split('\n'):
        line_count += 1
        left_paren = line.find('(')
        right_paren = line.find(')')
        if left_paren < 0 or right_paren < 0:
            continue
        package_name = line[:left_paren - 1]
        package_desc = line[right_paren + 2:]
        packages[package_name] = package_desc
    with open(outdir / 'debian_packages.json', 'w', encoding='utf-8') as json_file:
        json.dump(packages, json_file, ensure_ascii=True, indent=2)
    print(f'found {len(packages)} debian packages')

    return packages
