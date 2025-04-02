import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import citations for journal with files named like 1_01_1964_1.txt and structured entries"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., ENGJ)")
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
            self.stdout.write(f"📄 Processing: {txt_file}")
            full_path = os.path.join(folder_path, txt_file)

            match = re.match(r"(\d+)_([0-9]+)_(\d{4})_\d+\.txt", txt_file)
            if not match:
                self.stderr.write(f"❌ Could not parse filename: {txt_file}")
                continue

            volume = int(match.group(1))
            issue = int(match.group(2))
            year = int(match.group(3))

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = [entry.strip() for entry in content.split("=" * 80) if entry.strip()]
            article_counter = 0
            na_counter = 1

            for entry in entries:
                try:
                    fields = dict(re.findall(r"^(Title|Authors|DOI|Abstract):\s*(.*)", entry, re.MULTILINE))

                    title = fields.get("Title", "NA").strip() or "NA"
                    authors = fields.get("Authors", "NA").strip() or "NA"
                    abstract = fields.get("Abstract", "").strip()
                    doi_raw = fields.get("DOI", "").strip()
                    doi = doi_raw if doi_raw.upper() != "N/A" else None
                    url = f"https://doi.org/{doi}" if doi else ""

                    if not doi:
                        doi = f"N/A{na_counter}"
                        na_counter += 1
                        url = ""

                    # Final duplicate check
                    if model.objects.filter(doi=doi).exists():
                        self.stderr.write(f"⚠️ Duplicate DOI: {doi} — skipping")
                        continue

                    article_counter += 1

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
                        article_index=article_counter
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}:\n{entry[:100]}...\nError: {e}")
