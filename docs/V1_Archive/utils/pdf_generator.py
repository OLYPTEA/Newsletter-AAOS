from fpdf import FPDF
import os

class PDFGenerator:
    """
    Utilitaire pour transformer le contenu Markdown d'une newsletter en PDF.
    """
    def __init__(self, content, title="Hermes Newsletter"):
        self.content = content
        self.title = title

    def generate(self, output_path):
        pdf = FPDF()
        pdf.add_page()

        # Police standard
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, self.title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        # On nettoie un peu le markdown basique pour le PDF
        clean_text = self.content.replace("# ", "").replace("## ", "").replace("**", "")

        for line in clean_text.split('\n'):
            pdf.multi_cell(0, 10, line)
            pdf.ln(2)

        pdf.output(output_path)
        return output_path
