# DICOM Anonymizer (Streamlit App)

A simple Streamlit application to **anonymize DICOM files** via drag & drop.  
The patient's name is removed, and the anonymized files can be downloaded either individually or as a single ZIP archive.

---

## Features
- Drag & drop DICOM (`.dcm`) file upload
- Automatic anonymization (removes `PatientName` )
- Download anonymized files:
  - Individually (`*_anonym.dcm`)
  - All files bundled as a `.zip`

---

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dicom-anonymizer.git
   cd dicom-anonymizer

