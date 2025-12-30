import logging
import tqdm
import os
import pytesseract

from pdf2image import convert_from_path


class OCRConverter:
    def __init__(self):
        self.pdf_aspect_map = {
                "Bipolar-Disorder-A-Guide.pdf": "Mania",
                "Coping-with-Trauma-Related-Dissociation.pdf": "Dissociation",
                "Feeling-Good-The-New-Mood-Therapy.pdf": "Depression",
                "New-Harbinger-Self-Help-Workbook-The-Addiction-Recovery-Skills.pdf": "Substance Use",
                "Night-Falls-Fast-Understanding-Suicide.pdf": "Suicidal",
                "Overcoming-Harm-OCD.pdf": "Repetitive Thought",
                "RelasiSehat.pdf": "General",
                "Say-Good-Night-to-Insomnia.pdf": "Sleep Disturbance",
                "The-Anger-Workbook.pdf": "Anger",
                "The-Anxiety-and-Phobia-Workbook.pdf": "Anxiety",
                "The-Body-Keeps-the-Score-PDF.pdf": "Somatic",
                "The-Science-of-Successful-Learning.pdf": "Memory",
                "Understanding-Psychosis-and-Schizophrenia.pdf": "Psychosis"
        }
        self.files_dir = "./text_files"
        self.pdfs_dir = "../../external_data/pdfs"

    def convert_all_pdfs(self):
        logging.info("OCR Converter: Starting conversion of all PDFs")
        files = self.pdf_aspect_map.keys()

        for file_name in tqdm(files, desc="Converting PDFs", unit="file"):
            aspect = self.pdf_aspect_map[file_name]
            pdf_path = os.path.join(self.pdfs_dir, file_name)

            if not pdf_path:
                logging.error(f"PDF not found: {pdf_path}")
                continue

            try:
                text = self.convert_single_pdf(pdf_path)
            except Exception as err:
                logging.error(f"Failed OCR on {file_name}: {err}")

            out_file = os.path.join(self.files_dir, f"{aspect}.txt")
            try:
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(text)
                logging.info(f"Saved: {out_file}")
            except Exception as err:
                logging.error(f"Failed saving {out_file}: {err}")

        return
    
    def convert_single_pdf(self, pdf_path):
        logging.info(f"OCR Converter: Reading {pdf_path}")

        pages = convert_from_path(pdf_path, dpi=300)
        text_output = []

        for idx, page in enumerate(pages):
            page_text = pytesseract.image_to_string(page, lang='eng')
            text_output.append(page_text)

            page.close()

        return "\n".join(text_output)