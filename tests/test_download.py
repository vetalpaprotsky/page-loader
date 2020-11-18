from page_loader.download import download


def test_download(requests_mock, tmpdir):
    page_content = 'page content...'
    page_url = 'http://this.is.a.test/page'
    requests_mock.get(page_url, text=page_content)

    file_path = tmpdir / 'this-is-a-test-page.html'
    assert download(page_url, str(tmpdir)) == file_path

    with open(file_path) as file:
        assert file.read() == page_content
