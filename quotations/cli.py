import csv
import sys
import uuid

from docx import Document

from quotations import generate_quote_from_template


def main():
    if len(sys.argv) < 3:
        print('usage: FIXME <path-to-template> <path-to-data>')
        sys.exit(1)

    _, template_path, replacements_path = sys.argv

    replacements = {
        row['variable']: row['value'] for row in csv.DictReader(open(replacements_path))
    }
    quote_document = generate_quote_from_template(Document(template_path), replacements)

    output_filename = 'generated-proposal-{}.docx'.format(uuid.uuid4().hex)

    quote_document.save(output_filename)

    print(output_filename)
