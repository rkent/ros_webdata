## Copyright 2024 R. Kent James <kent@caspia.com>
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


from bs4 import BeautifulSoup
from datetime import date, timedelta
import requests

PACKAGE_AWS_URL = 'https://awstats.osuosl.org/reports/packages.ros.org/{year}/{month:02d}/awstats.packages.ros.org.downloads.html'

def get_download_files(output_dir, month, year):
    url = PACKAGE_AWS_URL.format(month=month, year=year)
    print(url)
    get_package_downloads(url)


"""

A typical table row we need to parse looks like this (with some example rows):

<table class="aws_data" border="1" cellpadding="2" cellspacing="0" width="100%">
    <tbody>
        <tr bgcolor="#ECECEC">
            <th colspan="2">Downloads</th>
            <th bgcolor="#66DDEE" width="80">Hits</th>
            <th bgcolor="#66DDEE" width="80">206 Hits</th>
            <th bgcolor="#2EA495" width="80">Bandwidth</th>
            <th bgcolor="#2EA495" width="80">Average size</th>
        </tr>
        <tr>
            <td width="32"><img src="/icon/mime/archive.png" alt="" title=""></td>
            <td class="aws"><a href="http://packages.ros.org/ros2/ubuntu/dists/jammy/main/binary-amd64/Packages.gz"
                    target="url" rel="nofollow">/ros2/ubuntu/dists/jammy/main/binary-amd64/Packages.gz</a></td>
            <td>387,830</td>
            <td>12,258</td>
            <td>583.33 GB</td>
            <td>1.49 MB</td>
        </tr>
        <tr>
            <td><img src="/icon/mime/package.png" alt="" title=""></td>
            <td class="aws"><a
                    href="http://packages.ros.org/ros2/ubuntu/pool/main/r/ros-humble-rosidl-default-runtime/ros-humble-rosidl-default-runtime_1.2.0-2jammy.20240728.210843_amd64.deb"
                    target="url" rel="nofollow">/ros2/ubuntu/pool/main/r/ros-humble-rosidl-default-runtime/ros-h...</a>
            </td>
            <td>49,802</td>
            <td>5</td>
            <td>308.41 MB</td>
            <td>6.34 KB</td>
        </tr>
        <tr>
            <td><img src="/icon/mime/package.png" alt="" title=""></td>
            <td class="aws"><a
                    href="http://packages.ros.org/ros2/ubuntu/pool/main/r/ros-humble-rosidl-parser/ros-humble-rosidl-parser_3.1.5-2jammy.20240728.202913_amd64.deb"
                    target="url" rel="nofollow">/ros2/ubuntu/pool/main/r/ros-humble-rosidl-parser/ros-humble-ros...</a>
            </td>
            <td>49,754</td>
            <td>5</td>
            <td>920.63 MB</td>
            <td>18.95 KB</td>
        </tr>

So for the above row, we need to get the ros type (ros2), distro (humble), name (rosidl-parser), downloads(49,754).
We are not interested in some rows (href="http://packages.ros.org/ros2/ubuntu/dists/jammy/main/binary-amd64/Packages.gz")
"""

def get_package_downloads(url):
    response = requests.get(url)

    print(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('table', class_='aws_data')

    count = 0
    package_rows = data[1].find_all('td', class_='aws')
    distro_package_counts = {}
    version_list = {}
    packages_counts = {}
    print(f'possible package rows found: {len(package_rows)}')
    row_count = 0
    for row in package_rows:
        details = row.a['href'].split('/')
        if len(details) < 8:
            continue
        if details[3] not in ['ros', 'ros2']:
            continue
        if not details[8].startswith('ros'):
            continue
        full_name_details= details[8].split('-')
        if len(full_name_details) <= 2:
            continue
        if full_name_details[1] in ['dev', 'build']:
            continue

        # row_count += 1
        # if row_count > 100:
        #    break
        # get existing package, or create a new
        name = '-'.join(full_name_details[2:])
        distro = full_name_details[1]
        count = int(row.next_sibling.get_text().replace(',', ''))

        # Accumulate counts for different releases of the package
        if not distro in packages_counts:
            packages_counts[distro] = {distro: {}}
        if not name in packages_counts[distro]:
            packages_counts[distro][name] = count
        else:
            packages_counts[distro][name] += count

        # print(f'{name=}, {distro=}, {count=}')
    return packages_counts


def get_averaged_downloads(output_dir='./outdir'):
    """Get average package downloads, averaged over three months."""
    print('get_average_downloads')
    three_days_ago = date.today() - timedelta(days=3)
    print(three_days_ago)
    base_date = three_days_ago
    last_month = three_days_ago.month - 1
    year = three_days_ago.year

    # construct month, date for the previous three months
    old_month = three_days_ago.month
    old_year = three_days_ago.year
    old_months = [(old_month, old_year)]
    for months_back in range(1, 4):
        old_month = three_days_ago.month - months_back
        old_year = three_days_ago.year
        if old_month < 1:
            old_month += 12
            old_year -= 1
        old_months.append((old_month, old_year))
    print(old_months)
    
    for months_back in range(1, 2):
        get_download_files(output_dir, *old_months[months_back])



if __name__ == "__main__":
    month = 9
    year = 2024
    url = PACKAGE_AWS_URL.format(month=month, year=year)
    packages_counts = get_package_downloads(url)
    for distro, packages in packages_counts.items():
        print(f'{distro=}')
