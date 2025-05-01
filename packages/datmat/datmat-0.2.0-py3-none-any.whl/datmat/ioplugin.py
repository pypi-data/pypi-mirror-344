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
This module contains the manager class for IOPlugins and the
base class for all IOPlugins
"""
from __future__ import annotations

import json
import os
import urllib.parse as up
from abc import abstractmethod, ABCMeta
from pathlib import Path

from yarl import URL

from .helpers import create_logger
from .models import URLSample, BaseSample
from .typehints import pathlike


class IOPlugin(metaclass=ABCMeta):
    """
    :py:class:`IOPlugins <fastr.core.ioplugin.IOPlugin>` are used for data import
    and export for the sources and sinks.

    The use of is mainly via the URL scheme used to specify input and output
    """
    _instantiate = True

    # Mapping that maps all url scheme to plugins
    PLUGIN_MAP = {}

    def __init__(self):
        """
        Initialization for the IOPlugin

        :return: newly created IOPlugin
        """
        super(IOPlugin, self).__init__()
        self._results = {}
        self.log = create_logger()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        scheme = cls.scheme

        if isinstance(scheme, str):
            scheme = [scheme]

        for scheme_entry in scheme:
            cls.PLUGIN_MAP[scheme_entry] = cls

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    @property
    @abstractmethod
    def scheme(self):
        """
        ``(abstract)`` This abstract property is to be overwritten by a subclass to indicate
        the url scheme associated with the IOPlugin.
        """
        raise NotImplementedError("IOPlugin scheme is not set")

    def url_to_path(self, url):
        """
        ``(abstract)`` Get the path to a file from a url.

        :param str url: the url to retrieve the path for
        :return: the corresponding path
        :rtype: str
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument
        raise NotImplementedError('{} is not for working with urls'.format(self.scheme))

    def fetch_url(self,
                  inurlsample: URLSample,
                  outpath: pathlike):
        """
        ``(abstract)``  Fetch a file from an external data source.

        :param inurlsample: url to the item in the data store
        :param outpath: path where to store the fetch data locally
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument
        raise NotImplementedError('{} is not for direct url data retrieval'.format(self.scheme))

    def fetch_value(self,
                    inurl: URL):
        """
        ``(abstract)``  Fetch a value from an external data source.

        :param inurl: the url of the value to retrieve
        :return: the fetched value
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument
        raise NotImplementedError('{} is not for direct value data retrieval'.format(self.scheme))

    def put_url(self,
                inpath: pathlike,
                outurl: URL):
        """
        ``(abstract)`` Put the files to the external data store.

        :param inpath: path to the local data
        :param outurl: url to where to store the data in the external data store.
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument
        raise NotImplementedError('{} is not for direct url data storage'.format(self.scheme))

    def put_value(self, value, outurl):
        """
        ``(abstract)`` Put the files to the external data store.

        :param value: the value to store
        :param outurl: url to where to store the data in the external data store.
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument
        raise NotImplementedError('{} is not for direct value data storage'.format(self.scheme))

    def path_to_url(self, path, mountpoint=None):
        """
        ``(abstract)`` Construct an url from a given mount point and a relative
        path to the mount point.

        :param str path: the path to determine the url for
        :param mountpoint: the mount point to use, will be automatically
                           detected if None is given
        :type mountpoint: str or None
        :return: url matching the path
        :rtype: str
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument
        raise NotImplementedError('{} is not for working with urls'.format(self.scheme))

    def setup(self, *args, **kwargs):
        """
        ``(abstract)`` Setup before data transfer. This can be any function
        that needs to be used to prepare the plugin for data transfer.
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument,no-self-use
        pass

    def cleanup(self):
        """
        ``(abstract)`` Clean up the IOPlugin. This is to do things like
        closing files or connections. Will be called when the plugin is no
        longer required.
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument,no-self-use
        pass

    def expand_url(self, urlsample: URLSample):
        """
        ``(abstract)`` Expand an URL. This allows a source to collect multiple
        samples from a single url. The URL will have a wildcard or point to
        something with info and multiple urls will be returned.

        :param URLSample urlsample: url to expand
        :return: the resulting url(s), a tuple if multiple, otherwise a str
        :rtype: str or tuple of str
        """
        # This is a placeholder function, so we do no use our arguments
        # pylint: disable=unused-argument,no-self-use
        return urlsample

    @staticmethod
    def isurl(string):
        """
        Test if given string is an url.

        :param str string: string to test
        :return: ``True`` if the string is an url, ``False`` otherwise
        :rtype: bool
        """
        parsed_url = up.urlparse(str(string))
        return parsed_url.scheme != ''

    @staticmethod
    def print_result(result):
        """
        Print the result of the IOPlugin to stdout to be picked up by the tool

        :param result: value to print as a result
        :return: None
        """
        print('__IOPLUGIN_OUT__={}'.format(json.dumps(result)))

    def pull_source_data(self,
                         inurl: URL,
                         outdir: Path,
                         sample_id,
                         datatype=None):
        """
        Transfer the source data from inurl to be available in outdir.

        :param str inurl: the input url to fetch data from
        :param str outdir: the directory to write the data to
        :param DataType datatype: the datatype of the data, used for determining
                                  the total contents of the transfer
        :return: None
        """
        results = {}
        self.setup()

        # Convert inurl to a URLSample to unify the code
        inurlsample = URLSample(data_url=inurl)

        # First expand the URL
        valuelist = self.expand_url(inurlsample)

        self.log.debug('[{}] pulling sample {} with value {} and datatype {}'.format(
            self.scheme, sample_id, inurlsample.data_url, datatype)
        )

        if isinstance(valuelist, tuple):
            # We expanded the URL, so now process each new value/URL seperately
            if len(valuelist) == 0:
                raise ValueError(('No data found when expanding'
                                  ' URL {}, this probably means '
                                  'the URL is not correct.').format(inurlsample.data_url))
            for cardinality_nr, (sub_sample_id, value) in enumerate(valuelist):
                if sub_sample_id is None:
                    self.log.debug('Changing sub sample id from None to {}'.format(sub_sample_id))
                    sub_sample_id = '{}_{}'.format(sample_id, cardinality_nr)
                self.log.debug('Found expanded item {}: {}'.format(sub_sample_id, value))
                if isinstance(value, URLSample):
                    # Expanded value is an URLSample, so it need to be processed
                    outsubdir = outdir / str(sub_sample_id)
                    if not os.path.isdir(outsubdir):
                        os.mkdir(outsubdir)
                    result = self.pull_source_data(value.data_url, outsubdir, sub_sample_id)
                    results.update(result)
                else:
                    # Expanded value is a value, so we assume this is the value to be used
                    results[sub_sample_id] = (value,)
        elif isinstance(valuelist, URLSample):
            # The expand did not change the URL
            if valuelist.data_url != inurl:
                raise ValueError('If valuelist is a URLSample, it should represent the original inurl!')

            outfile = outdir / valuelist.data_url.name
            result = self.fetch_url(valuelist, outfile)

            if not result:
                raise IOError('Could not retrieve data from {}'.format(valuelist.data_url))

            results[sample_id] = (result,)

        else:
            self.log.error('Expand of {} returned an invalid type! ({} after expansion)'.format(inurl, valuelist))

        return results

    def push_sink_data(self,
                       sample: BaseSample,
                       outurl: URL):
        """
        Write out the sink data from the inpath to the outurl.

        :param str inpath: the path of the data to be pushed
        :param str outurl: the url to write the data to
        :return: None
        """
        self.log.info('Push sink called with: {}, {}'.format(sample, outurl))
        result = self.put_url(sample, outurl)
        outpath = self.url_to_path(outurl)

        return result, outpath
