import pytest
from page_loader.utils import url_to_file_name


@pytest.mark.parametrize(
    'url,expected',
    [
        ('http://test.com', 'test-com.html'),
        ('https://test.com', 'test-com.html'),
        ('//test.com', 'test-com.html'),
        ('http://test.com/', 'test-com.html'),
        ('http://test.com/page', 'test-com-page.html'),
        ('http://test.com/page.html', 'test-com-page.html'),
        ('http://test.com/image.png', 'test-com-image.png'),
        ('http://testing.1.2.3.com', 'testing-1-2-3-com.html'),
        ('http://test.com/scripts/main-js.js', 'test-com-scripts-main-js.js'),
    ]
)
def test_url_to_file_name(url, expected):
    assert url_to_file_name(url) == expected
