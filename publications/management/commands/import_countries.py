import csv
import os

from django.core.management.base import BaseCommand

from publications.models import Country  # Adjust the import path if needed


class Command(BaseCommand):
    help = "Import countries from a CSV file"

    def handle(self, *args, **options):
        csv_path = "data/iso_3166_country_codes.csv"  # Adjust path if needed

        if not os.path.exists(csv_path):
            self.stderr.write(f"❌ File not found: {csv_path}")
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                _, created = Country.objects.get_or_create(
                    name=row["Name"],
                    alpha2=row["Alpha-2 Code"],
                    alpha3=row["Alpha-3 Code"],
                    numeric=row["Numeric Code"],
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} countries from {csv_path}"))
