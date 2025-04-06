import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from publications.journal_map import journals


class Command(BaseCommand):
    help = "Update file_exists status for all journal articles across all journals"

    def handle(self, *args, **options):
        pdf_dir = os.path.join(settings.MEDIA_ROOT, "publications")
        total_updated = 0

        for journal_key, model_name in journals.items():
            try:
                model = apps.get_model("publications", model_name)
            except LookupError:
                self.stderr.write(self.style.ERROR(f"❌ Could not find model: {model_name}"))
                continue

            self.stdout.write(self.style.NOTICE(f"\n📘 Processing journal: {journal_key} → {model_name}"))
            updated = 0

            for article in model.objects.all():
                try:
                    expected_path = os.path.join(pdf_dir, article.filename())
                    file_present = os.path.isfile(expected_path)
                    if article.file_exists != file_present:
                        article.file_exists = file_present
                        article.save(update_fields=["file_exists"])
                        updated += 1
                        self.stdout.write(f"{'✅' if file_present else '❌'} {article.filename()}")
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"⚠️ Error processing article ID {article.id}: {e}"))

            self.stdout.write(self.style.SUCCESS(f"✔️ Updated {updated} records for {journal_key}"))
            total_updated += updated

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Total updated across all journals: {total_updated}"))
