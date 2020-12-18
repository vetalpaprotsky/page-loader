import pytest
from page_loader import resource
from page_loader.exceptions import NetworkError


@pytest.mark.parametrize(
    'content,decode,expected',
    [
        (bytes('text data', encoding='utf-8'), True, 'text data'),
        (b'\xFF', False, b'\xFF'),
    ]
)
def test_get(content, decode, expected, requests_mock):
    url = 'http://test.com'
    requests_mock.get(url, content=content)

    assert resource.get(url, decode=decode) == expected


@pytest.mark.parametrize('status_code', [404, 500])
def test_get_when_resource_is_unavailable(status_code, requests_mock):
    url = 'http://test.com'
    requests_mock.get(url, status_code=status_code)

    with pytest.raises(NetworkError):
        resource.get(url)
