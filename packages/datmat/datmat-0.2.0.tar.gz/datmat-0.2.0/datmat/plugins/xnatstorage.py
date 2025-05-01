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
This module contains the XNATStorage plugin for fastr
"""

import fnmatch
import netrc
import os
import re
import tempfile
import time
import urllib.parse
from collections import OrderedDict
from html import unescape
from pathlib import Path

from yarl import URL

import requests
import xnat
import xnat.exceptions
from requests.exceptions import RequestException

from ..ioplugin import IOPlugin
from ..typehints import pathlike
from ..models import PathSample, URLSample, BaseSample


class XNATStorage(IOPlugin):
    """
    .. warning::

        As this IOPlugin is under development, it has not been thoroughly
        tested.

    The XNATStorage plugin is an IOPlugin that can download data from and
    upload data to an XNAT server. It uses its own ``xnat://`` URL scheme.
    This is a scheme specific for this plugin and though it looks somewhat
    like the XNAT rest interface, a different type or URL.

    Data resources can be access directly by a data url::

        xnat://xnat.example.com/data/archive/projects/sandbox/subjects/subject001/experiments/experiment001/scans/T1/resources/DICOM
        xnat://xnat.example.com/data/archive/projects/sandbox/subjects/subject001/experiments/*_BRAIN/scans/T1/resources/DICOM

    In the second URL you can see a wildcard being used. This is possible at
    long as it resolves to exactly one item.

    The ``id`` query element will change the field from the default experiment to
    subject and the ``label`` query element sets the use of the label as the
    fastr id (instead of the XNAT id) to ``True`` (the default is ``False``)

    To disable ``https`` transport and use ``http`` instead the query string
    can be modified to add ``insecure=true``. This will make the plugin send
    requests over ``http``::

        xnat://xnat.example.com/data/archive/projects/sandbox/subjects/subject001/experiments/*_BRAIN/scans/T1/resources/DICOM?insecure=true

    For sinks it is import to know where to save the data. Sometimes you want
    to save data in a new assessor/resource and it needs to be created. To
    allow the Fastr sink to create an object in XNAT, you have to supply the
    type as a query parameter::

        xnat://xnat.bmia.nl/data/archive/projects/sandbox/subjects/S01/experiments/_BRAIN/assessors/test_assessor/resources/IMAGE/files/image.nii.gz?resource_type=xnat:resourceCatalog&assessor_type=xnat:qcAssessmentData

    Valid options are: subject_type, experiment_type, assessor_type, scan_type,
    and resource_type.

    If you want to do a search where
    multiple resources are returned, it is possible to use a search url::

        xnat://xnat.example.com/search?projects=sandbox&subjects=subject[0-9][0-9][0-9]&experiments=*_BRAIN&scans=T1&resources=DICOM

    This will return all DICOMs for the T1 scans for experiments that end with _BRAIN that belong to a
    subjectXXX where XXX is a 3 digit number. By default the ID for the samples
    will be the experiment XNAT ID (e.g. XNAT_E00123). The wildcards that can
    be the used are the same UNIX shell-style wildcards as provided by the
    module :py:mod:`fnmatch`.

    It is possible to change the id to a different fields id or label. Valid
    fields are project, subject, experiment, scan, and resource::

        xnat://xnat.example.com/search?projects=sandbox&subjects=subject[0-9][0-9][0-9]&experiments=*_BRAIN&scans=T1&resources=DICOM&id=subject&label=true

    The following variables can be set in the search query:

    ============= ============== =============================================================================================
    variable      default        usage
    ============= ============== =============================================================================================
    projects      ``*``          The project(s) to select, can contain wildcards (see :py:mod:`fnmatch`)
    subjects      ``*``          The subject(s) to select, can contain wildcards (see :py:mod:`fnmatch`)
    experiments   ``*``          The experiment(s) to select, can contain wildcards (see :py:mod:`fnmatch`)
    scans         ``*``          The scan(s) to select, can contain wildcards (see :py:mod:`fnmatch`)
    resources     ``*``          The resource(s) to select, can contain wildcards (see :py:mod:`fnmatch`)
    id            ``experiment`` What field to use a the id, can be: project, subject, experiment, scan, or resource
    label         ``false``      Indicate the XNAT label should be used as fastr id, options ``true`` or ``false``
    insecure      ``false``      Change the url scheme to be used to http instead of https
    verify        ``true``       (Dis)able the verification of SSL certificates
    regex         ``false``      Change search to use regex :py:func:`re.match` instead of fnmatch for matching
    overwrite     ``false``      Tell XNAT to overwrite existing files if a file with the name is already present
    ============= ============== =============================================================================================

    If you want to download an entire project, you can use an URL in the following format::

        xnat://xnat.example.com/projects/project_name

    This will by default download all the DICOM resources for all subjects, experiments, scans in the project. You can
    add query parameters just like in the search to control a filter for a subset (or different resource). In practice
    this works almost like a search with projects='project_name' and resources='DICOM'

    For storing credentials the ``.netrc`` file can be used. This is a common
    way to store credentials on UNIX systems. It is required that the file is
    only accessible by the owner only or a ``NetrcParseError`` will be raised.
    A netrc file is really easy to create, as its entries look like::

        machine xnat.example.com
                login username
                password secret123

    See the :py:mod:`netrc module <netrc>` or the
    `GNU inet utils website <http://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html#The-_002enetrc-file>`_
    for more information about the ``.netrc`` file.

    .. note::

        On windows the location of the netrc file is assumed to be
        ``os.path.expanduser('~/_netrc')``. The leading underscore is
        because windows does not like filename starting with a dot.

    .. note::

        For scan the label will be the scan type (this is initially
        the same as the series description, but can be updated manually
        or the XNAT scan type cleanup).

    .. warning::

        labels in XNAT are not guaranteed to be unique, so be careful
        when using them as the sample ID.

    This plugin is heavily leaning on `XNATpy <https://xnat.readthedocs.io>` for the heavy lifting.

    For background on XNAT, see the
    `XNAT API DIRECTORY <https://wiki.xnat.org/display/XNAT16/XNAT+REST+API+Directory>`_
    for the REST API of XNAT.
    """
    scheme = ('xnat+http', 'xnat+https')

    def __init__(self):
        # initialize the instance and register the scheme
        super().__init__()
        self._xnat = (None, None)

    def cleanup(self):
        if self.xnat is not None:
            self.log.info('Attempting to cleanly disconnecting XNAT.')
            self.xnat.disconnect()

    @property
    def server(self):
        return self._xnat[0]

    @property
    def xnat(self) -> xnat.session.BaseXNATSession:
        return self._xnat[1]

    def connect(self, server, path='', insecure=False, verify=True):
        if self.server != server:
            # Try to neatly clean previous connection
            if self.xnat is not None:
                self.xnat.disconnect()

            try:
                netrc_file = os.path.join('~', '_netrc' if os.name == 'nt' else '.netrc')
                netrc_file = os.path.expanduser(netrc_file)
                user, _, password = netrc.netrc(netrc_file).authenticators(server)
            except FileNotFoundError:
                self.log.warning("Could not find .netrc file! Assuming 'guest' login.")
                user = None
                password = None
            except TypeError:
                raise ValueError('Could not retrieve login info for "{}" from the .netrc file!'.format(server))

            # Create the URL for the XNAT connection
            schema = 'http' if insecure else 'https'
            session = xnat.connect(urllib.parse.urlunparse([schema, server, path, '', '', '']),
                                   user=user, password=password, debug=False, verify=verify)

            # Time-out a request when no bytes are received for 120 seconds
            session.request_timeout = 120

            self._xnat = (server, session)

    def expand_url(self, urlsample: URLSample):
        url = urlsample.data_url

        if url.path == '/search':
            return self._expand_search(urlsample)
        if re.match('.*/projects/[^/]+$', url.path):
            return self._expand_project(urlsample)
        else:
            url, path_prefix, insecure, verify, use_regex, query = self._parse_uri(urlsample.data_url)

            # Create a session for this retrieval
            self.connect(url.host, path=path_prefix, insecure=insecure, verify=verify)
            match = re.match(
                r'/data/archive/projects/(?P<project>[a-zA-Z0-9_\-]+)/subjects/(?P<subject>[a-zA-Z0-9_\-]+)/experiments/(?P<experiment>[a-zA-Z0-9_\-]+)/scans/(?P<scan>[a-zA-Z0-9_\-]+)/resources/(?P<resource>[a-zA-Z0-9_\-]+).*',
                url.path)
            project = self.xnat.projects[match.group('project')]
            subject = project.subjects[match.group('subject')]
            experiment = subject.experiments[match.group('experiment')]
            scan = experiment.scans[match.group('scan')]
            urlsample = URLSample(
                data_url=urlsample.data_url,
                project_name=unescape(project.name),
                subject_label=unescape(subject.label),
                experiment_label=unescape(experiment.label),
                experiment_date=experiment.date,
                scan_id=scan.id,
                scan_type=unescape(scan.type)
            )
            return urlsample

    def fetch_url(self, inurlsample: URLSample, outpath: pathlike):
        """
        Get the file(s) or values from XNAT.

        :param inurlsample: url to the item in the data store
        :param outpath: path where to store the fetch data locally
        """
        url, path_prefix, insecure, verify, use_regex, query = self._parse_uri(inurlsample.data_url)

        # Create a session for this retrieval
        self.connect(url.host, path=path_prefix, insecure=insecure, verify=verify)

        # Find the filepath within the resource
        location = self._path_to_dict(url.path)
        # self.log.warning(location)
        filepath = location.get('files', '')

        # Find the resource
        resource = self._locate_resource(inurlsample.data_url, use_regex=use_regex)

        # Download the Resource
        workdir = Path(outpath)
        if not workdir.is_dir():
            workdir = workdir.parent / workdir.name.replace('.', '_')
            workdir.mkdir(parents=True, exist_ok=True)

        # Create uniquer dir to download in
        workdir = tempfile.mkdtemp(prefix='datmat_xnat_{}_tmp'.format(resource.id), dir=workdir)
        workdir = Path(workdir)

        # Retry downloading in case of connection reset
        max_tries = tries = 3
        success = False
        while tries > 0 and not success:
            try:
                self.log.info('Download attempt {} of {}'.format(max_tries - tries + 1, max_tries))
                tries -= 1
                resource.download_dir(workdir, verbose=False)
                success = True
            except requests.exceptions.ChunkedEncodingError:
                if tries <= 0:
                    raise
                else:
                    # Sleep 10 seconds times the amount of tries
                    time.sleep((max_tries - tries) * 10)

        # Find the file in the proper path
        resource_label = resource.label.replace(' ', '_')
        if filepath == '':
            target = 'resources/{}/files'.format(resource_label)
        else:
            target = f'resources/{resource_label}/files/{filepath}'

        result = list(workdir.rglob(target))

        if len(result) != 1:
            message = f'Could not find {filepath} file in downloaded resource! Glob for result using "{target}" did not return a single item but {len(result)}'
            self.log.error(message)
            raise ValueError(message)
        else:
            self.log.info(f'Found downloaded data in {result[0]}')

        data_path = result[0]

        outpath_sample = PathSample(
            data_path=data_path,
            project_name=inurlsample.project_name,
            subject_label=inurlsample.subject_label,
            experiment_label=inurlsample.experiment_label,
            experiment_date=inurlsample.experiment_date,
            scan_id=inurlsample.scan_id,
            scan_type=inurlsample.scan_type,
            filename=str(Path(*Path(target).parts[1:]))  # Remove 'resources' from target
        )

        return outpath_sample

    def push_sink_data(self,
                       sample: BaseSample,
                       outurl: URL):
        raise NotImplementedError("Not implemented for XNATStorage plugin")

    def _path_to_dict(self, path):
        self.log.info('Converting {} to dict...'.format(path))
        if not path.startswith('/data/'):
            raise ValueError('Resources to be located should have a path starting with /data/ (found {})'.format(path))

        if path.startswith('/data/archive/'):
            path_prefix_parts = 2
        else:
            path_prefix_parts = 1

        # Break path apart
        parts = path.lstrip('/').split('/', 11 + path_prefix_parts)

        # Ignore first two parts and build a dict from /key/value/key/value pattern
        path_iterator = parts[path_prefix_parts:].__iter__()
        location = OrderedDict()
        for key, value in zip(path_iterator, path_iterator):
            if key == 'files':
                filepath = [value] + list(path_iterator)
                value = '/'.join(filepath)

            location[key] = value

        self.log.info('Found {}'.format(location))
        return location

    def _locate_resource(self, url, create=False, use_regex=False):
        resources = self._find_objects(url=url, create=create, use_regex=use_regex)

        if len(resources) == 0:
            raise ValueError('Could not find data object at {}'.format(url))
        elif len(resources) > 1:
            raise ValueError('Data item does not point to a unique resource! Matches found: {}'.format(
                [x.fulluri for x in resources]))

        resource = resources[0]

        # Make sure the return value is actually a resource
        resource_cls = self.xnat.XNAT_CLASS_LOOKUP['xnat:abstractResource']
        if not isinstance(resource, resource_cls):
            raise TypeError('The resource should be an instance of {}'.format(resource_cls))

        return resource

    def _parse_uri(self, url: URL):
        if url.scheme not in self.scheme:
            raise ValueError('URL scheme {} not of supported type {}!'.format(url.scheme,
                                                                              self.scheme))

        query = url.query

        path_prefix = url.path[:url.path.find('/data/')]

        # Strip the prefix of the url path
        url = url.with_path(url.path[len(path_prefix):])

        if not url.path.startswith('/data/archive/') and url.path.startswith('/data/'):
            self.log.info('Patching archive into url path starting with data')
            url = url.with_path(url.path[:6] + 'archive/' + url.path[6:])

        if not url.path.startswith('/data/archive'):
            raise ValueError('Can only fetch urls with the /data/archive path')

        if url.scheme == 'xnat+http':
            insecure = True
        elif url.scheme == 'xnat+https':
            insecure = False
        else:
            self.log.warning('Using old-style insecure lookup, please use a xnat+http://'
                             ' or xnat+https:// url scheme instead!')
            insecure = query.get('insecure', '0') in ['true', '1']

        verify = query.get('verify', '1') in ['true', '1']
        use_regex = query.get('regex', '0') in ['true', '1']

        return url, path_prefix, insecure, verify, use_regex, query

    def put_url(self, inpath, outurl):
        """
        Upload the files to the XNAT storage

        :param inpath: path to the local data
        :param outurl: url to where to store the data in the external data store.
        """
        # Create a session for this retrieval
        url, path_prefix, insecure, verify, use_regex, query = self._parse_uri(outurl)
        self.connect(url.netloc, path=path_prefix, insecure=insecure, verify=verify)

        # Determine the resource to upload to
        resource = self._locate_resource(outurl, create=True, use_regex=use_regex)

        # Determine the file within xnat
        parsed_url = urllib.parse.urlparse(outurl)
        location = self._path_to_dict(parsed_url.path)

        # Upload the file
        self.log.info('Uploading to: {}'.format(resource.fulluri))
        self.log.info('Uploading to path: {}'.format(location['files']))
        try:
            overwrite = urllib.parse.parse_qs(url.query).get('overwrite', ['0'])[0] in ['true', '1']
            self._upload(resource, inpath, location['files'], overwrite=overwrite)
            return True
        except xnat.exceptions.XNATUploadError as exception:
            self.log.error('Encountered error when uploading data: {}'.format(exception))
            return False

    def _upload(self, resource, in_path, location, retries=3, overwrite=False):
        # Initial upload
        success = False
        tries = retries
        file_size = os.path.getsize(in_path)

        # Open the file once for streaming uploades
        with open(in_path, 'rb') as in_file_handle:
            while not success and tries > 0:
                tries -= 1
                try:
                    in_file_handle.seek(0)
                    resource.upload(in_file_handle, location, overwrite=overwrite)
                    success = True
                except (xnat.exceptions.XNATError, RequestException) as exception:
                    self.log.warning('Encountered XNAT error during upload: {}'.format(exception))
                    if tries > 0:
                        self.log.warning('Retrying {} times'.format(tries))

            # Something went wrong, now forcefully try again
            max_retries = retries

            # Try multiple times to upload and try to avoid XNAT hiccups etc
            resource.clearcache()
            resource.files.clearcache()
            while location not in resource.files and retries > 0:
                resource.clearcache()
                resource.files.clearcache()
                retries -= 1

                try:
                    in_file_handle.seek(0)
                    resource.upload(in_file_handle, location, overwrite=True)
                except xnat.exceptions.XNATError:
                    # Allow exceptions to be raised again, just wait 10 seconds per try and retry
                    delay = 10 * (max_retries - retries)
                    self.log.warning('Got exception during upload, sleep {} seconds and retry'.format(
                        delay
                    ))
                    time.sleep(delay)

        # Check if upload is successful
        resource.clearcache()
        resource.files.clearcache()
        if location not in resource.files:
            raise xnat.exceptions.XNATUploadError("Problem with uploading to XNAT "
                                                  "(file not found, persisted after retries)")

        xnat_size = int(resource.files[location].size)
        if xnat_size != file_size:
            raise xnat.exceptions.XNATUploadError(
                "Problem with uploading to XNAT (file size differs uploaded {}, expected {})".format(
                    xnat_size, file_size
                )
            )
        else:
            self.log.info('It appears the file is uploaded to {} with a file size of {}'.format(
                resource.files[location].fulluri,
                xnat_size
            ))

    def _find_objects(self,
                      url: URL,
                      create: bool = False,
                      use_regex: bool = False):
        self.log.info('Locating {}'.format(url))
        if not url.path.startswith('/data/'):
            raise ValueError('Resources to be located should have a path starting with /data/')

        # Create a search uri
        location = self._path_to_dict(url.path)

        if 'resources' not in location:
            raise ValueError('All files should be located inside a resource, did not'
                             ' find resources level in {}'.format(location))
        # Sort xsi type directives neatly
        types = {
            'resources': 'xnat:resourceCatalog'
        }
        for key in location.keys():
            option1 = (key.rstrip('s') + '_type')
            option2 = (key + '_type')
            if option1 in url.query:
                types[key] = url.query[option1][0]
            if option2 in url.query:
                types[key] = url.query[option2][0]

        items = None
        # Parse location part by part
        for object_type, object_key in location.items():
            # We don't want to go into files, those are put but not created
            # and they get via the resources
            if object_type == 'files':
                break

            self.log.info('Locating {} / {} in {}'.format(object_type, object_key, items))
            new_items = self._resolve_url_part(object_type, object_key, use_regex=use_regex, parents=items)

            if len(new_items) == 0:
                if not create:
                    raise ValueError('Could not find data parent_object at {} (No values at level {})'.format(url,
                                                                                                              object_type))
                elif items is not None and len(items) == 1:
                    self.log.debug('Items: {}'.format(items))
                    parent_object = items[0]

                    # Get the required xsitype
                    if object_type in types:
                        xsi_type = types[object_type]
                    else:
                        raise ValueError(
                            'Could not find the correct xsi:type for {} (available hints: {})'.format(object_type,
                                                                                                      types))

                    if '*' in object_key or '?' in object_key or '[' in object_key or ']' in object_key:
                        raise ValueError('Illegal characters found in name of object_key'
                                         ' to create! (characters ?*[] or illegal!), found: {}'.format(object_key))

                    self.log.info('Creating new object under {} with type {}'.format(parent_object.uri, xsi_type))

                    # Create the object with the correct secondary lookup
                    cls = self.xnat.XNAT_CLASS_LOOKUP[xsi_type]
                    kwargs = {cls.SECONDARY_LOOKUP_FIELD: object_key}
                    try:
                        cls(parent=parent_object, **kwargs)
                    except xnat.exceptions.XNATResponseError:
                        self.log.warning(('Got a response error when creating the object {} (parent {}),'
                                          ' continuing to check if creating was in a race'
                                          ' condition and another processed created it').format(
                            object_key,
                            parent_object,
                        ))

                    new_items = self._resolve_url_part(object_type, object_key, use_regex=use_regex, parents=items)

                    if len(new_items) != 1:
                        raise ValueError('There appears to be a problem creating the object_key!')
                else:
                    raise ValueError('To create an object, the path should point to a unique parent'
                                     ' object! Found {} matching items: {}'.format(len(items), items))
            # Accept the new items for the new level scan
            items = new_items

        return items

    def _resolve_url_part(self, level, query=None, use_regex=False, parents=None):
        """
        Get all matching projects

        :param dict query: the query to find projects to match for
        :return:
        """
        # If there are no parents, work directly on the session
        if parents is None:
            parents = [self.xnat]

        if query is None:
            query = '.*' if use_regex else '*'

        self.log.info('Find {}: {} (parents: {})'.format(level, query, parents))

        # Get all objects
        objects = []
        for parent in parents:
            extra_options = getattr(parent, level)
            if use_regex:
                objects.extend(x for x in extra_options.values() if
                               re.match(query, getattr(x, extra_options.secondary_lookup_field)) or x.id == query)
            elif all(x not in query for x in '*?[]'):
                if query in extra_options:
                    objects.append(extra_options[query])
            else:
                objects.extend(x for x in extra_options.values() if
                               fnmatch.fnmatchcase(getattr(x, extra_options.secondary_lookup_field),
                                                   query) or x.id == query)

        self.log.info('Found: {}'.format(objects))

        return objects

    def _expand_project(self, urlsample: URLSample):
        # Determine project name/id
        url = urlsample.data_url
        path_prefix, project = url.path.split('/projects/', 1)

        query = dict(url.query)
        query['projects'] = project

        if 'resources' not in query:
            query['resources'] = 'DICOM'

        # Create sample copy with new URL set
        new_url = url.with_path(path_prefix + '/search').with_query(query)
        new_sample = urlsample.model_copy()
        new_sample.data_url = new_url

        # Forward the expanding to the search
        print(f'New sample for search: {new_sample}')
        return self._expand_search(new_sample)

    def _expand_search(self, urlsample: URLSample):
        # Parse the query
        url = urlsample.data_url
        query = url.query

        # Check if all fields given are valid fieldnames
        valid_fields = ("projects",
                        "subjects",
                        "experiments",
                        "scans",
                        "resources",
                        "id",
                        "label",
                        "insecure",
                        "verify",
                        "regex")

        valid_query = True
        for key in query.keys():
            if key not in valid_fields:
                self.log.error('Using invalid query field {} options are {}!'.format(key,
                                                                                     valid_fields))
                valid_query = False

        if not valid_query:
            raise ValueError('The query was malformed, see the error log for details.')

        use_regex = query.get('regex', '0').lower() in ['1', 'true']
        insecure = query.get('insecure', '0') in ['true', '1']
        verify = query.get('verify', '1') in ['true', '1']

        # Make sure we are connect to the correct server
        self.connect(url.host, insecure=insecure, verify=verify)

        # Create the url version for the search
        default = '.*' if use_regex else '*'
        search_path = URL('/data/archive/projects/{p}/subjects/{s}/experiments/{e}/scans/{sc}/resources/{r}'.format(
            p=query.get('projects', default),
            s=query.get('subjects', default),
            e=query.get('experiments', default),
            sc=query.get('scans', default),
            r=query.get('resources', default)
        ))

        # Find all matching resources
        resources = self._find_objects(search_path, use_regex=use_regex)

        # Format the new expanded urls
        urlsamples = []
        for resource in resources:
            match = re.match(
                r'/data(/archive)?/projects/(?P<project>[a-zA-Z0-9_\-]+)/subjects/(?P<subject>[a-zA-Z0-9_\-]+)/experiments/(?P<experiment>[a-zA-Z0-9_\-]+)/scans/(?P<scan>[a-zA-Z0-9_\-]+)/resources/(?P<resource>[a-zA-Z0-9_\-]+).*',
                resource.uri
            )

            project = self.xnat.projects[match.group('project')]
            subject = project.subjects[match.group('subject')]
            experiment = subject.experiments[match.group('experiment')]
            scan = experiment.scans[match.group('scan')]

            newpath = resource.uri
            if not newpath.startswith('/data/archive/'):
                newpath = newpath.replace('/data/', '/data/archive/', 1)
            newurl = url.with_path(newpath).with_query(None).with_fragment(None)

            # Determine the ID of the sample
            newurlsample = URLSample(
                data_url=newurl,
                project_name=project.name,
                subject_label=subject.label,
                experiment_label=experiment.label,
                experiment_date=experiment.date,
                scan_id=scan.id,
                scan_type=scan.type,
                filename=resource.label,
            )
            urlsamples.append((f"{experiment.id}_{scan.id}_{resource.label}", newurlsample))

        return tuple(urlsamples)


