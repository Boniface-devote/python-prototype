import xlwings as xw
from io import BytesIO
import os
import glob
import json
import tempfile

# Directory containing Excel templates
TEMPLATES_DIR = 'template'  # Change this to your template directory path

# Global variables to store the modified files in memory
modified_excel_global = None
modified_pdf_global = None

def get_available_templates():
    """Get list of available Excel templates from the templates directory"""
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        return []
    
    excel_files = glob.glob(os.path.join(TEMPLATES_DIR, '*.xlsx'))
    return [os.path.basename(f) for f in excel_files]


def process_excel_and_pdf(data, pdf_type, template_file, freight_number, container_type='', num_containers=1):
    """
    Process extracted data, update Excel template with xlwings, 
    force recalculation, and generate a real Excel + PDF.
    """
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    modified_excel = None
    modified_pdf = None

    # Check for selected template
    if not template_file:
        return None, None, json_data

    template_path = os.path.join(TEMPLATES_DIR, template_file)
    if not os.path.exists(template_path):
        return None, None, json_data

    # Use a temporary folder for saving
    with tempfile.TemporaryDirectory() as tmpdir:
        modified_xlsx_path = os.path.join(tmpdir, "modified.xlsx")
        modified_pdf_path = os.path.join(tmpdir, "modified.pdf")

        # Open Excel with xlwings
        app = xw.App(visible=False)
        wb = app.books.open(template_path)
        ws = wb.sheets[0]

        # --- Insert data ---
        if pdf_type == 'normal':
            if 'attestation_number' in data:
                ws.range("E6").value = f"FERI/AD: {data['attestation_number']}"
                ws.range("B11").value = f"CERTIFICATE (FERI/ADR/AD) No : {data['attestation_number']}"
            if 'forwarding_agent' in data:
                ws.range("B8").value = f"DEBTOR: {data['forwarding_agent']}"
            if 'importateur' in data:
                ws.range("B10").value = f"IMPORTER: {data['importateur']}"
            if 'transport_id' in data:
                ws.range("B14").value = data['transport_id']
            if 'cbm' in data:
                cbm_value = float(data['cbm'].replace(' CBM', ''))
                ws.range("D14").value = cbm_value
            if freight_number is not None:
                ws.range("D18").value = freight_number

        else:  # maritime
            if 'feri_number' in data:
                ws.range("E6").value = f"FERI/AD: {data['feri_number']}"
                ws.range("B11").value = f"CERTIFICATE (FERI/ADR/AD) No : {data['feri_number']}"
            if 'transitaire' in data:
                ws.range("B8").value = f"DEBTOR: {data['transitaire']}"
            if 'importateur' in data:
                ws.range("B10").value = f"IMPORTER: {data['importateur']}"
            if 'bl' in data:
                ws.range("B14").value = data['bl']
            if 'cbm' in data and container_type not in ['40FT', '20FT']:
                cbm_value = float(data['cbm'].replace(' CBM', ''))
                ws.range("D14").value = cbm_value
            if container_type == '40FT':
                ws.range("D14").value = 110
            elif container_type == '20FT':
                ws.range("D14").value = 60
            ws.range("E14").value = num_containers
            ws.range("D17").value = num_containers
            ws.range("D18").value = num_containers * 250
            if freight_number is not None:
                ws.range("D18").value = freight_number

        # --- Force Excel to recalc all formulas ---
        wb.app.calculate()

        # Save Excel
        wb.save(modified_xlsx_path)

        # Export to PDF using Excel's engine
        wb.api.ExportAsFixedFormat(0, modified_pdf_path)

        wb.close()
        app.quit()

        # Load into memory buffers
        with open(modified_xlsx_path, "rb") as f:
            modified_excel = BytesIO(f.read())
        with open(modified_pdf_path, "rb") as f:
            modified_pdf = BytesIO(f.read())

        # Store in globals
        global modified_excel_global, modified_pdf_global
        modified_excel_global = modified_excel
        modified_pdf_global = modified_pdf

    return modified_excel, modified_pdf, json_data
