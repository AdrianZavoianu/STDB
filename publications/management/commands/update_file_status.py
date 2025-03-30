import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from publications.journal_map import journals


class Command(BaseCommand):
    help = "Update file_exists status for all ASCE journal articles"

    def add_arguments(self, parser):
        parser.add_argument("--journal", type=str, required=True, help="Journal short code (e.g. ASCE_JCC)")

    def handle(self, *args, **options):
        journal_key = options["journal"]
        if journal_key not in journals:
            self.stderr.write(self.style.ERROR(f"Invalid journal key: {journal_key}"))
            return

        model_name = journals[journal_key]
        model = apps.get_model("publications", model_name)

        pdf_dir = os.path.join(settings.MEDIA_ROOT, "publications")

        updated = 0
        for article in model.objects.all():
            expected_path = os.path.join(pdf_dir, article.filename())
            file_present = os.path.isfile(expected_path)
            if article.file_exists != file_present:
                article.file_exists = file_present
                article.save(update_fields=["file_exists"])
                updated += 1
                self.stdout.write(f"{'✅' if file_present else '❌'} {article.filename()}")

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} records."))
