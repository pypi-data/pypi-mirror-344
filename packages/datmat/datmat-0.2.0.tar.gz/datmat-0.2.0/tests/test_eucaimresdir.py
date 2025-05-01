import glob
import re

import datmat
from pathlib import Path

def test_writing_sample(eucaim_samples):
    samples, dest_folder = eucaim_samples
    dest_url = f'eucaimresdir://{dest_folder}'
    outpath_list = []
    for sample in samples:
        result, outpath = datmat.push_sink_data(sample, dest_url)
        outpath_list.append(outpath)
        assert Path(outpath) == Path(dest_folder)
        assert result is True

    dest_path = Path(dest_folder)
    assert (dest_path / 'sandbox' / '001'/ 'BL' / '4_T1' / 'DICOM' / 'files').exists() == True
    assert (dest_path / 'sandbox' / '001'/ 'BL' / '5_FLAIR' / 'DICOM' / 'files').exists() == True
    assert (dest_path / 'sandbox' / '002'/ 'FU' / '5_T1' / 'DICOM' / 'files').exists() == True
    assert (dest_path / 'sandbox' / '002'/ 'FU' / '3_FLAIR' / 'DICOM' / 'files').exists() == True


def test_materialize(xnat_subject_fixture, tmp_path):
    download_dir = tmp_path / 'download_dir'
    download_dir.mkdir()
    output_dir = tmp_path / 'output'
    output_dir.mkdir()

    inurl, metadata = xnat_subject_fixture
    outurl = f'eucaimresdir://{output_dir}'

    outpath = datmat.materialize(inurl, outurl, tempdir=download_dir)
    
    assert Path(outpath) == Path(output_dir)
    # file_folders = glob.glob(fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/*")
    # print(files)
    snapshot_files = glob.glob(fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/SNAPSHOTS/files/**")
    assert snapshot_files
    dicom_files = glob.glob(fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/DICOM/files/**")
    assert dicom_files
    print(snapshot_files)
    match = re.match(
       fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/SNAPSHOTS/files/[^/]+\.gif",
       snapshot_files[0])
    assert match
    match = re.match(
        fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/DICOM/files/[^/]+\.dcm",
        dicom_files[0])
    assert match
