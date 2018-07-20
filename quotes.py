"""
TODO:
- [] cli: quotes.py <path-to-template> <path-to-data>
"""
import uuid

from docx import Document
from jinja2 import Template

def template_render(template, replacements):
    return Template(template).render(replacements)

def main(template_document, replacements):
    doc = Document(template_document)

    # FIXME: header / footer
    # for section in doc.sections:
    #     print(dir(section))
    #     print(section.header)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.text = template_render(run.text, replacements)

        paragraph.text = template_render(paragraph.text, replacements)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.text = template_render(paragraph.text, replacements)

    output_filename = 'generated-proposal-{}.docx'.format(uuid.uuid4().hex)
    print(output_filename)
    doc.save(output_filename)

if __name__ == '__main__':
    TEMPLATE_FILENAME='Proposal-Template.docx'
    replacements = {
        'client_name': 'Michael Joseph',
        'system_size': '27.2 kWp',
        'annual_production': '43 683.2 kWh/a',
        'cost': 'R 476 292.54',
    }
    main(TEMPLATE_FILENAME, replacements)
