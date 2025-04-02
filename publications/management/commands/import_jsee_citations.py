import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import citations from generic structured text files (title/authors/doi/abstract) with per-issue indexing"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., GENERIC_JOURNAL)")
        parser.add_argument("--path", required=True, help="Path to folder with .txt files")

    def handle(self, *args, **options):
        journal_code = options["journal"]
        folder_path = options["path"]

        if journal_code not in journals:
            self.stderr.write(f"❌ Journal not found: {journal_code}")
            return

        model_name = journals[journal_code]
        try:
            model = apps.get_model("publications", model_name)
        except LookupError:
            self.stderr.write(f"❌ Model not found for: {model_name}")
            return

        try:
            journal_instance = JournalPublication.objects.get(name=model._meta.verbose_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(f"❌ JournalPublication instance not found for: {model._meta.verbose_name}")
            return

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
        doi_counter = 1  # Used to create unique placeholder DOIs

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            vol_issue_match = re.match(r"Volume_(\d+)_\((\d{4})\)_Issue_([\d&and]+)", txt_file)
            if not vol_issue_match:
                self.stderr.write(f"❌ Could not extract volume/issue/year from filename: {txt_file}")
                continue

            vol = int(vol_issue_match.group(1))
            year = int(vol_issue_match.group(2))
            issue_string = vol_issue_match.group(3)
            issue_match = re.match(r"(\d+)", issue_string)
            issue = int(issue_match.group(1)) if issue_match else 0

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = [e.strip() for e in content.split("================================================================================") if e.strip()]
            article_counter = 0  # Reset per issue

            for entry in entries:
                try:
                    fields = dict(re.findall(r"^(Title|Authors|DOI|Abstract):\s*(.*)", entry, re.MULTILINE))

                    title = fields.get("Title", "NA").strip() or "NA"
                    authors = fields.get("Authors", "NA").strip() or "NA"
                    abstract = fields.get("Abstract", "").strip()

                    raw_doi = fields.get("DOI", "").strip()
                    if raw_doi in ["", "N/A"]:
                        doi = f"N/A{doi_counter}"
                        doi_counter += 1
                    else:
                        doi = raw_doi
                        if model.objects.filter(doi=doi).exists():
                            continue  # Skip duplicate

                    # Final duplicate check
                    if model.objects.filter(journal=journal_instance, volume=vol, issue=issue, doi=doi).exists():
                        self.stderr.write(f"⚠️ Duplicate: Vol {vol} Issue {issue} DOI {doi} — skipping")
                        continue

                    article_counter += 1
                    article_index = article_counter

                    url = f"https://doi.org/{doi}" if not doi.startswith("N/A") else ""

                    article = model(
                        journal=journal_instance,
                        authors=authors,
                        title=title,
                        abstract=abstract,
                        doi=doi,
                        url=url,
                        volume=vol,
                        issue=issue,
                        year=year,
                        article_index=article_index
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}:\n{entry[:100]}...\nError: {e}")
