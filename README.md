# PDF → JSON → Excel/PDF Generator (Flask + xlwings)

A Flask web app that extracts structured data from shipping PDFs and fills Excel templates to produce ready-to-download Excel and PDF files.

Supported PDF types (tabs in the UI):
- Laban (Normal FERI)
- Malaba (Maritime)
- Possiano
- Busia

Excel templates are organized per type under `template/` and selected via a dropdown in the UI.

Note: Excel generation uses xlwings, which requires Microsoft Excel on Windows. You can still extract and view JSON on non‑Windows hosts, but Excel/PDF generation will not function there without replacing the Excel step with a headless alternative.

## Features
- Upload a PDF, auto-extract key fields with `pdfplumber`
- Choose an Excel template per PDF type and auto-populate via `xlwings`
- Generate both the filled Excel workbook and a PDF export
- Smart filename generation:
  - Maritime/Possiano/Busia: uses BL when available
  - Normal (Laban): uses Transport ID

## Project Structure
```
python-prototype-main/
  app/
    __init__.py              # Flask app factory
    routes.py                # Routes: index, process, downloads
    processing.py            # Template discovery + Excel/PDF processing
    data_extraction.py       # PDF text parsing and field extraction
    insertions_normal.py     # Excel population for Laban
    insertions_maritime.py   # Excel population for Malaba
    insertions_busia.py      # Excel population for Busia
    insertions_possiano.py   # Excel population for Possiano
  templates/
    upload_form.html         # Tailwind-powered UI with tabs
  template/
    laban/                   # .xlsx templates for Normal/Laban
    malaba/                  # .xlsx templates for Maritime/Malaba
    possiano/                # .xlsx templates for Possiano
    busia/                   # .xlsx templates for Busia
  app.py                     # Alt entry point (factory + PORT support)
  main.py                    # Local dev runner
  requirements.txt           # Python dependencies
  README.md
```

## Requirements
- Windows 10/11 with Microsoft Excel (for Excel/PDF generation)
- Python 3.8+

Non‑Windows (Linux/macOS): extraction works, but Excel/PDF generation requires changes (see Headless alternative below).

## Local Development (Windows)
1. Open PowerShell and navigate to the project root:
   ```bash
   cd "C:\Users\HomeLabs\Desktop\OGEFREM docs\python-prototype-main"
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app (choose one):
   - Dev server:
     ```bash
     python app.py
     ```
   - Gunicorn (WSGI) for a more production-like run on Windows:
     ```bash
     pip install gunicorn
     gunicorn --bind 0.0.0.0:8000 "app:create_app()"
     ```
4. Open `http://127.0.0.1:5000/` (or `http://127.0.0.1:8000/` if using Gunicorn).

## Using the App
1. Choose the correct tab (Laban/Maritime/Possiano/Busia)
2. Upload the source PDF
3. Select an Excel template from the dropdown for that tab
4. Optionally provide:
   - Freight number (all types)
   - Container type and number of containers (Maritime; UI includes these for certain other tabs as well)
5. Submit and wait for processing
6. If successful, you’ll see:
   - Extracted JSON data
   - Links to download the modified Excel and the generated PDF

## Deployment on Render (Linux)
Render runs on Linux. The project builds successfully, but Excel/PDF generation via Excel will not function on Linux—xlwings requires Excel on Windows. You have two options:

- Start the service for JSON extraction only (Excel actions will fail at runtime):
  - Set Render “Start Command” to:
    ```
    gunicorn --bind 0.0.0.0:$PORT "app:create_app()"
    ```
  - Ensure `pywin32` is Windows-only in `requirements.txt` (already handled):
    ```
    pywin32==311; sys_platform == "win32"
    ```

- Headless alternative (recommended for Linux):
  - Replace Excel automation with a headless flow:
    - Populate `.xlsx` using `openpyxl`
    - Convert `.xlsx` to PDF using LibreOffice in headless mode
  - This removes the Excel dependency and works on Linux containers.

## Deployment on Windows (IIS/Reverse Proxy)
1. Use a Windows host with Excel installed and a logged-in user session (Excel COM requires an interactive session).
2. Run with Gunicorn or Waitress behind IIS/Nginx as a reverse proxy:
   ```bash
   .\.venv\Scripts\Activate.ps1
   pip install waitress
   waitress-serve --listen=0.0.0.0:8000 --call "app:create_app"
   ```
3. Reverse proxy `http://127.0.0.1:8000/` to 80/443 and enable HTTPS.
4. For auto-start on login, use Windows Task Scheduler to run a small PowerShell script that activates the venv and starts the server.

## Key Modules and Behavior
- `app/data_extraction.py`: Uses `pdfplumber` + regex to parse text and extract fields like attestation number, importer, exporter, BL, CBM, weights, etc.
- `app/processing.py`: Discovers available templates, invokes Excel via `xlwings`, imports the right insertion module by `pdf_type`, and exports PDF.
- Insertions per type:
  - `insertions_normal.py` (Laban)
  - `insertions_maritime.py` (Malaba)
  - `insertions_busia.py` (Busia)
  - `insertions_possiano.py` (Possiano)

## Troubleshooting
- Build fails on Linux due to `pywin32`:
  - Ensure the requirement is platform-scoped: `pywin32==311; sys_platform == "win32"`
- Runtime fails on Render during Excel/PDF generation:
  - Expected on Linux; Excel is not available. Use a Windows host or the headless alternative.
- Excel stays open / hangs during repeated runs:
  - Use the utility `cleanup_excel_processes()` in `processing.py` (kills stray Excel processes) and ensure you keep a single interactive session.
- Template isn’t listed in the dropdown:
  - Confirm the file extension is `.xlsx` and it’s placed under the correct folder (`template/laban`, `template/malaba`, `template/possiano`, `template/busia`).

## License
Proprietary. All rights reserved.
