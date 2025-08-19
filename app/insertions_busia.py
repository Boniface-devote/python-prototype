def insert_data(ws, data, freight_number, container_type, num_containers, template_file=None):
    """
    Insert extracted data into the Excel worksheet for 'busia' PDF type.
    Mirrors maritime logic but uses different defaults where needed.
    """
    if 'feri_number' in data:
        ws.range('E6').value = f"FERI/AD: {data['feri_number']}"
        ws.range('B11').value = f"CERTIFICATE (FERI/ADR/AD) No : {data['feri_number']}"
    elif 'attestation_number' in data:
        ws.range('E6').value = f"FERI/AD: {data['attestation_number']}"
        ws.range('B11').value = f"CERTIFICATE (FERI/ADR/AD) No : {data['attestation_number']}"

    # Some Busia PDFs might use forwarding agent field naming similar to maritime
    forwarding_key = 'transitaire' if 'transitaire' in data else ('forwarding_agent' if 'forwarding_agent' in data else None)
    if forwarding_key:
        ws.range('B8').value = f"DEBTOR: {data[forwarding_key]}"

    if 'importateur' in data:
        ws.range('B10').value = f"IMPORTER: {data['importateur']}"

    if 'bl' in data:
        ws.range('B14').value = data['bl']

    # Handle CBM based on container type (Busia follows maritime default behavior)
    if container_type == '40FT':
        ws.range('D14').value = 110
        ws.range('E14').value = num_containers
        ws.range('D17').value = num_containers
    elif container_type == '20FT':
        ws.range('D14').value = 60
        ws.range('E14').value = num_containers
        ws.range('D17').value = num_containers
    elif 'cbm' in data:
        try:
            cbm_value = float(str(data['cbm']).replace(' CBM', ''))
            ws.range('D14').value = cbm_value
        except Exception:
            pass

    # Freight number; default multiplier for Busia is 200 per container
    if freight_number is not None:
        ws.range('D18').value = freight_number
    else:
        ws.range('D18').value = num_containers * 200


