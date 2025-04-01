import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import Wiley citations from structured .txt files with per-issue indexing"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., WILEY_EQE)")
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

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            # Extract volume and issue from filename
            vol_issue_match = re.match(r"Wiley_Vol(\d+)_Issue(\w+)\.txt", txt_file)
            if not vol_issue_match:
                self.stderr.write(f"❌ Could not extract volume/issue from filename: {txt_file}")
                continue

            vol = int(vol_issue_match.group(1))
            issue_str = vol_issue_match.group(2)
            issue = int(issue_str) if issue_str.isdigit() else 0

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = [entry.strip() for entry in content.split("================================================================================") if entry.strip()]
            article_counter = 0  # Reset per issue

            for entry in entries:
                try:
                    fields = dict(re.findall(r"^(Title|DOI|Authors|Publication Date|Article URL|PDF Link|Abstract):\s*(.*)", entry, re.MULTILINE))

                    doi = fields.get("DOI", "").replace("%2F", "/").strip()
                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    authors = fields.get("Authors", "NA").strip() or "NA"
                    title = fields.get("Title", "NA").strip() or "NA"
                    abstract = fields.get("Abstract", "").strip()

                    pub_date = fields.get("Publication Date", "1900").strip()
                    year_match = re.search(r"\b(19|20)\d{2}\b", pub_date)
                    year = int(year_match.group(0)) if year_match else 1900

                    url = f"https://doi.org/{doi}"

                    article_counter += 1

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
                        article_index=article_counter
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}:\n{entry[:100]}...\nError: {e}")
