import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import Wiley citations from structured .txt files"

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
            vol, issue = 0, 0
            filename = os.path.basename(txt_file)

            if match := re.search(r"Wiley_Issue(\d{4})", filename):
                year = int(match.group(1))
                vol = int(f"2{str(year)[-2:]}")
                issue = 0
            elif match := re.search(r"Vol(\d+)_Issue(?:_|)(\w+)", filename, re.I):
                vol = int(match.group(1))
                issue_str = match.group(2).lower()
                issue = int(issue_str) if issue_str.isdigit() else 0

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = content.strip().split("================================================================================")
            article_index = 1  # ✅ Reset for each (vol, issue)

            for entry in entries:
                try:
                    if "DOI:" not in entry:
                        continue

                    doi = re.search(r"DOI:\s*(\S+)", entry)
                    doi = doi.group(1).replace("%2F", "/") if doi else None
                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    title = re.search(r"Title:\s*(.*)", entry)
                    authors = re.search(r"Authors:\s*(.*)", entry)
                    abstract = re.search(r"Abstract:\s*(.*)", entry, re.S)
                    pubdate = re.search(r"Publication Date:\s*(\w+\s+)?(\d{4})", entry)

                    title = title.group(1).strip() if title else "NA"
                    authors = authors.group(1).strip() if authors else "NA"
                    abstract = abstract.group(1).strip() if abstract else ""
                    year = year
                    url = f"https://doi.org/{doi}"

                    # Final duplicate check using article_index
                    if model.objects.filter(journal=journal_instance, volume=vol, issue=issue, article_index=article_index).exists():
                        self.stderr.write(f"⚠️ Duplicate index: Vol {vol} Issue {issue} Index {article_index} — skipping {doi}")
                        article_index += 1
                        continue

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
                    article_index += 1  # ✅ Increment within this volume/issue only

                except Exception as e:
                    self.stderr.write(f"❌ Failed entry in {txt_file}:\n{entry[:100]}...\nError: {e}")
