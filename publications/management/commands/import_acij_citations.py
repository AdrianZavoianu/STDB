import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import JournalPublication

volumes_years = {
    122: 2025, 121: 2024, 120: 2023, 119: 2022, 118: 2021, 117: 2020, 116: 2019, 115: 2018, 114: 2017,
    113: 2016, 112: 2015, 111: 2014, 110: 2013, 109: 2012, 108: 2011, 107: 2010, 106: 2009, 105: 2008,
    104: 2007, 103: 2006, 102: 2005, 101: 2004, 100: 2003, 99: 2002, 98: 2001, 97: 2000, 96: 1999,
    95: 1998, 94: 1997, 93: 1996, 92: 1995, 91: 1994, 90: 1993, 89: 1992, 88: 1991, 87: 1990, 86: 1989,
    85: 1988, 84: 1987,
}

class Command(BaseCommand):
    help = "Import ACI journal articles from text files"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., ACI)")
        parser.add_argument("--path", required=True, help="Directory with .txt files")

    def handle(self, *args, **options):
        journal_code = options["journal"]
        folder_path = options["path"]

        if journal_code not in journals:
            self.stderr.write(f"❌ Journal code not recognized: {journal_code}")
            return

        model_name = journals[journal_code]
        try:
            model = apps.get_model("publications", model_name)
        except LookupError:
            self.stderr.write(f"❌ Could not find model for journal: {model_name}")
            return

        try:
            journal_instance = JournalPublication.objects.get(name=model._meta.verbose_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(f"❌ JournalPublication instance not found for: {model._meta.verbose_name}")
            return

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
        na_counter = 1

        for txt_file in txt_files:
            self.stdout.write(f"📄 Processing: {txt_file}")
            match = re.match(r"ACI_Vol(\d+)_Issue(\d+)_Page\d+\.txt", txt_file)
            if not match:
                self.stderr.write(f"❌ Filename format not recognized: {txt_file}")
                continue

            volume = int(match.group(1))
            issue = int(match.group(2))
            year = volumes_years.get(volume, 1900)

            full_path = os.path.join(folder_path, txt_file)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            article_blocks = re.split(r"\n\s*\n", content.strip())
            article_index = 1

            for block in article_blocks:
                try:
                    title = re.search(r"Title:\s*(.*)", block).group(1).strip()
                    authors = re.search(r"Authors:\s*(.*)", block).group(1).strip()
                    doi_match = re.search(r"DOI:\s*(.*)", block)
                    doi = doi_match.group(1).strip() if doi_match else ""
                    abstract_match = re.search(r"Abstract:\s*(.*)", block, re.DOTALL)
                    abstract = abstract_match.group(1).strip() if abstract_match else ""

                    if not doi or doi.upper() == "N/A":
                        doi = f"N/A{na_counter}"
                        na_counter += 1

                    if model.objects.filter(doi=doi).exists():
                        self.stdout.write(f"⚠️ Skipping duplicate DOI: {doi}")
                        continue

                    article = model(
                        journal=journal_instance,
                        authors=authors,
                        title=title,
                        abstract=abstract,
                        doi=doi,
                        url=f"https://doi.org/{doi}" if not doi.startswith("N/A") else "",
                        volume=volume,
                        issue=issue,
                        year=year,
                        article_index=article_index,
                    )
                    article.save()
                    article_index += 1
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to import article from block:\n{block[:200]}...\nError: {e}")
