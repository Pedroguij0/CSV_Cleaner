from cleaner.quality.auditor import Anomaly
from pathlib import Path
from typing import List, Dict
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
class ReportGenerator:
    @staticmethod
    def generate_markdow(
        output_path: Path,
        initial_count: int,
        final_count: int,
        duplicates_removed: int,
        anomalies: List[Anomaly]
    ) -> None:
        lines =[
            f"{'#'*10}Data Quality Report{'#'*10}\n",
            f"{'#'*5} 1. Counts Metrics {'#'*5}",
            f"- **Inicial Rows: {initial_count} **",
            f"- **Duplicates Removed: {duplicates_removed} **",
            f"- **Final Rows: {final_count} **",
            f"- **Encountered Anomalies: {len(anomalies)}\n",
            f"{'#'*5}2. Cleaning Actions Performed{'#'*5}\n",
            f"- String treatments with spaces remotions and title case standardization.",
            f"- Cleaning and Conversion of monetary values to float type.",
            f"- Dates transformation to international norm (YYYY-MM-DD)",
            f"- Missings filled with defaults values (discount: '0.0', Newsletter: 'False')",
            f"- Placeholders entering on critial texts with 'NOT INFORMED' mark.\n",
            f"{'#'*5}3. Critial Anomalies Table {'#'*5}",
            "| Record ID | Anomaly Type | Details | Raw Value | Warning Message | Data Frame Column |",
            "| :-------- | :----------- | :------ | :-------- | :-------------- | :---------------- |"
        ]
        for item in anomalies:
            rec_id = f"`{item.record_id}`"
            lines.append(
            f"| {rec_id:<9} | {item.anomaly_type:<16} | {item.details:<30} | {str(item.raw_value):<12} | {item.column:<12} | {item.message:<58} |"
        )
        output_path.write_text("\n".join(lines), encoding="utf-8")
    @staticmethod
    def generate_pdf(
        output_path: Path,
        initial_count: int,
        final_count: int,
        duplicates_removed: int,
        anomalies: List[Anomaly]
    ) -> None:
        doc = SimpleDocTemplate(str(output_path),
        pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        styles = getSampleStyleSheet()
        story=[]
        story.append(Paragraph("<b>Data Quality and Cleansing Report:</b>", styles["Title"]))
        story.append(Spacer(1,10))
        summary = f"<b>Initial Rows:</b> {initial_count} | <b>Duplicates Removed:</b> {duplicates_removed} | <b>Final Clean Rows:</b> {final_count} | <b>Anomalies:</b> {len(anomalies)}"
        story.append(Paragraph(summary, styles["Normal"]))
        story.append(Spacer(1,15))
        story.append(Paragraph("<b>Critical Anomalies Table:</b>",styles["Heading2"]))
        story.append(Spacer(1, 8))
        table_data = [["Record ID", "Anomaly Type", "Details", "Raw Value", "Column", "Warning Message"]]
        for a in anomalies:
            table_data.append([
                Paragraph(str(a.record_id), styles["Normal"]),
                Paragraph(str(a.anomaly_type), styles["Normal"]),
                Paragraph(str(a.details), styles["Normal"]),
                Paragraph(str(a.raw_value), styles["Normal"]),
                Paragraph(str(a.column), styles["Normal"]),
                Paragraph(str(a.message), styles["Normal"])
            ])
        tabela = Table(table_data, colWidths=[70, 95, 150, 75, 75, 250])
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),  # Cabeçalho escuro profissional
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),   # Bordas suaves
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]) # Linhas zebradas
        ]))
        story.append(tabela)
        doc.build(story)
