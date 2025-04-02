import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import citations for a structured journal with filename-based volume/issue and year"

    volumes_year = {
        25:2025, 24:2024, 23:2023, 22:2022, 21:2021, 20:2020,
        19:2019, 18:2018, 17:2017, 16:2016, 15:2015, 14:2014,
        13:2013, 12:2012, 11:2011, 10:2010, 9:2009, 8:2008,
        7:2007, 6:2006, 5:2005, 4:2004, 3:2003, 2:2002, 1:2001
    }

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code")
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
            self.stderr.write(f"❌ Model not found: {model_name}")
            return

        try:
            journal_instance = JournalPublication.objects.get(name=model._meta.verbose_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(f"❌ JournalPublication instance not found: {model._meta.verbose_name}")
            return

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            # Extract volume and issue from filename
            vol_issue_match = re.match(r"Vol_(\d+)_Issue_(\d+)\.txt", txt_file)
            if not vol_issue_match:
                self.stderr.write(f"❌ Invalid filename format: {txt_file}")
                continue

            vol = int(vol_issue_match.group(1))
            issue = int(vol_issue_match.group(2))
            year = self.volumes_year.get(vol, 1900)

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = [entry.strip() for entry in content.split("================================================================================") if entry.strip()]
            article_counter = 0  # Reset per issue

            for entry in entries:
                try:
                    title = re.search(r"Title:\s*(.*)", entry).group(1).strip()
                    authors = re.search(r"Authors:\s*(.*)", entry).group(1).strip()
                    doi = re.search(r"DOI:\s*(.*)", entry).group(1).strip()
                    abstract_match = re.search(r"Abstract:\s*(.*)", entry, re.S)
                    abstract = abstract_match.group(1).strip() if abstract_match else ""

                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    article_counter += 1
                    article_index = article_counter
                    url = doi

                    if model.objects.filter(
                        journal=journal_instance, volume=vol, issue=issue, article_index=article_index
                    ).exists():
                        self.stderr.write(f"⚠️ Duplicate index: Vol {vol} Issue {issue} Index {article_index} — skipping {doi}")
                        continue

                    article = model(
                        journal=journal_instance,
                        authors=authors if authors else "NA",
                        title=title if title else "NA",
                        abstract=abstract,
                        doi=doi,
                        url=url,
                        volume=vol,
                        issue=issue,
                        year=year,
                        article_index=article_index,
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}:\n{entry[:100]}...\nError: {e}")
