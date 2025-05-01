# Copyright 2017-2020 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
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

import os
from setuptools import setup

# Parse requirements file
with open('requirements.txt', 'r') as fh:
    _requires = fh.read().splitlines()
    
with open('test_requirements.txt', 'r') as fh:
    _tests_require = fh.read().splitlines()

entry_points = {
    "console_scripts": [
        "datmat = datmat.cli:cli",
    ],
}

VERSION = "0.2.0"
# When building something else than a release (tag) append the job id to the version.
if os.environ.get('CI_COMMIT_TAG'):
    pass
elif os.environ.get('CI_JOB_ID'):
    VERSION += f".{os.environ['CI_JOB_ID']}"

setup(
    name='datmat',
    version=VERSION,
    author='H.C. Achterberg, M. Koek, A. Versteeg, M. Birhanu, A.G.J. Harms, I. Bocharov',
    author_email='h.achterberg@erasmusmc.nl, m.koek@erasmusmc.nl, a.versteeg@erasmusmc.nl, m.birhanu@erasmusmc.nl',
    packages=[
        'datmat',
        'datmat.cli',
        'datmat.plugins'
    ],
    include_package_data=True,
    url='https://gitlab.com/radiology/infrastructure/data-materialisation',
    license='Apache 2.0',
    description='Datmat is a tool for data materalisation; it gets your data where it is, to where you need it to be.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Logging',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://datmat.readthedocs.io',
        'Issues': 'https://gitlab.com/radiology/infrastructure/data-materialisation/-/issues',
        'Download': 'https://gitlab.com/radiology/infrastructure/data-materialisation/-/archive/master/data-materialisation-master.zip',
        "CI/CD": 'https://gitlab.com/radiology/infrastructure/data-materialisation/-/pipelines',
    },
    install_requires=_requires,
    entry_points=entry_points,
    tests_require=_tests_require
)
