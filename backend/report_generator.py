from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_report(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    content = []

    content.append(Paragraph("<b>File Analysis Report</b>"))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>File Name:</b> {data['name']}"))
    content.append(Paragraph(f"<b>Result:</b> {data['result']}"))
    content.append(Paragraph(f"<b>Hash:</b> {data['hash']}"))
    content.append(Paragraph(f"<b>MIME Type:</b> {data['mime']}"))
    content.append(Paragraph(f"<b>Score:</b> {data['score']}%"))

    content.append(Spacer(1, 10))

    # 🔥 METADATA SECTION
    content.append(Paragraph("<b>Metadata (Original Content):</b>"))
    for key, value in data["metadata"].items():
        content.append(Paragraph(f"{key}: {value}"))

    content.append(Spacer(1, 10))

    # 🔥 HIDDEN CONTENT
    content.append(Paragraph("<b>Hidden Content Detection:</b>"))
    content.append(Paragraph(data["hidden"]))

    content.append(Spacer(1, 10))

    # 🔥 REASONS
    content.append(Paragraph("<b>Reasons:</b>"))
    for r in data["reasons"]:
        content.append(Paragraph(f"- {r}"))

    doc.build(content)

    return filename