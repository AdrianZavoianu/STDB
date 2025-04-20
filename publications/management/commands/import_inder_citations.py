import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import IJMRI articles from structured .txt files"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., IJMRI)")
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

        placeholder_counter = 1
        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        for txt_file in sorted(txt_files):
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            match = re.match(r"IJMRI_(\d{4})_Vol(\d+)_Issue(\d+(?:[-&]\d+)*)\.txt", txt_file)
            if not match:
                self.stderr.write(f"⚠️ Skipping invalid file name: {txt_file}")
                continue

            year = int(match.group(1))
            volume = int(match.group(2))
            issue = int(re.split(r"[-&]", match.group(3))[0])  # use first issue if multiple

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = [e.strip() for e in content.split("=" * 80) if e.strip()]
            index = 1

            for entry in entries:
                try:
                    title_match = re.search(r"Title:\s*(.*)", entry)
                    authors_match = re.search(r"Authors:\s*(.*)", entry)
                    doi_match = re.search(r"DOI:\s*(.*)", entry)
                    url_match = re.search(r"URL:\s*(.*)", entry)
                    abstract_match = re.search(r"Abstract:\s*(.*)", entry, re.DOTALL)

                    title = title_match.group(1).strip() if title_match else "NA"
                    authors = authors_match.group(1).strip() if authors_match else "NA"
                    doi = doi_match.group(1).strip() if doi_match else ""
                    url = url_match.group(1).strip() if url_match else ""
                    abstract = abstract_match.group(1).strip() if abstract_match else ""

                    if not doi or doi.upper() == "N/A":
                        doi = f"N/A{placeholder_counter}"
                        placeholder_counter += 1

                    if model.objects.filter(doi=doi).exists():
                        self.stdout.write(f"⏭️ Skipped duplicate DOI: {doi}")
                        continue

                    if model.objects.filter(journal=journal_instance, volume=volume, issue=issue, article_index=index).exists():
                        self.stdout.write(f"⏭️ Skipped duplicate index: Vol {volume} Issue {issue} Index {index}")
                        index += 1
                        continue

                    article = model(
                        journal=journal_instance,
                        title=title,
                        authors=authors,
                        abstract=abstract,
                        doi=doi,
                        url=url,
                        year=year,
                        volume=volume,
                        issue=issue,
                        article_index=index,
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")
                    index += 1

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file} (index {index}): {e}")
