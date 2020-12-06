import re
import os


def load_fixture(path):
    with open(os.path.join(os.getcwd(), 'tests', 'fixtures', path)) as file:
        return file.read()


def whitespaces_removed(string):
    return re.sub(r"\s+", '', string)


# FIXME: Not the best way to check whether two html pages have the same content.
def is_content_identical(html1, html2):
    return (
        sorted(whitespaces_removed(html1)) == sorted(whitespaces_removed(html2))
    )
