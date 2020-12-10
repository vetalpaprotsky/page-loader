import pytest
from page_loader.resources import get_content
from requests.exceptions import RequestException


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


@pytest.mark.parametrize('status_code', [404, 500])
def test_get_content_when_resource_is_unavailable(status_code, requests_mock):
    url = 'http://test.com'
    requests_mock.get(url, status_code=status_code)

    with pytest.raises(RequestException):
        get_content(url)
