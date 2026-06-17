from fpdf import FPDF
from datetime import datetime
import os

def generate_compliance_report(data: dict, output_path: str = "outputs/compliance_report.pdf"):
    os.makedirs("outputs", exist_ok=True)
    
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_fill_color(30, 60, 114)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "ReguTrack Compliance Report", fill=True, ln=True, align="C")
    
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    
    # Regulation Info
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Regulation Details", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"ID: {data.get('regulation_id', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Source: {data.get('source', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Title: {data.get('title', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Date: {data.get('published_date', datetime.now().strftime('%Y-%m-%d'))}", ln=True)
    
    pdf.ln(3)

    # Risk Level
    risk = data.get("risk_level", "MEDIUM")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, f"Risk Level: {risk}", ln=True)
    
    pdf.ln(3)

    # Impact Summary
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Impact Summary", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, data.get("impact_summary", "Analysis pending."))
    
    pdf.ln(3)

    # Policy Changes
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Proposed Policy Changes", ln=True)
    pdf.set_font("Helvetica", size=11)
    for change in data.get("policy_changes", ["No changes proposed yet."]):
        pdf.multi_cell(0, 8, f"• {change}")
    
    pdf.ln(3)

    # Audit Trail
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Audit Trail", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 8, f"Decision: {data.get('decision', 'PENDING')}", ln=True)
    pdf.cell(0, 8, f"Audit Hash: {data.get('audit_hash', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 8, "System: ReguTrack Multi-Agent Compliance System", ln=True)
    
    pdf.output(output_path)
    return output_path