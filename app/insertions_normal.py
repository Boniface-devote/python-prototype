def insert_data(ws, data, freight_number, container_type='', num_containers=1):
    """
    Insert extracted data into the Excel worksheet for 'normal' PDF type.
    """
    if 'attestation_number' in data:
        ws.range('E6').value = f"FERI/AD: {data['attestation_number']}"
        ws.range('B11').value = f"CERTIFICATE (FERI/ADR/AD) No : {data['attestation_number']}"
    
    if 'forwarding_agent' in data:
        ws.range('B8').value = f"DEBTOR: {data['forwarding_agent']}"
    
    if 'importateur' in data:
        ws.range('B10').value = f"IMPORTER: {data['importateur']}"
    
    if 'transport_id' in data:
        ws.range('B14').value = data['transport_id']
    
    if 'cbm' in data:
        cbm_value = float(data['cbm'].replace(' CBM', ''))
        ws.range('D14').value = cbm_value
    
    if freight_number is not None:
        ws.range('D18').value = freight_number