import csv

from django.core.management.base import BaseCommand

from publications.models import WCEEProceedings


class Command(BaseCommand):
    help = "Export normalized article index and filename for a specific WCEE edition"

    TARGET_EDITION = 15  # 🔧 Change the edition here
    OUTPUT_FILE = f"wcee_filenames_edition_{TARGET_EDITION}.csv"

    def handle(self, *args, **options):
        queryset = WCEEProceedings.objects.filter(edition=self.TARGET_EDITION).order_by("id")
        count = queryset.count()

        with open(self.OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Index", "Filename"])

            for idx, article in enumerate(queryset, start=1):
                writer.writerow([f"{idx:04}", article.filename()])

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {count} filenames for edition {self.TARGET_EDITION} to {self.OUTPUT_FILE}"))
