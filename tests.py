import pytest
from docx import Document

from quotations import generate_quote_from_template


@pytest.fixture
def template_doc():
    return Document()


def test_quote_replacement(template_doc):

    template_values = {'this_is': 'just my test', 'data': 'of simple things'}

    quote = generate_quote_from_template(template_doc, template_values)

    for variable, value in template_values.items():
        assert variable not in quote
        assert value in quote
