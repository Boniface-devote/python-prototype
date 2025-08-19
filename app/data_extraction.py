import pdfplumber
import re
from io import BytesIO

def extract_data_from_pdf(pdf_content, pdf_type):
    """
    Extract structured data from the PDF content based on the PDF type (normal or maritime).
    """
    extracted = {}
    with pdfplumber.open(BytesIO(pdf_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Clean up text
    text = text.replace('\n', ' ').strip()

    if pdf_type == 'normal':
        # Attestation Number
        match = re.search(r'A\.D\s+N°\s*(\w+)', text)
        if match:
            extracted['attestation_number'] = match.group(1)

        # Importateur (only name)
        match = re.search(r'IMPORTATEUR\s*:\s*(.*?)(?=\s*(?:;|EXPORTATEUR))', text, re.DOTALL | re.IGNORECASE)
        if match:
            importateur_name = match.group(1).strip()
            # remove trailing "Importateur" word if it exists
            importateur_name = re.sub(r'\bIMPORTATEUR\b.*$', '', importateur_name, flags=re.IGNORECASE).strip()
            extracted['importateur'] = importateur_name

        # Exporter (only name)
        match = re.search(r'EXPORTATEUR\s*([^\n;]+?)(?=\s+Exportater|\s*;|TRANSITAIRE)', text, re.DOTALL | re.IGNORECASE)
        if match:
            exporter_name = match.group(1).strip()
            name_match = re.match(r'^[A-Za-z\s().&-]+', exporter_name)
            exporter_name = name_match.group(0).strip() if name_match else exporter_name
            if exporter_name.endswith(' E'):
                exporter_name = exporter_name[:-2].strip()
            extracted['exporter'] = exporter_name


        # Forwarding Agent (only name)
        match = re.search(r'TRANSITAIRE\s*:\s*([^\s;][^;]*?)(?:\s*Forwarding agent|DEST\.)', text, re.DOTALL)
        if match:
            forwarding_name = match.group(1).strip()
            name_match = re.match(r'^[A-Za-z\s().&-]+(?:\s*\([A-Za-z]+\)\s*[A-Za-z.]+)?', forwarding_name)
            extracted['forwarding_agent'] = name_match.group(0).strip() if name_match else forwarding_name

        # Transport ID
        match = re.search(r'TITRE DE TRANSPORT\s*:\s*(.+?)\s*TRANS', text)
        if match:
            extracted['transport_id'] = match.group(1).strip()

        # CBM (Cubic Meters)
        match = re.search(r'(\d+\.\d+\s*CBM)', text)
        if match:
            extracted['cbm'] = match.group(1).strip()

        # Gross Weight
        match = re.search(r'POIDS BRUT\s*:\s*([\d\.]+)\s*Kg', text)
        if match:
            extracted['gross_weight'] = float(match.group(1))

    else:  # maritime
        # FERI Number or Attestation Number
        match = re.search(r'(?:FERI N°|VALIDATION|A\.D\s+N°)\s*:\s*(\w+)', text)
        if match:
            extracted['feri_number'] = match.group(1)

         # Importateur (only name)
        match = re.search(r'IMPORTATEUR\s*:\s*(.*?)(?=\s*(?:;|EXPORTATEUR))', text, re.DOTALL | re.IGNORECASE)
        if match:
            importateur_name = match.group(1).strip()
            # remove trailing "Importateur" word if it exists
            importateur_name = re.sub(r'\bIMPORTATEUR\b.*$', '', importateur_name, flags=re.IGNORECASE).strip()
            extracted['importateur'] = importateur_name


        # Transitaire (only name)
        match = re.search(r'TRANSITAIRE\s*:\s*([^\s;][^;]*?)(?:\s*Forwarding agent|DEST\.|ADD:|$)', text, re.DOTALL)
        if match:
            forwarding_name = match.group(1).strip()
            name_match = re.match(r'^[A-Za-z\s().&-]+(?:\s*\([A-Za-z]+\)\s*[A-Za-z.]+)?', forwarding_name)
            extracted['transitaire'] = name_match.group(0).strip() if name_match else forwarding_name

        # BL (Bill of Lading)
        match = re.search(r'(?:BL|TITRE DE TRANSPORT)\s*:\s*(.+?)(?:\s*ARMATEUR|TRANS|$)', text)
        if match:
            extracted['bl'] = match.group(1).strip()

        # CBM (Cubic Meters)
        match = re.search(r'(\d+\.\d+\s*CBM)\s*(?=(?:POIDS|TEU|CONTENEUR|$))', text)
        if match:
            extracted['cbm'] = match.group(1).strip()

        # Gross Weight
        match = re.search(r'POIDS BRUT\s*:\s*([\d\.]+)\s*(?:Kg|T)', text)
        if match:
            extracted['gross_weight'] = float(match.group(1))

        # Exporter (only name)
        match = re.search(r'EXPORTATEUR\s*([^\n;]+?)(?=\s+Exportater|\s*;|TRANSITAIRE)', text, re.DOTALL | re.IGNORECASE)
        if match:
            exporter_name = match.group(1).strip()
            name_match = re.match(r'^[A-Za-z\s().&-]+', exporter_name)
            exporter_name = name_match.group(0).strip() if name_match else exporter_name
            if exporter_name.endswith(' E'):
                exporter_name = exporter_name[:-2].strip()
            extracted['exporter'] = exporter_name


    return extracted