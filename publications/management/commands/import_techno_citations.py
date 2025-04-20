import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import Techno-Press journal citations from structured single-article text files."

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., TAFR_JEE)")
        parser.add_argument("--path", required=True, help="Path to folder containing article .txt files")

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

        # Track index per (volume, issue)
        issue_index_tracker = {}

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        for filename in txt_files:
            file_path = os.path.join(folder_path, filename)
            self.stdout.write(f"📄 Processing: {filename}")

            match = re.match(r"Vol(\d+)_Issue(\d+)_Y(\d{4})_", filename)
            if not match:
                self.stderr.write(f"❌ Invalid filename format: {filename}")
                continue

            vol = int(match.group(1))
            issue = int(match.group(2))
            year = int(match.group(3))

            key = (vol, issue)
            if key not in issue_index_tracker:
                issue_index_tracker[key] = 1
            else:
                issue_index_tracker[key] += 1
            article_index = issue_index_tracker[key]

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                def extract_field(label):
                    match = re.search(rf"{label}:\s*(.*?)\n(?=\w+:|$)", content, re.S)
                    return match.group(1).strip() if match else "NA"

                title = extract_field("Title")
                authors = extract_field("Authors")
                doi = extract_field("DOI")
                url = extract_field("URL")
                abstract = extract_field("Abstract")

                if model.objects.filter(doi=doi).exists():
                    self.stderr.write(f"⚠️ Skipping duplicate DOI: {doi}")
                    continue

                article = model(
                    journal=journal_instance,
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    doi=doi if doi != "N/A" else None,
                    url=url if url != "N/A" else None,
                    year=year,
                    volume=vol,
                    issue=issue,
                    article_index=article_index,
                )
                article.save()
                self.stdout.write(f"✅ Imported: {title[:60]}...")

            except Exception as e:
                self.stderr.write(f"❌ Failed to process {filename}: {e}")
