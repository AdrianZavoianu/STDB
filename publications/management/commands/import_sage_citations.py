import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import Sage citations from .ris files with per-issue article indexing"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., SAGE_EQS)")
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

        ris_files = [f for f in os.listdir(folder_path) if f.endswith(".ris")]

        for ris_file in ris_files:
            full_path = os.path.join(folder_path, ris_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            vol_match = re.search(r"Vol_(\d+)_Issue_(\d+)\.ris", ris_file)
            if not vol_match:
                self.stderr.write(f"❌ Filename format incorrect: {ris_file}")
                continue

            volume = int(vol_match.group(1))
            issue = int(vol_match.group(2))

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read().replace("\xa0", " ")  # Normalize non-breaking spaces

            entries = [entry.strip() for entry in content.split("ER  -") if entry.strip()]
            article_index = 0  # reset for each issue

            for entry in entries:
                try:
                    field_dict = dict(re.findall(r"(?m)^([A-Z0-9]{2})  - (.*)", entry))
                    doi = field_dict.get("DO", "").strip()
                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    title = field_dict.get("T1", "NA").strip()
                    abstract = field_dict.get("N2", "").strip()
                    authors = ", ".join(re.findall(r"(?m)^AU  - (.*)", entry)) or "NA"
                    url = field_dict.get("UR", f"https://doi.org/{doi}")

                    year = int(field_dict.get("PY", "1900"))

                    article_index += 1

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
                        article_index=article_index
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to import entry:\n{entry[:100]}...\nError: {e}")
