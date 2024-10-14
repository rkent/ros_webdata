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

import json
import requests
import yaml


ROS_PYTHON_DEPS_URL = 'https://github.com/ros/rosdistro/raw/refs/heads/master/rosdep/python.yaml'
def get_pip_names(outdir):
    print('get_pip_names')
    pip_package_names = {}
    response = requests.get(ROS_PYTHON_DEPS_URL , allow_redirects=True)
    content = response.content.decode("utf-8")
    rosdeps = yaml.safe_load(content)
    for key in rosdeps:
        found_it = False
        for distro in ['ubuntu', 'debian', 'fedora']:
            if distro not in rosdeps[key]:
                continue
            if type(rosdeps[key][distro]) is dict:
                if 'pip' in rosdeps[key][distro]:
                    if type(rosdeps[key][distro]['pip']) is list:
                        pip_package_names[key] = rosdeps[key][distro]['pip'][0]
                        found_it = True
                        break
                    if 'packages' in rosdeps[key][distro]['pip']:
                        pip_package_names[key] = rosdeps[key][distro]['pip']['packages'][0]
                        found_it = True
                        break
        if found_it:
            print(f'{key}: {pip_package_names[key]}')

    with open(outdir / 'pip_package_names.json', 'w', encoding ='utf8') as json_file:
        json.dump(pip_package_names, json_file, ensure_ascii=True, indent=1)

    print(f'found {len(pip_package_names)} pip package names')
    return pip_package_names

PYPI_API_URL = 'https://pypi.python.org/pypi/{package_name}/json'
def get_pip_descriptions(outdir, pip_package_names):
    print('get_pip_descriptions')
    pip_descriptions = {}
    for key, value in pip_package_names.items():
        url = PYPI_API_URL.format(package_name=value)
        response = requests.get(url , allow_redirects=True)
        result = response.json()
        summary = result['info'].get('summary') if 'info' in result else None
        if summary:
            pip_descriptions[key] = summary
            print(key, pip_descriptions[key])
        else:
            print(f'No pip summary found for {key}: {value}')

    with open(outdir / 'pip_packages.json', 'w', encoding ='utf8') as json_file:
        json.dump(pip_descriptions, json_file, ensure_ascii=True, indent=1)
