import os
import shutil
from datetime import datetime
from utils.pdf_generator import PDFGenerator

class AgentA4:
    """
    A4: L'agent de livraison.
    Convertit le brouillon en PDF et archive la livraison.
    """
    def __init__(self):
        self.draft_path = "newsletter_draft.md"
        self.archive_dir = "newsletters/archives"

    def deliver(self):
        if not os.path.exists(self.draft_path):
            print("[ERREUR A4] : Aucun document à livrer.")
            return

        # 1. Conversion en PDF
        with open(self.draft_path, "r", encoding="utf-8") as f:
            content = f.read()

        now = datetime.now()
        date_folder = now.strftime("%Y-%m")
        target_dir = os.path.join(self.archive_dir, date_folder)
        os.makedirs(target_dir, exist_ok=True)

        filename_pdf = f"newsletter_{now.strftime('%Y-%m-%d')}.pdf"
        pdf_path = os.path.join(target_dir, filename_pdf)

        print(f"📄 A4 : Conversion en PDF en cours...")
        try:
            generator = PDFGenerator(content, title="Hermes Newsletter")
            generator.generate(pdf_path)
        except Exception as e:
            print(f"[ERREUR PDF] : {e}")
            return

        # 2. Archivage du Markdown original
        filename_md = f"newsletter_{now.strftime('%Y-%m-%d')}.md"
        md_path = os.path.join(target_dir, filename_md)
        shutil.copy(self.draft_path, md_path)

        # 3. Log de livraison
        os.makedirs("logs", exist_ok=True)
        with open("logs/delivery_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] - {filename_pdf} - Statut : OK\n")

        print(f"🚚 A4 : Livraison effectuée avec succès.")
        print(f"📍 Fichiers archivés dans : {target_dir}")

if __name__ == "__main__":
    a4 = AgentA4()
    a4.deliver()
