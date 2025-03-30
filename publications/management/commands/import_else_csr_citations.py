import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import Elsevier citations from structured .txt files"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., ELSE_CSR)")
        parser.add_argument("--path", required=True, help="Path to folder with .txt files")

    def handle(self, *args, **options):
        journal_code = options["journal"]
        folder_path = options["path"]

        if journal_code not in journals:
            self.stderr.write(f"Journal not found: {journal_code}")
            return

        model_name = journals[journal_code]
        try:
            model = apps.get_model("publications", model_name)
        except LookupError:
            self.stderr.write(f"Model not found for: {model_name}")
            return

        try:
            journal_instance = JournalPublication.objects.get(name=model._meta.verbose_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(f"JournalPublication instance not found for: {model._meta.verbose_name}")
            return

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = content.strip().split("\n\n")
            article_index = 1
            for entry in entries:
                try:
                    if "doi.org" not in entry:
                        continue  # skip if no DOI

                    doi_match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", entry, re.I)
                    doi = doi_match.group(1).strip() if doi_match else None
                    if not doi:
                        continue

                    if model.objects.filter(doi=doi).exists():
                        continue

                    # Set defaults
                    authors = "NA"
                    title = "NA"
                    abstract = ""
                    keywords = ""
                    url = f"https://doi.org/{doi}"

                    # Extract authors, title, volume, etc.
                    lines = entry.splitlines()
                    lines = [l.strip() for l in lines if l.strip()]
                    vol = issue = year = None

                    # Attempt to find volume number first
                    vol_match = re.search(r"Volume\s+(\d+)", entry)
                    if vol_match:
                        vol = int(vol_match.group(1))
                    else:
                        raise ValueError("Missing volume number")

                    issue_match = re.search(r"Issue\s+(\d+)", entry)
                    issue = int(issue_match.group(1)) if issue_match else 0

                    year_match = re.search(r"\b(19|20)\d{2}\b", entry)
                    year = int(year_match.group(0)) if year_match else 1900

                    # Authors, title, journal format assumption
                    idx = 0
                    if "Journal of" in lines[2]:
                        authors = lines[0] if lines[0] else "NA"
                        title = lines[1] if lines[1] else "NA"
                    else:
                        # Try heuristic fallback for short entries
                        for i, line in enumerate(lines):
                            if "Journal of" in line:
                                authors = lines[i - 2] if i >= 2 else "NA"
                                title = lines[i - 1] if i >= 1 else "NA"
                                break

                    # Abstract
                    abstract_match = re.search(r"Abstract:(.*?)Keywords:", entry, re.S)
                    if abstract_match:
                        abstract = abstract_match.group(1).strip()

                    # Create article
                    article = model(
                        journal=journal_instance,
                        authors=authors or "NA",
                        title=title or "NA",
                        abstract=abstract,
                        doi=doi,
                        url=url,
                        volume=vol,
                        issue=issue,
                        year=year,
                        article_index=article_index
                    )
                    article.save()
                    article_index += 1
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}: {e}")
