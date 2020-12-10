import pytest
import os
from page_loader.utils import write_to_file, create_dir


@pytest.mark.parametrize(
    'content,read_mode',
    [
        ('text data', 'r'),
        (b'\xFF', 'rb'),
    ]
)
def test_write_to_file(content, read_mode, tmpdir):
    file_path = tmpdir / 'file.txt'
    write_to_file(content, file_path)

    with open(file_path, read_mode) as file:
        assert file.read() == content


def test_write_to_file_when_path_does_not_exist():
    with pytest.raises(OSError):
        write_to_file('content', 'non/existing/dir/path/file.txt')


def test_create_dir(tmpdir):
    dir_path = tmpdir / 'dir'
    create_dir(dir_path)

    assert os.path.isdir(dir_path)


def test_create_dir_when_path_does_not_exist():
    with pytest.raises(OSError):
        create_dir('non/existing/dir/path')
