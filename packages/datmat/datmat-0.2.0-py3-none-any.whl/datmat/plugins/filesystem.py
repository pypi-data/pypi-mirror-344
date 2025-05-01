# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
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

"""
This module contains the FileSystem plugin for fastr
"""

import os
import shutil
from pathlib import Path

from yarl import URL

from datmat import helpers
from datmat.ioplugin import IOPlugin
from datmat.models import URLSample, PathSample


class FileSystem(IOPlugin):
    """
    The FileSystem plugin is create to handle ``file://`` type or URLs. This is
    generally not a good practice, as this is not portable over between
    machines. However, for test purposes it might be useful.

    The URL scheme is rather simple: ``file://host/path``
    (see `wikipedia <http://en.wikipedia.org/wiki/File_URI_scheme>`_ for details)

    We do not make use of the ``host`` part and at the moment only support
    localhost (just leave the host empty) leading to ``file:///`` URLs.

    .. warning:: This plugin ignores the hostname in the URL and does only
                 accept driver letters on Windows in the form ``c:/``
    """
    scheme = 'file'

    def __init__(self):
        # initialize the instance and register the scheme
        super(FileSystem, self).__init__()

    def url_to_path(self, url: URL):
        """ Get the path to a file from a url.
        Currently supports the file:// scheme

        Examples:

        .. code-block:: python

          >>> 'file:///d:/data/project/file.ext'
          'd:\\data\\project\\file.ext'

        .. warning::

          file:// will not function cross platform and is mainly for testing

        """

        # Translate properly depending on the scheme being used
        if not url.scheme == self.scheme:
            raise ValueError('This parses the {} scheme and not the {} scheme!'.format(self.scheme, parsed_url.scheme))

        if os.name == 'nt':
            path = url.path.lstrip('/')
        else:
            path = url.path

        return path.replace('/', os.path.sep)

    def path_to_url(self, path, mountpoint=None):
        """ Construct an url from a given mount point and a relative path to the mount point. """
        path = Path(path).expanduser()
        return path.as_uri()

    def fetch_url(self, inurlsample: URLSample, outpath):
        """
        Fetch the files from the file.

        :param inurlsample: Sample that contains the data url to the item in the data store, starts with ``file://``
        :param outpath: path where to store the fetch data locally
        """
        inpath = self.url_to_path(inurlsample.data_url)

        # Clear away present data
        if os.path.exists(outpath):
            self.log.info('Removing currently exists data at {}'.format(outpath))
            if os.path.islink(outpath):
                os.remove(outpath)
            elif os.path.isdir(outpath):
                shutil.rmtree(outpath)
            else:
                os.remove(outpath)

        try:
            os.symlink(inpath, outpath)
            self.log.debug('Symlink successful')
        except OSError:
            self.log.debug('Cannot symlink, fallback to copy')
            if os.path.isdir(inpath):
                shutil.copytree(inpath, outpath)
            else:
                shutil.copy2(inpath, outpath)

        outpath_sample = PathSample(
            data_path=outpath
        )

        return outpath_sample

    def fetch_value(self, inurlsample: URLSample):
        """
        Fetch a value from an external file file.

        :param inurlsample: url of the value to read
        :return: the fetched value
        """
        path = self.url_to_path(inurlsample.data_url)
        with open(path, 'r') as file_handle:
            data = file_handle.read()

        return data

    def put_url(self, inpath, outurl):
        """
        Put the files to the external data store.

        :param inpath: path of the local data
        :param outurl: url to where to store the data, starts with ``file://``
        """
        outpath = self.url_to_path(outurl)
        helpers.copy_file_dir(inpath.data_path, outpath)
        return os.path.exists(outpath)

    def put_value(self, value, outurl):
        """
        Put the value in the external data store.

        :param value: value to store
        :param outurl: url to where to store the data, starts with ``file://``
        """
        outpath = self.url_to_path(outurl)

        with open(outpath, 'w') as file_handle:
            file_handle.write(str(value))

        return os.path.exists(outpath)
