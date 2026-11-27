# GuardianNodes RoadSoS — Documentation

This directory contains project documentation, presentation generation scripts, and standalone report templates.

## Files

- **`Project_Documentation.html`**: Complete standalone HTML report with responsive styling and print CSS.
- **`create_pdf.py`**: Automated script using `fpdf2` to generate `RoadSoS_Project_Document.pdf`.
- **`create_ppt.py`**: Automated script using `python-pptx` to generate `Project_Presentation.pptx`.

## Generating Documents

Make sure requirements are installed:
```bash
pip install fpdf2 python-pptx
```

Generate PDF document:
```bash
python docs/create_pdf.py
```

Generate PowerPoint slides:
```bash
python docs/create_ppt.py
```
