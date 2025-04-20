import html
import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import BNZSEE citations from individual RIS files"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., BNZ_BNZSEE)")
        parser.add_argument("--path", required=True, help="Path to folder containing .ris files")

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

        ris_files = [f for f in os.listdir(folder_path) if f.endswith(".ris")]

        for ris_file in ris_files:
            full_path = os.path.join(folder_path, ris_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse RIS into dictionary
                data = {}
                for line in content.splitlines():
                    if "  - " in line:
                        tag, value = line.split("  - ", 1)
                        data.setdefault(tag.strip(), []).append(value.strip())

                doi = data.get("DO", [None])[0]
                title = data.get("TI", ["NA"])[0]
                authors = "; ".join(data.get("AU", ["NA"])) or "NA"
                abstract_raw = data.get("AB", [""])[0]
                abstract = html.unescape(re.sub(r"<[^>]+>", "", abstract_raw))  # Strip tags
                url = data.get("UR", [None])[0]
                volume = int(data.get("VL", [0])[0])
                issue = int(data.get("IS", [0])[0])
                year = int(data.get("PY", ["1900"])[0][:4])  # Extract year from YYYY/MM/DD

                # Assign next article_index per (volume, issue)
                max_index = (
                    model.objects
                    .filter(journal=journal_instance, volume=volume, issue=issue)
                    .aggregate(Max("article_index"))
                )
                article_index = (max_index["article_index__max"] or 0) + 1

                if doi and model.objects.filter(doi=doi).exists():
                    self.stderr.write(f"⚠️ Duplicate DOI — skipping: {doi}")
                    continue

                if not doi:
                    # Assign unique placeholder DOI
                    doi = f"N/A{model.objects.count() + 1}"

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
                self.stdout.write(f"✅ Imported: {title[:60]}...")

            except Exception as e:
                self.stderr.write(f"❌ Failed to import article:\n{data}\nError: {e}")
