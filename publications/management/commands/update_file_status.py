import os

from django.conf import settings
from django.core.management.base import BaseCommand

from publications.models import ASCEJournalStructuralEngineering


class Command(BaseCommand):
    help = "Update file_exists status for all ASCE journal articles"

    def handle(self, *args, **kwargs):
        pdf_dir = os.path.join(settings.MEDIA_ROOT, "publications")

        updated = 0
        for article in ASCEJournalStructuralEngineering.objects.all():
            expected_path = os.path.join(pdf_dir, article.filename())
            file_present = os.path.isfile(expected_path)
            if article.file_exists != file_present:
                article.file_exists = file_present
                article.save(update_fields=["file_exists"])
                updated += 1
                self.stdout.write(f"{'✅' if file_present else '❌'} {article.filename()}")

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} records."))
