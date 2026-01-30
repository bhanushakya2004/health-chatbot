from agno.tools import tool
from app.config.database import get_patients_collection, get_reports_collection

@tool
def get_patient_info(patient_id: str) -> str:
    """Fetch patient information from MongoDB by patient ID."""
    patients_collection = get_patients_collection()
    patient = patients_collection.find_one({"patient_id": patient_id})
    if patient:
        patient.pop('_id', None)  # Remove MongoDB _id field
        return str(patient)
    return "Patient not found"

@tool
def get_patient_reports(patient_id: str) -> str:
    """Fetch all medical reports for a patient from MongoDB."""
    reports_collection = get_reports_collection()
    reports = list(reports_collection.find({"patient_id": patient_id}))
    if reports:
        for report in reports:
            report.pop('_id', None)
        return str(reports)
    return "No reports found for this patient"

@tool
def get_latest_report(patient_id: str) -> str:
    """Fetch the most recent medical report for a patient."""
    reports_collection = get_reports_collection()
    report = reports_collection.find_one(
        {"patient_id": patient_id},
        sort=[("date", -1)]
    )
    if report:
        report.pop('_id', None)
        return str(report)
    return "No reports found"
