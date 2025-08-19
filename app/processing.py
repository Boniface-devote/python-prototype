import xlwings as xw
from io import BytesIO
import os
import glob
import json
import tempfile
import shutil

# Directory containing Excel templates
laban_dir = 'template/laban'  # Directory for Normal FERI templates
malaba_dir = 'template/malaba'  # Directory for Maritime templates

# Global variables to store the modified files and data in memory
modified_excel_global = None
modified_pdf_global = None
data_global = None
pdf_type_global = None

def get_available_templates(template_dir):
    """Get list of available Excel templates from the specified directory"""
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        return []
    
    excel_files = glob.glob(os.path.join(template_dir, '*.xlsx'))
    return [os.path.basename(f) for f in excel_files]

def process_excel_and_pdf(data, pdf_type, template_file, freight_number, container_type='', num_containers=1):
    """
    Process extracted data, update Excel template, and generate PDF using xlwings.
    Returns modified Excel, PDF buffers, and formatted JSON data.
    """
    global modified_excel_global, modified_pdf_global, data_global, pdf_type_global
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    modified_excel = None
    modified_pdf = None

    # Store data and pdf_type globally
    data_global = data
    pdf_type_global = pdf_type

    # Check for selected template
    template_path = None
    if template_file:
        template_path = os.path.join(laban_dir if pdf_type == 'normal' else malaba_dir, template_file)
        if not os.path.exists(template_path):
            template_path = None

    if template_path:
        # Create temporary files for processing
        temp_dir = tempfile.mkdtemp()
        temp_excel_path = os.path.join(temp_dir, f"temp_{template_file}")
        temp_pdf_path = os.path.join(temp_dir, "temp_output.pdf")
        
        try:
            # Copy template to temporary location
            shutil.copy2(template_path, temp_excel_path)
            
            # Open Excel application with xlwings
            app = xw.App(visible=False, add_book=False)
            
            try:
                # Open the workbook
                wb = app.books.open(temp_excel_path)
                ws = wb.sheets[0]  # Get the active sheet
                
                # Insert data into specific cells
                if pdf_type == 'normal':
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

                else:  # maritime
                    if 'feri_number' in data:
                        ws.range('E6').value = f"FERI/AD: {data['feri_number']}"
                        ws.range('B11').value = f"CERTIFICATE (FERI/ADR/AD) No : {data['feri_number']}"
                    if 'transitaire' in data:
                        ws.range('B8').value = f"DEBTOR: {data['transitaire']}"
                    if 'importateur' in data:
                        ws.range('B10').value = f"IMPORTER: {data['importateur']}"
                    if 'bl' in data:
                        ws.range('B14').value = data['bl']
                    if 'cbm' in data and container_type not in ['40FT', '20FT']:
                        cbm_value = float(data['cbm'].replace(' CBM', ''))
                        ws.range('D14').value = cbm_value
                    if container_type == '40FT':
                        ws.range('D14').value = 110
                    elif container_type == '20FT':
                        ws.range('D14').value = 60
                    ws.range('E14').value = num_containers
                    ws.range('D17').value = num_containers
                    ws.range('D18').value = num_containers * 250
                    if freight_number is not None:
                        ws.range('D18').value = freight_number

                # Force calculation of all formulas
                wb.app.calculate()
                
                # Save the Excel file
                wb.save()
                
                # Export to PDF with exact formatting
                wb.api.ExportAsFixedFormat(Type=0, Filename=temp_pdf_path)
                
                # Read the modified Excel file into memory
                with open(temp_excel_path, 'rb') as f:
                    modified_excel = BytesIO(f.read())
                
                # Read the PDF file into memory
                with open(temp_pdf_path, 'rb') as f:
                    modified_pdf = BytesIO(f.read())
                
                # Store in globals
                modified_excel_global = modified_excel
                modified_pdf_global = modified_pdf
                
            finally:
                # Close workbook and quit Excel application
                wb.close()
                app.quit()
                
        except Exception as e:
            print(f"Error processing Excel/PDF: {str(e)}")
            # Cleanup in case of error
            try:
                if 'app' in locals():
                    app.quit()
            except:
                pass
            
        finally:
            # Clean up temporary files
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

    return modified_excel, modified_pdf, json_data

def cleanup_excel_processes():
    """
    Utility function to cleanup any remaining Excel processes
    Call this if you encounter issues with Excel not closing properly
    """
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and 'excel' in proc.info['name'].lower():
                proc.kill()
    except ImportError:
        print("psutil not available for process cleanup")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")