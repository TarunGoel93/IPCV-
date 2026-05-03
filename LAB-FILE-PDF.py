from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import json

# ==============================
# PATH
# ==============================
base_path = r"D:\IPCV"
pdf_path = os.path.join(base_path, "IPCV_Lab_File_Professional.pdf")

doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        rightMargin=40, leftMargin=40,
                        topMargin=50, bottomMargin=40)

styles = getSampleStyleSheet()

# ==============================
# STYLES
# ==============================
title_style = ParagraphStyle(
    'TitleStyle', parent=styles['Title'],
    fontSize=18, spaceAfter=12
)

heading_style = ParagraphStyle(
    'HeadingStyle', parent=styles['Heading2'],
    textColor=colors.darkblue, spaceAfter=6
)

body_style = ParagraphStyle(
    'BodyStyle', parent=styles['Normal'],
    fontSize=11, spaceAfter=6
)

code_style = ParagraphStyle(
    'CodeStyle', parent=styles['Normal'],
    fontName='Courier', fontSize=8,
    backColor=colors.whitesmoke,
    borderPadding=5
)

content = []

# ==============================
# COVER PAGE
# ==============================
content.append(Spacer(1, 2*inch))
content.append(Paragraph("DIGITAL IMAGE PROCESSING LAB", styles['Title']))
content.append(Spacer(1, 20))
content.append(Paragraph("IPCV Lab File", styles['Heading2']))
content.append(Spacer(1, 40))
content.append(Paragraph("Name: ____________", body_style))
content.append(Paragraph("Roll No: ____________", body_style))
content.append(Paragraph("Course: ____________", body_style))
content.append(Spacer(1, 100))
content.append(Paragraph("Submitted To: ____________", body_style))
content.append(PageBreak())

# ==============================
# READ NOTEBOOK
# ==============================
def extract_code(ipynb_path):
    code = ""
    try:
        with open(ipynb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                code += "".join(cell["source"]) + "\n\n"
    except:
        code = "Error reading notebook"
    return code

# ==============================
# ADD NORMAL IMAGES
# ==============================
def add_images(folder):
    imgs = []
    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder, file)
            try:
                img = Image(path, width=2.5*inch, height=2.5*inch)
                imgs.append(img)
            except:
                pass

    rows = [imgs[i:i+2] for i in range(0, len(imgs), 2)]

    for row in rows:
        table = Table([row])
        table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER')
        ]))
        content.append(table)
        content.append(Spacer(1, 10))

# ==============================
# ADD DATASET IMAGES (EXP 16)
# ==============================
def add_dataset_images(dataset_path):
    if not os.path.exists(dataset_path):
        return

    for person in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person)

        if not os.path.isdir(person_path):
            continue

        # Person name
        content.append(Paragraph(f"<b>{person}</b>", body_style))

        imgs = []

        for file in os.listdir(person_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(person_path, file)
                try:
                    img = Image(path, width=2.2*inch, height=2.2*inch)
                    imgs.append(img)
                except:
                    pass

        rows = [imgs[i:i+3] for i in range(0, len(imgs), 3)]

        for row in rows:
            table = Table([row])
            table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER')
            ]))
            content.append(table)
            content.append(Spacer(1, 8))

# ==============================
# GET EXPERIMENT FOLDERS
# ==============================
folders = sorted([
    f for f in os.listdir(base_path)
    if f.startswith("LAB-EXP-")
], key=lambda x: int(x.split('-')[-1]))

# ==============================
# BUILD CONTENT
# ==============================
for folder in folders:

    exp_path = os.path.join(base_path, folder)

    if not os.path.exists(exp_path):
        continue

    images_path = os.path.join(exp_path, "images")
    result_path = os.path.join(exp_path, "resultant_img")
    dataset_path = os.path.join(exp_path, "dataset")

    # Find notebook
    ipynb_file = None
    for f in os.listdir(exp_path):
        if f.endswith(".ipynb"):
            ipynb_file = os.path.join(exp_path, f)
            break

    # Title
    content.append(Paragraph(folder.replace('-', ' '), title_style))

    # Sections
    content.append(Paragraph("<b>Aim:</b> To implement the given image processing technique.", body_style))
    content.append(Paragraph("<b>Theory:</b> This experiment demonstrates the working of image processing concepts.", body_style))
    content.append(Paragraph("<b>Algorithm:</b> 1. Load image 2. Process 3. Output result", body_style))

    content.append(Spacer(1, 10))

    # Code
    content.append(Paragraph("Code:", heading_style))

    if ipynb_file:
        code_text = extract_code(ipynb_file)
        content.append(Preformatted(code_text, code_style))
    else:
        content.append(Paragraph("No code found.", body_style))

    content.append(Spacer(1, 10))

    # ==============================
    # EXPERIMENT 16 SPECIAL
    # ==============================
    if folder.endswith("16") and os.path.exists(dataset_path):
        content.append(Paragraph("Dataset Images:", heading_style))
        add_dataset_images(dataset_path)

    # ==============================
    # INPUT / OUTPUT IMAGES
    # ==============================
    content.append(Paragraph("Input Images:", heading_style))
    add_images(images_path)

    content.append(Paragraph("Output Images:", heading_style))
    add_images(result_path)

    # Result
    content.append(Paragraph("<b>Result:</b> The experiment was successfully executed.", body_style))

    content.append(PageBreak())

# ==============================
# BUILD PDF
# ==============================
doc.build(content)

print("✅ Professional Lab PDF Created!")
print("📄 Saved at:", pdf_path)