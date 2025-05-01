import datetime
import os
import re

from yarl import URL

from datmat.models import URLSample, PathSample
from datmat.plugins import XNATStorage

# TODO: What happens when we try to access a protected (visible, but not accessible) XNAT project?
#       XNATpy shows an empty subject list.
# TODO: How is the 403 error from trying to access a private (not visible) XNAT project handled?

def make_path_dicom(url, project_id, subject_id, experiment_id, scan_id):
    url = f"{url}/data/archive/" \
          + f"projects/{project_id}/" \
          + f"subjects/{subject_id}/" \
          + f"experiments/{experiment_id}/" \
          + f"scans/{scan_id}/" \
          + f"resources/DICOM"
    return url


def test_xnat_expand_url(xnat_url_fixture):
    xnat_url, metadata = xnat_url_fixture

    plugin = XNATStorage()
    inurlsample = URLSample(data_url=xnat_url)
    expected_outurlsample = URLSample(
        data_url=xnat_url,
        project_name=metadata['project_name'],
        subject_label=metadata['subject_label'],
        experiment_label=metadata['experiment_label'],
        experiment_date=metadata['experiment_date'],
        scan_id=metadata['scan_id'],
        scan_type=metadata['scan_type']
    )

    expanded_url = plugin.expand_url(inurlsample)
    assert expanded_url == expected_outurlsample


def test_xnat_expand_url_search_single(xnat_url_fixture):
    _, metadata = xnat_url_fixture

    plugin = XNATStorage()
    xnat_search_url = URL(f"xnat+https://{metadata['base_url']}/search"
                          + f"?projects={metadata['project_name']}"
                          + f"&subjects={metadata['subject_label']}"
                          + f"&experiments=*"
                          + f"&scans={metadata['scan_id']}"
                          + f"&resources=DICOM")

    inurlsample = URLSample(data_url=xnat_search_url)

    expected_url = URL("xnat+https://xnat.health-ri.nl/data/archive/projects/sandbox/subjects/BMIAXNAT_S17618"
                       + "/experiments/BMIAXNAT_E69813/scans/5/resources/718274")

    expected_outurlsample = URLSample(
        data_url=expected_url,
        project_name=metadata['project_name'],
        subject_label=metadata['subject_label'],
        experiment_label=metadata['experiment_label'],
        experiment_date=metadata['experiment_date'],
        scan_id=metadata['scan_id'],
        scan_type=metadata['scan_type'],
        filename='DICOM',
    )

    expanded_url = plugin.expand_url(inurlsample)

    assert expanded_url == (('BMIAXNAT_E69813_5_DICOM', expected_outurlsample),)


def test_xnat_fetch_url(xnat_urlsample_fixture, tmp_path):
    xnat_urlsample, metadata = xnat_urlsample_fixture
    plugin = XNATStorage()
    response = plugin.fetch_url(xnat_urlsample, tmp_path)
    assert isinstance(response, PathSample)
    assert response.project_name == metadata['project_name']
    assert response.subject_label == metadata['subject_label']
    assert response.experiment_label == metadata['experiment_label']
    assert str(response.experiment_date) == metadata['experiment_date']
    assert response.scan_id == metadata['scan_id']
    assert response.scan_type == metadata['scan_type']
    assert response.filename == 'DICOM/files'

    # Cast paths to posix before comparison to avoid issues with / vs \
    match = re.match(
        fr"{tmp_path.as_posix()}/datmat_xnat_([0-9]+)_tmp([a-zA-Z0-9_\-]+)/{metadata['experiment_label']}/scans/{metadata['scan_id']}-([a-zA-Z0-9_\-]+)/resources/DICOM/files",
        str(response.data_path.as_posix())
    )

    assert match
    assert response.data_path.exists()


def test_xnat_expand_project():
    xnat_project_url = URL(
        "xnat+http://xnat.health-ri.nl/projects/sandbox?scans=*T1*"
    )
    inurlsample = URLSample(data_url=xnat_project_url)

    plugin = XNATStorage()

    result = plugin.expand_url(inurlsample)

    print([x[0] for x in result])
    print(sorted([x[0] for x in result]))
    assert sorted([x[0] for x in result]) == ['BMIAXNAT12_E02329_6_DICOM', 'BMIAXNAT15_E02599_6_DICOM',
                                              'BMIAXNAT36_E01628_6_DICOM', 'BMIAXNAT_E163574_6_DICOM',
                                              'BMIAXNAT_E69813_6_DICOM', 'BMIAXNAT_E82572_6_DICOM']

    assert result[0] == ('BMIAXNAT12_E02329_6_DICOM',
                         URLSample(
                             data_url=URL('xnat+http://xnat.health-ri.nl/data/archive/projects/sandbox/subjects/BMIAXNAT12_S00261/experiments/BMIAXNAT12_E02329/scans/6/resources/1097057'),
                             project_name='sandbox',
                             subject_label='SUBJECT001',
                             experiment_label='SUBJECT001',
                             experiment_date=datetime.date(2000, 1, 1),
                             scan_id='6',
                             scan_type='T1',
                             filename='DICOM',
                             timepoint=None,
                         ))


