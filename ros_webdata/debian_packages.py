import requests
import sys
import os


DEBIAN_URL = 'https://packages.debian.org/stable/allpackages?format=txt.gz'
def get_debian_packages():
    print('get_debian_packages')
    response = requests.get(DEBIAN_URL)
    print(f'response encoding is {response.encoding}')
    content = response.content.decode('utf-8')
    print(f'content:\n{len(content)}')
    line_count = 0
    packages = {}
    for line in content.split('\n'):
        if line_count> 20:
            break
        left_paren = line.find('(')
        right_paren = line.find(')')
        if left_paren < 0 or right_paren < 0:
            continue
        line_count += 1
        package_name = line[:left_paren - 1]
        package_desc = line[right_paren + 2:]
        s4pane = '4pane'
        print(f'{package_name}: {package_desc}')
        print(':'.join(hex(ord(x))[2:] for x in package_name))
        print(':'.join(hex(ord(x))[2:] for x in s4pane))
        print(s4pane)
        print(f'{s4pane}')
        print('4pane')
        # packages[package_name] = package_desc
        # For some reason, this prints as gibberish in github actions
        # print(f'{package_name} : {package_desc}')
    return packages
