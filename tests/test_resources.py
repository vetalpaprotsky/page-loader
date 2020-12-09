import pytest
from page_loader.resources import get_content
from page_loader.exceptions import HTTPError


@pytest.mark.parametrize(
    'content,decode,expected',
    [
        (bytes('text data', encoding='utf-8'), True, 'text data'),
        (b'\xFF', False, b'\xFF'),
    ]
)
def test_get_content(content, decode, expected, requests_mock):
    url = 'http://test.com'
    requests_mock.get(url, content=content)

    assert get_content(url, decode=decode) == expected


def test_get_content_when_resource_is_unavailable(requests_mock):
    url = 'http://test.com'
    requests_mock.get(url, status_code=500)

    with pytest.raises(HTTPError):
        get_content(url)
