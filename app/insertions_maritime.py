def insert_data(ws, data, freight_number, container_type, num_containers, template_file=None):
    """
    Insert extracted data into the Excel worksheet for 'maritime' PDF type.
    """
    if 'feri_number' in data:
        ws.range('E6').value = f"FERI/AD: {data['feri_number']}"
        ws.range('B11').value = f"CERTIFICATE (FERI/ADR/AD) No : {data['feri_number']}"
        
    elif 'attestation_number' in data:
        ws.range('E6').value = f"FERI/AD: {data['attestation_number']}"
        ws.range('B11').value = f"CERTIFICATE (FERI/ADR/AD) No : {data['attestation_number']}"
    
    if 'transitaire' in data:
        ws.range('B8').value = f"DEBTOR: {data['transitaire']}"
    
    if 'importateur' in data:
        ws.range('B10').value = f"IMPORTER: {data['importateur']}"
    
    if 'bl' in data:
        ws.range('B14').value = data['bl']
    
    # Handle CBM based on template and container type
    specific_templates = ['Proforma_Invoice malaba cement 0.5.xlsx', 
                          'Proforma_Invoice malaba.xlsx',
                          'Proforma_roro.xlsx']
    if template_file in specific_templates and 'cbm' in data:
        cbm_value = float(data['cbm'])  # already a float from extraction
        ws.range('D14').value = cbm_value
    else:
        if container_type == '40FT':
            ws.range('D14').value = 110
            ws.range('E14').value = num_containers
            ws.range('D17').value = num_containers
            # Handle freight number (overrides default calculation if provided)
            if freight_number is not None:
                ws.range('D18').value = freight_number
            else:
                ws.range('D18').value = num_containers * 250
        elif container_type == '20FT':
            ws.range('D14').value = 60
            ws.range('E14').value = num_containers
            ws.range('D17').value = num_containers
            # Handle freight number (overrides default calculation if provided)
            if freight_number is not None:
                ws.range('D18').value = freight_number
            else:
                ws.range('D18').value = num_containers * 250
        
        
        # # Insert number of containers for non-specific templates