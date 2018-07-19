from docx import Document

FILENAME='SLB Consulting Proposal-Template.docx'
TEMPLATE_CLIENT='SLB Consulting'
CLIENT='Michael Joseph'

doc = Document(FILENAME)

# FIXME: header / footer
# for section in doc.sections:
#     print(dir(section))
#     print(section.header)

print(dir(doc.paragraphs[0].runs[0]))
for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        if TEMPLATE_CLIENT in run.text:
            run.text = run.text.replace(TEMPLATE_CLIENT, CLIENT)

    if 'SLB Consulting' in paragraph.text:
        paragraph.text = paragraph.text.replace('SLB Consulting', CLIENT)

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if TEMPLATE_CLIENT in paragraph.text:
                    paragraph.text = paragraph.text.replace(TEMPLATE_CLIENT, CLIENT)

doc.save('{}-proposal.docx'.format(CLIENT))

