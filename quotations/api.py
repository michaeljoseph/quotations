import csv
import io
import uuid

from docx import Document
from flask import Flask, flash, redirect, render_template, request, send_file

from quotations import generate_quote_from_template

ALLOWED_TEMPLATE_EXTENSIONS = ['docx']
ALLOWED_REPLACEMENTS_EXTENSIONS = ['csv']
app = Flask(__name__)


def allowed_file(upload, extensions):
    return (
        '.' in upload.filename
        and upload.filename.rsplit('.', 1)[1].lower() in extensions
    )


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)

        template = request.files['template']
        replacements = request.files['replacements']

        # if user does not select file, browser also
        # submit an empty part without filename
        if template.filename == '' or replacements.filename == '':
            print('No selected files')
            return redirect(request.url)

        if allowed_file(template, ALLOWED_TEMPLATE_EXTENSIONS):
            if allowed_file(replacements, ALLOWED_REPLACEMENTS_EXTENSIONS):

                cfp = io.StringIO()
                cfp.write(
                    replacements.read().decode('utf-8')
                )
                cfp.seek(0)

                replacements = {
                    row['variable']: row['value']
                    for row in csv.DictReader(cfp)
                }
                document = generate_quote_from_template(
                    Document(template), replacements
                )

                fp = io.BytesIO()
                document.save(fp)
                fp.seek(0)
                return send_file(
                    fp,
                    as_attachment=True,
                    attachment_filename='generated-proposal-{}.docx'.format(
                        uuid.uuid4().hex
                    ),
                )

    return render_template('index.html')
