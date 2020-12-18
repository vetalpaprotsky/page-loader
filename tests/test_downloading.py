import pytest
import os
from tests.utils import load_fixture, is_content_identical
from page_loader.downloading import download
from page_loader.exceptions import NetworkError, StorageError


def test_download_page_with_resources(requests_mock, tmpdir):
    page_html = load_fixture('page.html')
    application_css_content = load_fixture('page_resources/application.css')
    application_js_content = load_fixture('page_resources/application.js')
    runtime_js_content = load_fixture('page_resources/runtime.js')
    python_png_binary = load_fixture('page_resources/python.png', binary=True)
    page_url = 'https://ru.hexlet.io/courses'

    mocks = [
        (
            # the page itself and link href="/courses"
            page_url,
            page_html,
        ),
        (
            # link href="/assets/application.css"
            'https://ru.hexlet.io/assets/application.css',
            application_css_content,
        ),
        (
            # script src="/assets/application.js"
            'https://ru.hexlet.io/assets/application.js',
            application_js_content,
        ),
        (
            # script src="https://ru.hexlet.io/packs/js/runtime.js"
            'https://ru.hexlet.io/packs/js/runtime.js',
            runtime_js_content,
        ),
        (
            # img src="/assets/professions/python.png"
            'https://ru.hexlet.io/assets/professions/python.png',
            python_png_binary,
        ),
    ]
    for url, content in mocks:
        if isinstance(content, bytes):
            requests_mock.get(url, content=content)
        else:
            requests_mock.get(url, text=content)

    page_file_path = tmpdir / 'ru-hexlet-io-courses.html'
    assert download(page_url, str(tmpdir)) == page_file_path

    with open(page_file_path) as file:
        assert is_content_identical(
            file.read(),
            load_fixture('page_after_download.html')
        )

    resources = [
        ('ru-hexlet-io-courses.html', page_html),
        ('ru-hexlet-io-assets-application.css', application_css_content),
        ('ru-hexlet-io-assets-application.js', application_js_content),
        ('ru-hexlet-io-packs-js-runtime.js', runtime_js_content),
        ('ru-hexlet-io-assets-professions-python.png', python_png_binary),
    ]
    resources_dir_path = tmpdir / 'ru-hexlet-io-courses_files'
    for name, content in resources:
        resource_path = resources_dir_path / name
        read_mode = 'rb' if isinstance(content, bytes) else 'r'
        with open(resource_path, read_mode) as file:
            assert file.read() == content


def test_download_page_with_some_unavailable_resources(requests_mock, tmpdir):
    page_html = '''
        <html>
            <body>
                <img src="unavailable.png">
                <img src="available.png">
            <body>
        </html>
    '''
    page_url = 'http://test.com'
    requests_mock.get(page_url, text=page_html)
    requests_mock.get(page_url + '/unavailable.png', status_code=404)
    requests_mock.get(page_url + '/available.png', content=b'\xFF')

    download(page_url, str(tmpdir))

    resources_dir_path = tmpdir / 'test-com_files'
    assert os.path.isfile(tmpdir / 'test-com.html')
    assert not os.path.isfile(resources_dir_path / 'test-com-unavailable.png')
    assert os.path.isfile(resources_dir_path / 'test-com-available.png')


def test_download_page_without_resources(requests_mock, tmpdir):
    page_url = 'http://test.com'
    requests_mock.get(page_url, text='<html></html>')

    download(page_url, str(tmpdir))

    resources_dir_path = tmpdir / 'test-com_files'
    assert os.path.isfile(tmpdir / 'test-com.html')
    assert not os.path.isdir(resources_dir_path)


def test_download_unavailable_page(requests_mock, tmpdir):
    page_url = 'http://test.com'
    requests_mock.get(page_url, status_code=404)

    with pytest.raises(NetworkError):
        download(page_url, str(tmpdir))


def test_download_with_non_existing_output_dir(requests_mock):
    page_url = 'http://test.com'
    requests_mock.get(page_url, text='<html></html>')

    with pytest.raises(StorageError):
        download(page_url, 'non/existing/dir/path')
