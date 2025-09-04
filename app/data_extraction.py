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

        # 1. Look for "CBM :" pattern (most reliable)
        match = re.search(r'CBM\s*[:\-]?\s*(\d+(?:\.\d+)?)', text)

        # 2. If not found, look for "TN: ... CBM: ..."
        if not match:
            match = re.search(r'CBM\s*:\s*(\d+(?:\.\d+)?)', text)

        # 3. If still not found, fallback to generic "X.XXX CBM"
        if not match:
            match = re.search(r'(\d+(?:\.\d+)?)\s*CBM', text)

        if match:
            extracted['cbm'] = float(match.group(1))

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

###################
# Invesco Flagging
###################
# Mapping of DISCHARGE-LOCATION to OUT-BOUND-Border
BORDER_MAPPING = {
    "KASENYI": "NTOROKO",
    "OMBAY": "LIA",
    "LIA": "LIA",
    "KASINDI": "MPONDWE",
    "GOLI": "GOLI",
    "KAROMBO": "PADEA",
    "VURRA": "VURRA",
    "RUZIZI": "KATUNA",
    "CYANIKA": "CYANIKA"
}

# --- Extraction function for Normal Certificate ---
def extract_normal_certificate_data(extracted_text):
    patterns = {
        "Certificate_No": r"A\.D\s+N°\s+(\S+)",
        "Importer": r"IMPORTATEUR\s*:\s*(.+)",
        "Exporter": r"EXPORTATEUR\s+(.+)",
        "Forwarder": r"TRANSITAIRE\s*:\s*(.+)",
        "Entry_No": r"TITRE DE TRANSPORT\s*:\s*(.+?)\s*TRANS",
        "Final_Destination": r"DEST\. FINALE EN RDC\s*:\s*([A-Z]+)",
        "Discharge_Place": r"LIEU DE\s+([A-Z]+)\s+\d{2}/\d{2}/\d{4}",
        "Transport": r"MOYEN DE TRANSPORT\s*:\s*([\w/ ]+?)\s+VG",
    }

    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        data[key] = match.group(1).strip() if match else None

    # Block-based parse for FOB/Charges
    block_match = re.search(r"VALEUR FOB.*?TOTAL", extracted_text, re.S | re.I)
    if block_match:
        block_text = block_match.group(0)
        numbers = re.findall(r"\d+\.\d+", block_text)
        if len(numbers) >= 4:
            data["FOB_Value"] = numbers[0]
            data["Base_Freight"] = numbers[1]
            data["Additional_Fees"] = numbers[2]
            data["Insurance"] = numbers[3]
            data["transporterName"] = "OWN"
            data["validationNotes"] = "please verify"

    # Extract Goods Descriptions
    descriptions_list = []
    start_marker = r"MARCHANDISE\s+N\.C\.\s+Pays\s*:"
    end_marker = r"TYPE NR COLIS"
    
    start_matches = list(re.finditer(start_marker, extracted_text, re.IGNORECASE))
    end_match = re.search(end_marker, extracted_text, re.IGNORECASE)
    
    if start_matches and end_match:
        for i, start_match in enumerate(start_matches):
            start_pos = start_match.end()
            if i < len(start_matches) - 1:
                end_pos = start_matches[i + 1].start()
            else:
                end_pos = end_match.start()
            
            goods_text = extracted_text[start_pos:end_pos].strip()
            
            description_match = re.search(
                r"[A-Z]+\s*HS\s*:\s*([^\n]*)\n([\s\S]*?)(?=(?:\s*MARCHANDISE\s+N\.C\.\s+Pays\s*:|\s*VALEURS DECLAREES PAR L'EXPORTATEUR|$))",
                goods_text,
                re.IGNORECASE
            )
            if description_match:
                description = description_match.group(2)
                description = ' '.join(description.split()).strip()
                descriptions_list.append(description)
    
    data["Descriptions"] = descriptions_list if descriptions_list else ["No descriptions extracted"]

    return data

# --- Extraction function for AD Certificate ---
def extract_ad_certificate_data(extracted_text):
    patterns = {
        "Certificate_No": r"AD\s*N°\s*:?([0-9A-Z/ ]+)",
        "Importer": r"IMPORTATEUR\s*:?\s*([^\n]+?)(?=\s*BL#:|$)",
        "Transporteur": r"(?<!ID\s)Transporteur\s*:\s*(.+?)(?=\s+Fret\b|$)",
        "Carrier": r"Carrier:\s*([^\n]+)(?=\s+On\b|$)",
        "Forwarder": r"Transitaire:\s*([^\n]+)",
        "Entry_No": r"N°\s*Declaration\s*([\w\d]+(?:\s[\w\d]+)*)(?=\s*Agent)",
        "Discharge_Place": r"Lieu d'entrée en RDC:?\s*([A-Z]+)",
        "Final_Destination": r"Destination finale en\s*([A-Z][A-Za-z]*)\b",
        "Transport": r"ID Transporteur:?\s*([^\n]+)",
        "Descriptions": r"MARCHANDISE\s*:\s*([^\n]+)",
        "FOB_Value": r"Valeur FOB\s*:\s*([\d.,]+)",
        "Base_Freight": r"Valeur Fret\s*:\s*([\d.,]+)",
        "Insurance": r"Assurance\s*([\d.,]+)\s*USD"
    }

    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            try:
                data[key] = match.group(1).strip()
            except IndexError:
                data[key] = match.group(0).strip()
        else:
            data[key] = None

    # --- New Exporter field ---
    transporteur = data.get("Transporteur") or ""
    carrier = data.get("Carrier") or ""
    exporter = f"{transporteur} {carrier}".strip() if (transporteur or carrier) else None
    data["Exporter"] = exporter

    # Keep your custom extra fields
    data["transporterName"] = "OWN"
    data["validationNotes"] = "please verify"

    return data

# --- Main extraction function ---
def extract_certificate_data(pdf_file):
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    # Determine certificate type based on content
    if re.search(r"AD\s*N°", extracted_text, re.IGNORECASE):
        data = extract_ad_certificate_data(extracted_text)
        data["Certificate_Type"] = "AD"
    else:
        data = extract_normal_certificate_data(extracted_text)
        data["Certificate_Type"] = "Normal"

    # Map Discharge_Place to OUT-BOUND-Border
    discharge_place = data.get("Discharge_Place")
    data["Out_Bound_Border"] = BORDER_MAPPING.get(discharge_place, "UNKNOWN") if discharge_place else "UNKNOWN"

    return data