import importlib

from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import UnifiedArticles


class Command(BaseCommand):
    help = "Populate unified table from individual journal article models"

    def handle(self, *args, **kwargs):
        UnifiedArticles.objects.all().delete()
        total_inserted = 0
        total_failed = 0

        for short_code, model_name in journals.items():
            try:
                module = importlib.import_module("publications.models")
                Model = getattr(module, model_name)
            except (ImportError, AttributeError) as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to import {model_name}: {e}"))
                continue

            self.stdout.write(self.style.WARNING(f"📚 Importing from: {model_name}"))

            for article in Model.objects.all():
                try:
                    UnifiedArticles.objects.get_or_create(
                        journal_name=article.journal.name,
                        title=article.title,
                        authors=article.authors,
                        abstract=article.abstract,
                        year=article.year,
                        doi=article.doi,
                        url=article.url,
                        volume=article.volume,
                        issue=article.issue,
                        article_index=article.article_index,
                        file_exists=article.file_exists,
                        publication_code=article.publication_code(),
                    )
                    total_inserted += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Failed to insert article {article.title[:50]}... Error: {e}"))
                    total_failed += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Done. Inserted: {total_inserted} | Failed: {total_failed}"))
