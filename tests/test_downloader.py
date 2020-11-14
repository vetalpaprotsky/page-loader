from page_loader.downloader import download


def test_download():
    assert download() == 'Loading...'
