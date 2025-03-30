import os
import re
from collections import defaultdict

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import Springer citations from RIS-style .ris files"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., SPRI_EEV)")
        parser.add_argument("--path", required=True, help="Path to folder with .ris files")

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

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".ris")]

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")
            with open(full_path, "r", encoding="utf-8") as f:
                entries = f.read().strip().split("\nER  -")

            for raw_entry in entries:
                entry = raw_entry.strip()
                if not entry:
                    continue

                try:
                    lines = [line.strip() for line in entry.splitlines() if line.strip()]
                    data = defaultdict(list)

                    for line in lines:
                        if len(line) < 6 or "  - " not in line:
                            continue
                        tag, value = line.split("  - ", 1)
                        data[tag].append(value.strip())

                    doi = data.get("DO", [None])[0]
                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    authors = "; ".join(data.get("AU", [])) or "NA"
                    title = data.get("TI", ["NA"])[0]
                    abstract = data.get("AB", [""])[0]
                    journal_name = data.get("JO", ["NA"])[0]
                    url = data.get("UR", [f"https://doi.org/{doi}"])[0]

                    volume = int(data.get("VL", [0])[0])
                    issue = int(data.get("IS", [0])[0])
                    year = int(data.get("PY", [1900])[0])

                    # Assign article_index per (volume, issue)
                    max_index = (
                        model.objects
                        .filter(journal=journal_instance, volume=volume, issue=issue)
                        .aggregate(Max("article_index"))
                    )
                    article_index = (max_index["article_index__max"] or 0) + 1

                    if model.objects.filter(journal=journal_instance, volume=volume, issue=issue, article_index=article_index).exists():
                        self.stderr.write(f"⚠️ Duplicate index: Vol {volume} Issue {issue} Index {article_index} — skipping {doi}")
                        continue

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
                    self.stderr.write(f"❌ Failed entry in {txt_file}:\n{entry[:150]}...\nError: {e}")
