---
name: doc-generation
version: 1.0.0
description: |
  Generate native PowerPoint presentation slides (.pptx) and PDF documents (.pdf)
  using python-pptx, reportlab, or fpdf2.
license: MIT
compatibility: any-agent
allowed-tools:
  - Read
  - Write
  - command
---

# Native PDF & PPTX Generation Skill

Use this skill when you need to generate native PowerPoint slides (`.pptx`) or PDF documents (`.pdf`) from raw structured data or markdown text.

## 1. PowerPoint Presentation (.pptx) Generation

We use the `python-pptx` library to create native slides that can be opened and edited in MS PowerPoint, Apple Keynote, or Google Slides.

### Installation
```bash
pip install python-pptx
```

### Python Template for PPTX
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_presentation(filename="presentation.pptx"):
    prs = Presentation()
    
    # Slide 1: Title Slide
    slide_layout = prs.slide_layouts[0] # Title Layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Strategic Plan 2026"
    subtitle.text = "Prepared by Antigravity AI"
    
    # Slide 2: Bullet Points
    slide_layout = prs.slide_layouts[1] # Bullet Points Layout
    slide = prs.slides.add_slide(slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    
    title_shape.text = "Key Objectives"
    tf = body_shape.text_frame
    tf.text = "Maximize productivity"
    
    p = tf.add_paragraph()
    p.text = "Automate documentation workflows"
    p.level = 1
    
    prs.save(filename)
```

## 2. PDF Document Generation

We use the `fpdf2` library to compile formatted reports, invoices, or guides into clean PDF files.

### Installation
```bash
pip install fpdf2
```

### Python Template for PDF
```python
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Antigravity Workspace Report', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_pdf(filename="report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 10, 'This report was generated automatically.', new_x="LMARGIN", new_y="NEXT")
    pdf.output(filename)
```
