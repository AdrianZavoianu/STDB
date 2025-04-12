import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication


class Command(BaseCommand):
    help = "Import custom citations from structured .txt files with Volume and Issue in filename"

    # volumes_years = {
    #     29: 2025, 28: 2024, 27: 2023, 26: 2022, 25: 2021, 24: 2020,
    #     23: 2019, 22: 2018, 21: 2017, 20: 2016, 19: 2015, 18: 2014,
    #     17: 2013, 16: 2012, 15: 2011, 14: 2010, 13: 2009, 12: 2008,
    #     11: 2007, 10: 2006, 9: 2005, 8: 2004, 7: 2003, 6: 2002,
    #     5: 2001, 4: 2000, 3: 1999, 2: 1998, 1: 1997
    # }
    # volumes_years = {32:2025, 31:2024, 30:2023, 29:2022, 28:2021, 27:2020,
    #                  26:2019, 25:2018, 24:2017, 23:2016, 22:2015, 21:2014,
    #                  20:2013, 19:2012, 18:2011, 17:2010, 16:2009, 15:2008,
    #                  14:2007, 13:2006, 12:2005, 11:2004, 10:2003, 9:2002,
    #                  8:2001, 7:2000, 6:1999, 5:1998, 4:1997, 3:1996,
    #                  2:1995, 1:1994}
    # volumes_years = {34:2024, 33:2023, 32:2022, 31:2021, 30:2020, 29:2019,
    #                  28:2018, 27:2017, 26:2016, 25:2015, 24:2014, 23:2013,
    #                  22:2012, 21:2011, 20:2010, 19:2009, 18:2008, 17:2007,
    #                  16:2006, 15:2005, 14:2004, 13:2003, 12:2002, 11:2001,
    #                  10:2000, 9:1999, 8:1998, 7:1997, 6:1996, 5:1995,
    #                  4:1994, 3:1993, 2:1992, 1:1991
    # }
    volumes_years = {9:2017, 8:2016, 7:2015, 6:2014, 5:2013, 4:2012,
                     3:2011, 2:2010, 1:2009}

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., TAYF_EEQE)")
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
            match = re.search(r"Vol_(\d+)_Issue_(\w+)", txt_file, re.I)
            if not match:
                self.stderr.write(f"⚠️ Could not extract volume/issue from filename: {txt_file}")
                continue

            volume = int(match.group(1))
            issue_raw = match.group(2)
            issue = 0 if "sup" in issue_raw.lower() else int(issue_raw)

            year = self.volumes_years.get(volume, 1900)

            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"\n📄 Processing: {txt_file} (Vol {volume}, Issue {issue}, Year {year})")

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = content.strip().split("=" * 75)

            for entry in entries:
                try:
                    entry = entry.strip()
                    if not entry or "DOI:" not in entry:
                        continue

                    lines = [line.strip() for line in entry.splitlines() if line.strip()]

                    title_line = next((l for l in lines if l.startswith("Title:")), None)
                    author_line = next((l for l in lines if l.startswith("Authors:")), None)
                    doi_line = next((l for l in lines if l.startswith("DOI:")), None)
                    abstract_line = next((l for l in lines if l.startswith("Abstract:")), None)

                    title = title_line.replace("Title:", "").strip() if title_line else "NA"
                    authors = author_line.replace("Authors:", "").strip() if author_line else "NA"
                    doi = doi_line.replace("DOI:", "").strip() if doi_line else None
                    abstract = abstract_line.replace("Abstract:", "").strip() if abstract_line else ""

                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    url = f"https://doi.org/{doi}"

                    # Assign unique article index per (journal, volume, issue)
                    max_index = (
                        model.objects
                        .filter(journal=journal_instance, volume=volume, issue=issue)
                        .aggregate(Max("article_index"))
                    )
                    article_index = (max_index["article_index__max"] or 0) + 1

                    # Final duplicate check
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
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}:\n{entry[:150]}...\nError: {e}")
