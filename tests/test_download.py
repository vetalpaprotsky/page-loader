import os
from tests.utils import load_fixture, whitespaces_removed
from page_loader.download import download


def test_download_page_without_resources(requests_mock, tmpdir):
    page_content = '<html></html>'
    page_url = 'http://this.is.a.test/page'
    requests_mock.get(page_url, text=page_content)

    page_path = tmpdir / 'this-is-a-test-page.html'
    assert download(page_url, str(tmpdir)) == page_path

    with open(page_path) as file:
        page = whitespaces_removed(file.read())
        expected = whitespaces_removed(page_content)
        assert page == expected

    resources_dir_path = tmpdir / 'this-is-a-test-page_files'
    assert not os.path.isdir(resources_dir_path)


# TODO: refactor this.
def test_download_page_with_resources(requests_mock, tmpdir):
    page_content = load_fixture('page.html')
    application_css_content = 'h3 { color: red; }'
    application_js_content = 'alert("Hexlet");'
    runtime_js_content = 'alert("JS");'
    python_png_binary = b'\xAB\xBC\xCD\xDE\xEF'
    page_url = 'https://ru.hexlet.io/courses'

    mocks = [
        (
            # the page itself and link href="/courses"
            page_url,
            page_content,
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
        if type(content) is bytes:
            requests_mock.get(url, content=content)
        else:
            requests_mock.get(url, text=content)

    page_path = tmpdir / 'ru-hexlet-io-courses.html'
    assert download(page_url, str(tmpdir)) == page_path

    with open(page_path) as file:
        # TODO: Come up with a better way to check whether pages are equal.
        page = whitespaces_removed(file.read())
        expected = whitespaces_removed(load_fixture('page_after_download.html'))
        assert sorted(page) == sorted(expected)

    recourses = [
        ('ru-hexlet-io-courses.html', page_content),
        ('ru-hexlet-io-assets-application.css', application_css_content),
        ('ru-hexlet-io-assets-application.js', application_js_content),
        ('ru-hexlet-io-packs-js-runtime.js', runtime_js_content),
        ('ru-hexlet-io-assets-professions-python.png', python_png_binary),
    ]
    resources_dir_path = tmpdir / 'ru-hexlet-io-courses_files'
    for name, content in recourses:
        recourse_path = resources_dir_path / name
        read_mode = 'rb' if type(content) is bytes else 'r'
        with open(recourse_path, read_mode) as file:
            assert file.read() == content
