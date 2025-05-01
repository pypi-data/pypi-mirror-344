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
import urllib.parse
from abc import abstractmethod

from yarl import URL

from .. import helpers
from ..models import BaseSample
from ..ioplugin import IOPlugin


class StructuredDirectory(IOPlugin):
    """
    The Structured plugin is created to handle ``strucdir:///`` type or URLs.

    The URL scheme is rather simple: ``strucdir:///path/to/project`` and 
    resembles the FileSystem scheme:
    (see `wikipedia <http://en.wikipedia.org/wiki/File_URI_scheme>`_ for details)

    We do not make use of the ``host`` part and at the moment only support
    localhost (just leave the host empty) leading to ``strucdir:///`` URLs.

    .. warning:: This plugin ignores the hostname in the URL and does only
                 accept driver letters on Windows in the form ``c:/``
    """
    scheme = 'strucdir'

    def __init__(self):
        # initialize the instance and register the scheme
        super(StructuredDirectory, self).__init__()

    @abstractmethod
    def _sample_to_outpath(self, url, sample):
        raise NotImplementedError('{} is not for working with urls'.format(self.scheme))

    def url_to_path(self, url):
        """ Get the path to a file from a url.
        Currently supports the file:// scheme

        Examples:

        .. code-block:: python

          >>> 'file:///d:/data/project/file.ext'
          'd:\\data\\project\\file.ext'

        .. warning::

          file:// will not function cross platform and is mainly for testing

        """
        parsed_url = urllib.parse.urlparse(str(url))

        # Translate properly depending on the scheme being used
        if parsed_url.scheme == self.scheme:
            if os.name == 'nt':
                path = parsed_url.path.lstrip('/')
            else:
                path = parsed_url.path

            return path.replace('/', os.path.sep)
        else:
            raise ValueError('This parses the {} scheme and not the {} scheme!'.format(self.scheme, parsed_url.scheme))

    def path_to_url(self, path, mountpoint=None):
        """ Construct an url from a given mount point and a relative path to the mount point. """
        path = os.path.abspath(os.path.expanduser(path))
        return "{scheme}://{path}".format(scheme=self.scheme, path=path)

    def put_url(self, sample, outurl):
        """
        Put the files to the external data store.

        :param inpath: path of the local data
        :param outurl: url to where to store the data, starts with ``file://``
        """
        outpath = self._sample_to_outpath(outurl, sample)
        print(f'Copy {sample.data_path} to {outpath}')
        helpers.copy_file_dir(sample.data_path, outpath)
        return os.path.exists(outpath)

    def pull_source_data(self, sample: BaseSample, outurl: URL, **kwargs):
        raise NotImplementedError("Not implemented for StructuredDirectory plugin")
