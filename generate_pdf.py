from fpdf import FPDF
import re

INPUT = "informe_revision.md"
OUTPUT = "informe_revision.pdf"

HEADER_RE = re.compile(r"^(#+)\s+(.*)")

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

with open(INPUT, "r", encoding="utf-8") as f:
    lines = f.readlines()

pdf.add_page()
pdf.set_font("Arial", "", 12)

for line in lines:
    line = line.rstrip("\n")
    if not line.strip():
        pdf.ln(5)
        continue
    m = HEADER_RE.match(line)
    if m:
        level = len(m.group(1))
        text = m.group(2)
        size = 16 - (level - 1) * 2
        pdf.set_font("Arial", "B", size if size >= 10 else 10)
        pdf.multi_cell(0, 8, text)
        pdf.set_font("Arial", "", 12)
        pdf.ln(2)
    elif line.startswith("|") and line.endswith("|"):
        # Simple table: render raw
        pdf.set_font("Courier", "", 9)
        pdf.multi_cell(0, 5, line)
        pdf.set_font("Arial", "", 12)
    elif line.startswith("```"):
        # Skip fenced markers
        continue
    else:
        pdf.multi_cell(0, 6, line)

pdf.output(OUTPUT)
print(f"Generado {OUTPUT}")
