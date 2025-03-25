# publications/management/commands/import_asce_articles.py

import os
import re
from collections import defaultdict

from django.core.management.base import BaseCommand

from publications.models import (ASCEJournalStructuralEngineering,
                                 JournalPublication)


class Command(BaseCommand):
    help = 'Import ASCE Journal Articles from all text files in /data/'

    def handle(self, *args, **options):
        journal_name = "ASCE Journal of Structural Engineering"
        data_dir = "data"
        file_pattern = ".txt"

        try:
            journal = JournalPublication.objects.get(name=journal_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Journal '{journal_name}' not found. Please add it first."))
            return

        issue_counter = defaultdict(int)

        for filename in sorted(os.listdir(data_dir)):
            if not filename.endswith(file_pattern):
                continue

            full_path = os.path.join(data_dir, filename)
            self.stdout.write(self.style.NOTICE(f"Processing {filename}..."))

            with open(full_path, encoding="utf-8") as file:
                raw_text = file.read()

            articles = re.split(r"\n\s*TI\s+-", raw_text)[1:]

            for block in articles:
                fields = {
                    "authors": [],
                    "title": "",
                    "abstract": "",
                    "year": None,
                    "volume": None,
                    "issue": None,
                    "doi": "",
                    "url": "",
                }

                lines = block.strip().split("\n")
                fields["title"] = lines[0].strip()
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith("AU - "):
                        fields["authors"].append(line.replace("AU - ", "").strip())
                    elif line.startswith("DP - "):
                        fields["year"] = int(line.replace("DP - ", "").strip())
                    elif line.startswith("VI - "):
                        fields["volume"] = int(line.replace("VI - ", "").strip())
                    elif line.startswith("IP - "):
                        fields["issue"] = int(line.replace("IP - ", "").strip())
                    elif line.startswith("AID - "):
                        doi_match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", line, re.IGNORECASE)
                        if doi_match:
                            fields["doi"] = doi_match.group(0)
                    elif re.match(r"^4100\s+-", line):
                        fields["url"] = line.split("-", 1)[1].strip()
                    elif line.startswith("AB - "):
                        fields["abstract"] = line.replace("AB - ", "").strip()
                    elif fields["abstract"] and not any(
                        line.startswith(tag) for tag in (
                            "AU -", "TI -", "PT -", "DP -", "TA -", "PG -", "VI -", "IP -",
                            "AID -", "4099", "4100", "SO -")
                    ):
                        fields["abstract"] += " " + line

                # Assign article index per volume/issue pair
                key = (fields["volume"], fields["issue"])
                issue_counter[key] += 1
                article_index = issue_counter[key]

                authors = ", ".join(fields["authors"])
                ASCEJournalStructuralEngineering.objects.create(
                    journal=journal,
                    title=fields["title"],
                    authors=authors,
                    abstract=fields["abstract"],
                    volume=fields["volume"],
                    issue=fields["issue"],
                    article_index=article_index,
                    year=fields["year"],
                    doi=fields["doi"],
                    url=fields["url"]
                )

                self.stdout.write(self.style.SUCCESS(
                    f"[{filename}] Imported: {fields['title'][:60]}... (Vol {fields['volume']} Issue {fields['issue']} Index {article_index})"
                ))
