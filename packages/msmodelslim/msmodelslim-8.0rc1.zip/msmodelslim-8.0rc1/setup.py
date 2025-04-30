# Copyright (c) 2024-2024 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from configparser import ConfigParser

from setuptools import setup, find_packages

config = ConfigParser()
config.read('./config/config.ini')

abs_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(abs_path, "requirements.txt")) as f:
    required = f.read().splitlines()


setup(
    name='msmodelslim',
    version='8.0.RC1',
    description='msModelSlim, MindStudio ModelSlim Tools',
    long_description_content_type='text/markdown',
    url='https://gitee.com/ascend/msit',
    packages=find_packages(exclude=['precision_tool', 'security', ]),
    package_data={
        '': [
            'LICENSE',
            'data.json',
            'README.md',
            '*.txt',
            '*.bat',
            '*.sh',
            '*.cpp',
            '*.h',
            '*.py',
            '*.so',
        ]
    },
    data_files=[('', ['requirements.txt'])],
    license='Apache-2.0',
    keywords='msmodelslim',
    python_requires='>=3.7',
    install_requires=required,

)
