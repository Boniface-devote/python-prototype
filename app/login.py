from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import json
import sys
import os

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the Edge WebDriver 
driver_path = os.path.join("..", "python-prototype", "msedgedriver.exe")

# URL and credentials
login_url = "https://www.invesco-ug.com/auth/login"
target_url = "https://www.invesco-ug.com/business/application/new"
email_address = "blaise@goldencourtsafrica.com"
password = "NEW@2025"

# Read extracted data from stdin
try:
    form_data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    logging.error("Invalid JSON data provided")
    sys.exit(1)

# Set up the Edge WebDriver
service = Service(driver_path)
driver = webdriver.Edge(service=service)

try:
    # Open the login page
    logging.info("Opening login page")
    driver.get(login_url)

    # Wait for email and enter it
    logging.info("Entering email")
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "emailAddress"))
    )
    email_field.send_keys(email_address)

    # Wait for password and enter it
    logging.info("Entering password")
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys(password)

    # Click login button
    logging.info("Clicking login button")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
    )
    login_button.click()

    WebDriverWait(driver, 30).until(
        EC.url_changes(login_url)
    )

    driver.get(target_url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='certificateNumber']//input"))
    )

    # Fill the form
    # Handle dropdowns
    issuing_body_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Issuing Body']//button[@ngbdropdowntoggle]"))
    )
    issuing_body_dropdown.click()
    issuing_body_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@ngbdropdownitem and text()='DR CONGO']"))
    )
    issuing_body_option.click()

    # Select Cert. Type based on Certificate_Type
    cert_type_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Cert. Type']//button[@ngbdropdowntoggle]"))
    )
    cert_type_dropdown.click()
    cert_type_value = "CONTINUANCE" if form_data.get("Certificate_Type") == "AD" else "REGIONAL"
    cert_type_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[@ngbdropdownitem and text()='{cert_type_value}']"))
    )
    cert_type_option.click()

    cargo_origin_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Cargo Origin']//button[@ngbdropdowntoggle]"))
    )
    cargo_origin_dropdown.click()
    cargo_origin_value = "OUTSIDE UGANDA" if form_data.get("Certificate_Type") == "AD" else "UGANDA"
    cargo_origin_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[@ngbdropdownitem and text()='{cargo_origin_value}']"))
    )
    cargo_origin_option.click()

    shipment_route_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Shipment Route']//button[@ngbdropdowntoggle]"))
    )
    shipment_route_dropdown.click()
    shipment_route_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@ngbdropdownitem and text()='OUT-BOUND']"))
    )
    shipment_route_option.click()

    transport_mode_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Transport Mode']//button[@ngbdropdowntoggle]"))
    )
    transport_mode_dropdown.click()
    transport_mode_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@ngbdropdownitem and text()='ROAD']"))
    )
    transport_mode_option.click()

    fob_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='FOB Currency']//button[@ngbdropdowntoggle]"))
    )
    fob_dropdown.click()
    fob_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@ngbdropdownitem and text()='USD']"))
    )
    fob_option.click()

    # Fill OUT-BOUND-Border dropdown
    out_bound_border_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@ngbdropdown and contains(@class, 'dropdown')]//button[@ngbdropdowntoggle and contains(text(), 'Select Border Point')]"))
    )
    out_bound_border_dropdown.click()
    out_bound_border_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[@ngbdropdownitem and text()='{form_data.get('Out_Bound_Border', 'UNKNOWN')}']"))
    )
    out_bound_border_option.click()

    # Fill text inputs using extracted data
    certificate_number_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='certificateNumber']//input[@id='certificateNumber']"))
    )
    certificate_number_field.clear()
    certificate_number_field.send_keys(form_data.get("Certificate_No", ""))

    Entry_No_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='customsDeclarationNumber']//input[@id='customsDeclarationNumber']"))
    )
    Entry_No_field.clear()
    Entry_No_field.send_keys(form_data.get("Entry_No", ""))

    importer_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='importerName']//input[@id='importerName']"))
    )
    importer_name_field.clear()
    importer_name_field.send_keys(form_data.get("Importer", ""))

    exporter_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='exporterName']//input[@id='exporterName']"))
    )
    exporter_name_field.clear()
    exporter_name_field.send_keys(form_data.get("Exporter", ""))

    Forwarder_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='importAgentName']//input[@id='importAgentName']"))
    )
    Forwarder_name_field.clear()
    Forwarder_name_field.send_keys(form_data.get("Forwarder", ""))

    Forwarder_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='exportAgentName']//input[@id='exportAgentName']"))
    )
    Forwarder_name_field.clear()
    Forwarder_name_field.send_keys(form_data.get("Forwarder", ""))

    transporterName_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='transporterName']//input[@id='transporterName']"))
    )
    transporterName_field.clear()
    transporterName_field.send_keys(form_data.get("transporterName", ""))

    Transport_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='vehicleNumber']//input[@id='vehicleNumber']"))
    )
    Transport_field.clear()
    Transport_field.send_keys(form_data.get("Transport", ""))

    Discharge_Place_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='dischargeLocation']//input[@id='dischargeLocation']"))
    )
    Discharge_Place_field.clear()
    Discharge_Place_field.send_keys(form_data.get("Discharge_Place", ""))

    Final_Destination_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='finalDestination']//input[@id='finalDestination']"))
    )
    Final_Destination_field.clear()
    Final_Destination_field.send_keys(form_data.get("Final_Destination", ""))

    FOB_Value_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='fobValue']//input[@id='fobValue']"))
    )
    FOB_Value_field.clear()
    FOB_Value_field.send_keys(form_data.get("FOB_Value", ""))

    Base_Freight_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-input[@id='freightValue']//input[@id='freightValue']"))
    )
    Base_Freight_field.clear()
    Base_Freight_field.send_keys(form_data.get("Base_Freight", ""))

    # Fill validationNotes field
    validation_notes_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//app-my-text-area[@id='validationNotes']//textarea[@id='validationNotes']"))
    )
    validation_notes_field.clear()
    validation_notes_field.send_keys(form_data.get("validationNotes", ""))

    if form_data.get("Certificate_Type") == "AD":
      # Fill cargoDescription field properly
        cargo_description_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//app-my-text-area[@id='cargoDescription']//textarea[@id='cargoDescription']")
            )
        )
        cargo_description_field.clear()
        descriptions = form_data.get("Descriptions", [])
        if descriptions:
            numbers_part = "".join(str(item) for item in descriptions if str(item).isdigit())
            text_part = " ".join(str(item) for item in descriptions if not str(item).isdigit())
            
            full_text = numbers_part
            if text_part:
                full_text += ": " + text_part  # adds colon and text

            cargo_description_field.send_keys(full_text)

    else:
        # Fill cargoDescription field (joining Descriptions list into a single string)
        cargo_description_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//app-my-text-area[@id='cargoDescription']//textarea[@id='cargoDescription']"))
        )
        cargo_description_field.clear()
        descriptions = form_data.get("Descriptions", [])
        cargo_description_field.send_keys("\n".join(descriptions) if descriptions else "")

    # Fill freight currency
    freight_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Freight Currency']//button[@ngbdropdowntoggle]"))
    )
    freight_dropdown.click()
    freight_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//app-my-input-dropdown[@label='Freight Currency']//button[@ngbdropdownitem and text()='USD']"))
    )
    freight_option.click()

    logging.info("Form filled successfully")

    # Keep browser open for inspection
    time.sleep(180)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
    driver.save_screenshot("error_screenshot.png")
    logging.info("Screenshot saved as error_screenshot.png")

finally:
    logging.info("Closing browser")
    driver.quit()