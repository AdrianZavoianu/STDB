import os
import re

from django.core.management.base import BaseCommand

from publications.models import (ConferenceProceeding, Country, DocumentType,
                                 WCEEProceedings)

WCEE_YEARS = {
    '1': 1956, '2': 1960, '3': 1965, '4': 1969, '5': 1974, '6': 1977,
    '7': 1980, '8': 1984, '9': 1988, '10': 1992, '11': 1996, '12': 2000,
    '13': 2004, '14': 2008, '15': 2012, '16': 2017, '17': 2021, '18': 2024
}

COUNTRY_ALIASES = {
    "USA": "United States",
    "Russia": "Russian Federation",
    "Iran": "Iran, Islamic Republic of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Macedonia": "North Macedonia",
    "Republic of Macedonia": "North Macedonia",
    "Moldova": "Moldova, Republic of",
    "Republic of Moldova": "Moldova, Republic of",
    "Czechoslovakia": "Czechia",
    "Czech Republic": "Czechia",
    "Republic of Indonesia": "Indonesia",
    "Argentine": "Argentina",
    "Republic of Uzbekistan": "Uzbekistan",
    "-": "Others",
    "West Germany": "Germany",
    "Yugoslavia": "Serbia",
    "Korea": "Korea, Democratic People's Republic of",
    "South Korea": "Korea, Democratic People's Republic of",
    "Taiwan": "Taiwan, Province of China",
    "Saltanate of Oman": "Oman",
    "England": "United Kingdom",
    "México": "Mexico",
    "UK": "United Kingdom",
    "Vietnam": "Viet Nam",
    "U.S.A.": "United States",
    "Republic of Korea": "Korea, Democratic People's Republic of",
    "UAE": "United Arab Emirates",
    "Western Australia": "Australia",
    "Iran.": "Iran, Islamic Republic of",
    "California": "United States",
    "Usa": "United States",
    "Alabama": "United States",
    "Us": "United States",
    "": "Others",
    "Uk": "United Kingdom",
    "New York": "United States",
    "Columbia": "Colombia",
    "Lebanon (Arab)": "Lebanon",
    "Salvador": "El Salvador",
    "United States of America": "United States",
    "Republic of North Macedonia": "North Macedonia",
    "SOUTH KOREA": "Korea, Democratic People's Republic of",
    "TAIWAN": "Taiwan, Province of China",
    "IRAN": "Iran, Islamic Republic of",
    "REPUBLIC OF MACEDONIA – FYROM": "North Macedonia",
    "RUSSIA": "Russian Federation",
    "THE NETHERLANDS": "Netherlands",
    "CZECH REPUBLIC": "Czechia",
    # Extend as needed
}

class Command(BaseCommand):
    help = "Import WCEE articles from structured .txt files with country-specific indexing"

    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, help="Path to folder with .txt files")

    def handle(self, *args, **options):
        folder_path = options["path"]

        try:
            doc_type = DocumentType.objects.get(name="Conference Article")
            conference = ConferenceProceeding.objects.get(name__icontains="World Conference", doc_type=doc_type)
        except ConferenceProceeding.DoesNotExist:
            self.stderr.write("❌ Conference proceeding not found.")
            return

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
        failed_files = []

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]

                data = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data[key.strip().lower()] = value.strip()

                title = data.get("title", "NA")
                authors = data.get("author", "NA")
                url = data.get("article url", None)

                edition_str = data.get("conference", "").replace("WCEE", "").strip()
                edition = int(edition_str) if edition_str.isdigit() else None
                year = WCEE_YEARS.get(str(edition), None)

                raw_country = data.get("country", "").split(",")[0].strip()
                resolved_name = COUNTRY_ALIASES.get(raw_country, raw_country)
                country = Country.objects.get(name__iexact=resolved_name)

                index = (
                    WCEEProceedings.objects
                    .filter(conference=conference, edition=edition, country=country)
                    .count() + 1
                )

                article = WCEEProceedings(
                    conference=conference,
                    title=title,
                    authors=authors,
                    abstract="",
                    year=year,
                    edition=edition,
                    url=url,
                    article_index=index,
                    file_source="S",
                    file_exists=False,
                    country=country,
                )
                article.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Imported: {title[:60]}..."))

            except Exception as e:
                self.stderr.write(f"❌ Failed to import {txt_file}:\n{e}")
                failed_files.append(txt_file)

        if failed_files:
            self.stdout.write("\n⚠️ The following files failed to import:")
            for f in failed_files:
                self.stdout.write(f"- {f}")
        else:
            self.stdout.write("\n✅ All files imported successfully.")
