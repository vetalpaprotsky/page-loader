import os
import re


def load_fixture(path):
    with open(os.path.join(os.getcwd(), 'tests', 'fixtures', path)) as file:
        return file.read()


def whitespaces_removed(string):
    return re.sub(r"\s+", '', string)
