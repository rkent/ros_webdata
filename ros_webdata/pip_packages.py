import json
import requests
import yaml


ROS_PYTHON_DEPS_URL = 'https://github.com/ros/rosdistro/raw/refs/heads/master/rosdep/python.yaml'
def get_python_deps(outdir):
    print('get_python_deps')
    distro_packages = {}
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
                        distro_packages[key] = rosdeps[key][distro]['pip'][0]
                        found_it = True
                        break
                    if 'packages' in rosdeps[key][distro]['pip']:
                        distro_packages[key] = rosdeps[key][distro]['pip']['packages'][0]
                        found_it = True
                        break
        if found_it:
            print(f'{key}: {distro_packages[key]}')

    with open(outdir / 'pip_package_names.json', 'w', encoding ='utf8') as json_file:
        json.dump(distro_packages, json_file, ensure_ascii=True, indent=1)

    print(f'found {len(distro_packages)} pip package names')
