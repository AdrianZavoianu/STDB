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
                        continue

                    doi_match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", entry, re.I)
                    doi = doi_match.group(1).strip() if doi_match else None
                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    authors = title = "NA"
                    abstract = ""
                    url = f"https://doi.org/{doi}"
                    lines = [l.strip() for l in entry.splitlines() if l.strip()]

                    # Authors and title: assume 2 lines before the journal name
                    for i, line in enumerate(lines):
                        if "Computers & Structures" in line:
                            if i >= 2:
                                authors = lines[i - 2]
                                title = lines[i - 1]
                            break

                    # Year
                    year_match = re.search(r"\b(19|20)\d{2}\b", entry)
                    year = int(year_match.group(0)) if year_match else 1900

                    # Volume (handle 'Volumes 90–91' or 'Volume 38')
                    vol_match = re.search(r"Volumes?\s+(\d+)", entry)
                    if not vol_match:
                        raise ValueError("Missing volume number")
                    volume = int(vol_match.group(1))

                    # Issue (handle 'Issues 5–6' or 'Issue 6')
                    issue_match = re.search(r"Issues?\s+(\d+)", entry)
                    issue = int(issue_match.group(1)) if issue_match else 0

                    # Abstract
                    abstract_match = re.search(r"Abstract:(.*?)Keywords:", entry, re.S)
                    if abstract_match:
                        abstract = abstract_match.group(1).strip()
                    else:
                        # fallback: try from 'Abstract:' to next DOI
                        abstract_match = re.search(r"Abstract:(.*)", entry, re.S)
                        if abstract_match:
                            abstract = abstract_match.group(1).strip()

                    article = model(
                        journal=journal_instance,
                        authors=authors,
                        title=title,
                        abstract=abstract,
                        doi=doi,
                        url=url,
                        volume=volume,
                        issue=issue,
                        year=year,
                        article_index=article_index,
                    )
                    article.save()
                    article_index += 1
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}: {e}")
