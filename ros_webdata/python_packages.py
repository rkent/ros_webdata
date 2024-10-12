import requests
import yaml

ROSDEPS_PYTHON_URL='https://github.com/ros/rosdistro/raw/refs/heads/master/rosdep/python.yaml'

def get_python_packages():
    response = requests.get(ROSDEPS_PYTHON_URL)
    content = response.content.decode('utf-8')
    with open('config.yml', 'r') as file:
        prime_service = yaml.safe_load(file)
