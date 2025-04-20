import html
import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import single-article RIS files (1 per file), with issue-specific indexing."

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., CJCE_CJCE)")
        parser.add_argument("--path", required=True, help="Path to folder with .ris files")

    def handle(self, *args, **options):
        journal_code = options["journal"]
        folder_path = options["path"]

        if journal_code not in journals:
            self.stderr.write(self.style.ERROR(f"❌ Journal not found: {journal_code}"))
            return

        model_name = journals[journal_code]
        try:
            model = apps.get_model("publications", model_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(f"❌ Model not found for: {model_name}"))
            return

        try:
            journal_instance = JournalPublication.objects.get(name=model._meta.verbose_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"❌ JournalPublication instance not found for: {model._meta.verbose_name}"))
            return

        ris_files = [f for f in os.listdir(folder_path) if f.endswith(".ris")]

        for ris_file in ris_files:
            path = os.path.join(folder_path, ris_file)
            self.stdout.write(f"📄 Processing: {path}")

            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]

                # RIS parsing
                data = {}
                for line in lines:
                    match = re.match(r"^([A-Z0-9]{2})\s{0,2}-\s(.*)", line)
                    if match:
                        tag = match.group(1).upper()
                        val = match.group(2).strip()
                        data.setdefault(tag, []).append(val)

                # ✅ Extract title from T1 > TI > T2
                title = next((data.get(k, [None])[0] for k in ["T1", "TI", "T2"] if k in data), None)
                if not title:
                    self.stderr.write(f"⚠️ Missing title in {ris_file}, keys: {list(data.keys())}")
                    title = "NA"

                # ✅ Authors
                authors = "; ".join(data.get("AU", ["NA"]))

                # ✅ Abstract
                abstract = html.unescape(data.get("AB", [""])[0])
                abstract = re.sub(r"<[^>]*>", "", abstract)

                # ✅ DOI
                doi = data.get("DO", [""])[0].strip()
                if not doi:
                    max_id = model.objects.aggregate(Max("id"))["id__max"] or 0
                    doi = f"N/A{max_id + 1}"
                elif model.objects.filter(doi=doi).exists():
                    self.stderr.write(f"⚠️ Skipping duplicate DOI: {doi}")
                    continue

                # ✅ Volume / Issue / Year
                volume = int(data.get("VL", ["0"])[0])
                issue = int(data.get("IS", ["0"])[0])
                year = int(data.get("PY", ["1900"])[0][:4])

                # ✅ URL
                url = data.get("UR", [""])[0]

                # ✅ Determine index per issue
                max_index = model.objects.filter(
                    journal=journal_instance,
                    volume=volume,
                    issue=issue
                ).aggregate(Max("article_index"))

                article_index = (max_index["article_index__max"] or 0) + 1

                # ✅ Save to DB
                article = model(
                    journal=journal_instance,
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    doi=doi,
                    url=url,
                    volume=volume,
                    issue=issue,
                    year=year,
                    article_index=article_index
                )
                article.save()
                self.stdout.write(f"✅ Imported: {title[:70]}")

            except Exception as e:
                self.stderr.write(f"❌ Failed to import {ris_file}:\n{e}")
