import streamlit as st
import pydicom as pm
import io, zipfile, re  # re neu für kleine ID-Validierung

st.image("MCIxGelenkpunkt.png")
st.title("DICOM-File Anonymizer")

# ✨ Neu: manuelle Patienten-ID
patient_id_input = st.text_input(
    "Patienten-ID (wird als Ordnername im ZIP verwendet)",
    placeholder="z. B. 12345",
    help="Erlaubt sind Ziffern - die ID soll mit der PatientenID in der Tenodese-Tabelle übereinstimmen."
)

def sanitize_id(pid: str) -> str:
    pid = pid.strip().replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9\-_]", "_", pid)

uploaded_files = st.file_uploader(
    "Ziehe DICOM-Dateien hierher", 
    accept_multiple_files=True, 
    type=["dcm"]
)

if uploaded_files:
    # ID prüfen, bevor Dateien verarbeitet werden
    if not patient_id_input:
        st.warning("Bitte zuerst eine Patienten-ID eingeben.")
        st.stop()
    patient_id = sanitize_id(patient_id_input)
    if not patient_id:
        st.error("Ungültige Patienten-ID.")
        st.stop()

    seen_files = set()  # merkt sich Dateinamen
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for uploaded_file in uploaded_files:
            if uploaded_file.name in seen_files:
                st.warning(f"⚠️ {uploaded_file.name} wurde mehrfach hochgeladen – nur einmal verarbeitet.")
                continue
            seen_files.add(uploaded_file.name)

            dicom_file = pm.dcmread(uploaded_file)

            print(dicom_file.PatientName)       # Debug-Ausgabe
            print(dicom_file.PatientBirthDate)
            print(dicom_file.PatientID)         # Debug-Ausgabe

            # Anonymisieren
            dicom_file.PatientName = "Anonymized"
            # dicom_file.PatientBirthDate = "19000101"
            # ❌ dicom_file.PatientID = patient_id   # nicht mehr überschreiben!

            print(dicom_file.PatientName)       # Debug-Ausgabe
            print(dicom_file.PatientBirthDate)
            print(dicom_file.PatientID)         # Debug-Ausgabe

            # Datei in Memory schreiben
            dcm_buffer = io.BytesIO()
            dicom_file.save_as(dcm_buffer)
            dcm_buffer.seek(0)

            # neuen Namen bestimmen
            new_filename = uploaded_file.name.replace(".dcm", "_anonym.dcm")

            # ✨ in Unterordner <ID>/... ins ZIP packen
            zip_path = f"{patient_id}/{new_filename}"
            zipf.writestr(zip_path, dcm_buffer.getvalue())

            # Einzel-Download-Button anzeigen (unverändert: nur die Datei)
            st.download_button(
                label=f"⬇️ {new_filename}",
                data=dcm_buffer.getvalue(),
                file_name=new_filename,
                mime="application/dicom",
                key=f"dl_{uploaded_file.name}"
            )

    zip_buffer.seek(0)
    st.download_button(
        label=f"⬇️ Alle anonymisierten Dateien herunterladen (ZIP) – {patient_id}",
        data=zip_buffer,
        file_name=f"{patient_id}.zip",   # ZIP heißt wie die ID
        mime="application/zip",
        key="dl_zip_all"
    )
