from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def create_pdf(text, filename):

    doc = SimpleDocTemplate(filename)

    story = []

    sections = text.split("\n")

    for line in sections:

        if line.strip()=="":
            story.append(Spacer(1,10))

        elif ":" in line and len(line)<60:

            story.append(Paragraph(f"<b>{line}</b>", styles['Heading3']))
            story.append(Spacer(1,10))

        else:

            story.append(Paragraph(line, styles['BodyText']))
            story.append(Spacer(1,10))

    doc.build(story)