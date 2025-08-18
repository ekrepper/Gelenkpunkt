import streamlit as st
import pydicom as pm
import io, zipfile

st.title("DICOM Anonymizer")

uploaded_files = st.file_uploader(
    "Ziehe DICOM-Dateien hierher", 
    accept_multiple_files=True, 
    type=["dcm"]
)

if uploaded_files:
    seen_files = set()  # merkt sich Dateinamen
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for uploaded_file in uploaded_files:
            if uploaded_file.name in seen_files:
                st.warning(f"⚠️ {uploaded_file.name} wurde mehrfach hochgeladen – nur einmal verarbeitet.")
                continue
            seen_files.add(uploaded_file.name)

            dicom_file = pm.dcmread(uploaded_file)

            print(dicom_file.PatientName)  # Debug-Ausgabe
            print(dicom_file.PatientBirthDate)

            # Anonymisieren
            dicom_file.PatientName = "Anonymized"
            #dicom_file.PatientBirthDate = "19000101"

            print(dicom_file.PatientName)  # Debug-Ausgabe
            print(dicom_file.PatientBirthDate)

            # Datei in Memory schreiben
            dcm_buffer = io.BytesIO()
            dicom_file.save_as(dcm_buffer)
            dcm_buffer.seek(0)

            # neuen Namen bestimmen
            new_filename = uploaded_file.name.replace(".dcm", "_anonym.dcm")

            # in ZIP packen
            zipf.writestr(new_filename, dcm_buffer.getvalue())

            # Einzel-Download-Button anzeigen
            st.download_button(
                label=f"⬇️ {new_filename}",
                data=dcm_buffer.getvalue(),
                file_name=new_filename,
                mime="application/dicom"
            )

    zip_buffer.seek(0)
    st.download_button(
        label="⬇️ Alle anonymisierten Dateien herunterladen (ZIP)",
        data=zip_buffer,
        file_name="dicoms_anonymized.zip",
        mime="application/zip"
    )
