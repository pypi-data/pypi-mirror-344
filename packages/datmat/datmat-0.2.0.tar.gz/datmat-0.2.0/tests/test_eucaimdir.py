import glob
import re

import datmat
from pathlib import Path

def test_writing_sample(eucaim_samples):
    samples, dest_folder = eucaim_samples
    dest_url = f'eucaimdir://{dest_folder}'
    outpath_list = []
    for sample in samples:
        result, outpath = datmat.push_sink_data(sample, dest_url)
        outpath_list.append(outpath)
        assert Path(outpath) == Path(dest_folder)
        assert result is True

    dest_path = Path(dest_folder)
    assert (dest_path / 'sandbox' / '001'/ 'BL' / '4_T1').exists() == True
    assert (dest_path / 'sandbox' / '001'/ 'BL' / '5_FLAIR').exists() == True
    assert (dest_path / 'sandbox' / '002'/ 'FU' / '5_T1').exists() == True
    assert (dest_path / 'sandbox' / '002'/ 'FU' / '3_FLAIR').exists() == True


def test_materialize(xnat_subject_fixture, tmp_path):
    download_dir = tmp_path / 'download_dir'
    download_dir.mkdir()
    output_dir = tmp_path / 'output'
    output_dir.mkdir()

    inurl, metadata = xnat_subject_fixture
    outurl = f'eucaimdir://{output_dir}'

    outpath = datmat.materialize(inurl, outurl, tempdir=download_dir)
    
    assert Path(outpath) == Path(output_dir)
    files = glob.glob(fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/*")
    assert files
    match = re.match(
        fr"{output_dir.as_posix()}/{metadata['project_name']}/{metadata['subject_label']}/{metadata['experiment_label']}/{metadata['scan_id']}_{metadata['scan_type']}/[^/]+\.dcm",
        files[0])
    assert match
