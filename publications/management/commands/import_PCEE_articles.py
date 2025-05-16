import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals  # optional if mapping used
from publications.models import ConferenceProceeding, Country, DocumentType


class Command(BaseCommand):
    help = "Import PCEE articles from filenames"

    def handle(self, *args, **options):
        # === Customize these ===
        conference_name = "Pacific Conference on Earthquake Engineering"
        edition = 19
        year = 2019
        country_name = "New Zealand"
        file_source = "L"
        folder_path = "data"

        # === Fetch database objects ===
        try:
            conference = ConferenceProceeding.objects.get(name=conference_name)
        except ConferenceProceeding.DoesNotExist:
            self.stderr.write(f"❌ Conference not found: {conference_name}")
            return

        try:
            country = Country.objects.get(name__iexact=country_name)
        except Country.DoesNotExist:
            self.stderr.write(f"❌ Country not found: {country_name}")
            return

        model = apps.get_model("publications", "PCEEProceedings")
        filenames = sorted(f for f in os.listdir(folder_path) if f.lower().endswith(".pdf"))

        counter = 0
        for fname in filenames:
            try:
                # Remove session prefix and extract metadata
                clean_name = re.sub(r"^\s*[\w.]+\s*", "", fname)
                parts = clean_name.replace(".pdf", "").split(" - ", maxsplit=1)
                if len(parts) != 2:
                    self.stderr.write(f"⚠️  Skipping malformed filename: {fname}")
                    continue

                authors = parts[0].strip()
                title = parts[1].strip()
                article_index = counter + 1

                # Avoid duplicates
                if model.objects.filter(
                    conference=conference, edition=edition, country=country, article_index=article_index
                ).exists():
                    self.stderr.write(f"⚠️  Skipping duplicate index {article_index} for {title[:50]}")
                    continue

                article = model(
                    conference=conference,
                    country=country,
                    edition=edition,
                    year=year,
                    title=title,
                    authors=authors,
                    abstract="",
                    article_index=article_index,
                    url="",
                    file_source=file_source,
                )
                article.save()
                self.stdout.write(f"✅ Imported: {title[:60]}...")
                counter += 1

            except Exception as e:
                self.stderr.write(f"❌ Failed to import {fname}: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Finished importing {counter} articles."))
