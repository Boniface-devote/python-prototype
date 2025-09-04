import json
import subprocess
import sys
from flask import Blueprint, jsonify, render_template, request, send_file
from .data_extraction import extract_certificate_data, extract_data_from_pdf
from .processing import get_available_templates, process_excel_and_pdf, laban_dir, malaba_dir, possiano_dir, busia_dir, modified_excel_global, modified_pdf_global, data_global, pdf_type_global
import re
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # templates = get_available_templates()
    # return render_template('upload_form.html', data=None, modified=False, templates=templates)
    normal_templates = get_available_templates(laban_dir)
    maritime_templates = get_available_templates(malaba_dir)
    possiano_templates= get_available_templates(possiano_dir)
    busia_templates = get_available_templates(busia_dir)
    return render_template('upload_form.html', normal_templates=normal_templates, maritime_templates=maritime_templates, possiano_templates=possiano_templates, busia_templates=busia_templates)

@bp.route('/process/<pdf_type>', methods=['POST'])
def process_pdf(pdf_type):
    if pdf_type not in ['normal', 'maritime', 'possiano', 'busia']:
        return "Invalid PDF type", 400

    data = None
    modified = False
    json_data = None
    
    if 'pdf_file' not in request.files:
        return "No PDF file part"
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected PDF file"
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        pdf_content = pdf_file.read()
        data = extract_data_from_pdf(pdf_content, pdf_type)
        
        # Get Freight Number from form input
        freight_number = request.form.get('freight_number', '').strip()
        try:
            freight_number = int(freight_number) if freight_number else None
        except ValueError:
            freight_number = None

        # Get Container Type and Number of Containers (for maritime only)
        container_type = request.form.get('container_type', '') if pdf_type == 'maritime' else ''
        num_containers = 1
        if pdf_type == 'maritime':
            num_containers = request.form.get('num_containers', '').strip()
            try:
                num_containers = int(num_containers) if num_containers else 1
            except ValueError:
                num_containers = 1

        # Process Excel and PDF
        template_file = request.form.get('template_file', '').strip()
        modified_excel, modified_pdf, json_data = process_excel_and_pdf(
            data, pdf_type, template_file, freight_number, container_type, num_containers
        )
        modified = modified_excel is not None

    normal_templates = get_available_templates(laban_dir)
    maritime_templates = get_available_templates(malaba_dir)
    possiano_templates = get_available_templates(possiano_dir)
    busia_templates = get_available_templates(busia_dir)
    return render_template(
        'upload_form.html',
        data=data,
        json_data=json_data,
        modified=modified,
        normal_templates=normal_templates,
        maritime_templates=maritime_templates,
        possiano_templates=possiano_templates,
        busia_templates=busia_templates,
    )

@bp.route('/download_excel')
def download_excel():
    from .processing import modified_excel_global, data_global, pdf_type_global
    if modified_excel_global is None:
        return "No modified Excel available"
    
    # Determine download name based on pdf_type and data
    download_name = 'modified.xlsx'
    if data_global and pdf_type_global:
        identifier = None
        if pdf_type_global in ['maritime', 'busia', 'possiano'] and 'bl' in data_global:
            identifier = data_global['bl']
        elif pdf_type_global == 'normal' and 'transport_id' in data_global:
            identifier = data_global['transport_id']
        if identifier:
            # Sanitize identifier for safe filename
            identifier = re.sub(r'[^\w\-]', '_', identifier.strip())
            download_name = f'Proforma_Invoice_{identifier}.xlsx'

    modified_excel_global.seek(0)
    return send_file(
        modified_excel_global,
        as_attachment=True,
        download_name=download_name,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@bp.route('/download_pdf')
def download_pdf():
    from .processing import modified_pdf_global, data_global, pdf_type_global
    if modified_pdf_global is None:
        return "No PDF available"
    
    # Determine download name based on pdf_type and data
    download_name = 'modified.pdf'
    if data_global and pdf_type_global:
        identifier = None
        if pdf_type_global in ['maritime', 'busia', 'possiano'] and 'bl' in data_global:
            identifier = data_global['bl']
        elif pdf_type_global == 'normal' and 'transport_id' in data_global:
            identifier = data_global['transport_id']
        if identifier:
            # Sanitize identifier for safe filename
            identifier = re.sub(r'[^\w\-]', '_', identifier.strip())
            download_name = f'Proforma_Invoice_{identifier}.pdf'

    modified_pdf_global.seek(0)
    return send_file(
        modified_pdf_global,
        as_attachment=True,
        download_name=download_name,
        mimetype='application/pdf'
    )

#Invesco flagging routes
@bp.route("/flagging/", methods=["GET", "POST"])
def flagging_index():
    extracted_data = None
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file uploaded", 400
        pdf_file = request.files["pdf"]
        if pdf_file.filename == "":
            return "No selected file", 400

        extracted_data = extract_certificate_data(pdf_file)

    return render_template("index.html", data=extracted_data)

@bp.route("/flagging/fill-form", methods=["POST"])
def fill_form():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        login_script = os.path.join(base_dir, "login.py")
        result = subprocess.run(
            [sys.executable, login_script],
            input=json.dumps(data),
            text=True,
            capture_output=True
        )
        return jsonify({"status": "success", "output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
