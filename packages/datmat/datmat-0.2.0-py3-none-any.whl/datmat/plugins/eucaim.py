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

from .structureddirectory import StructuredDirectory


class EUCaimDirectory(StructuredDirectory):
    """
    The EUCAIM plugin is create to handle ``eucaimdir:///`` type or URLs.

    The URL scheme is rather simple: ``eucaimdir:///path/to/project`` and 
    resembles the FileSystem scheme:
    (see `wikipedia <http://en.wikipedia.org/wiki/File_URI_scheme>`_ for details)

    We do not make use of the ``host`` part and at the moment only support
    localhost (just leave the host empty) leading to ``eucaimdir:///`` URLs.

    .. warning:: This plugin ignores the hostname in the URL and does only
                 accept driver letters on Windows in the form ``c:/``
    """
    scheme = 'eucaimdir'

    def __init__(self):
        # initialize the instance and register the scheme
        super(EUCaimDirectory, self).__init__()

    def _sample_to_outpath(self, url, sample):
        return self.url_to_path(url / sample.project_name / sample.subject_label / sample.experiment_label / f'{sample.scan_id}_{sample.scan_type}')

