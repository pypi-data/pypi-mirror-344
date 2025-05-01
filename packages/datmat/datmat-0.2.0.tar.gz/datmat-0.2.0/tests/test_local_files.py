import datmat
from datmat.models import PathSample


def test_pull_file(tmp_files):
    source_file, dest_folder = tmp_files
    print(f'Using {source_file=} and {dest_folder=}')
    response = datmat.pull_source_data(source_file.as_uri(),
                                       f'{dest_folder}',
                                       'test01')
    expected_response_path = dest_folder / 'input.txt'
    expected_response = {'test01': (PathSample(data_path=expected_response_path),)}

    assert response == expected_response
    assert response['test01'][0].data_path == expected_response_path
    assert (dest_folder / 'input.txt').exists()


def test_materialize_file(tmp_files):
    source_file, dest_folder = tmp_files
    temp_folder = dest_folder / 'temp'
    temp_folder.mkdir()
    print(f'Using {source_file=} and {dest_folder=}')
    outpath = datmat.materialize(source_file.as_uri(),
                                              f'file://{dest_folder}/output.txt',
                                              f'{temp_folder}')
    assert outpath == str(dest_folder / 'output.txt')
    assert (dest_folder / 'output.txt').exists()
