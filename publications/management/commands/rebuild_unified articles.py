import importlib

from django.core.management.base import BaseCommand

from publications.journal_map import journals
from publications.models import UnifiedArticles


class Command(BaseCommand):
    help = "Rebuilds the UnifiedArticles table by importing data from all journal-specific models."

    def handle(self, *args, **options):
        UnifiedArticles.objects.all().delete()
        self.stdout.write("🔄 Deleted all entries from UnifiedArticles.")

        inserted = 0
        skipped = 0

        for journal_key, model_name in journals.items():
            try:
                model = importlib.import_module("publications.models").__getattribute__(model_name)
            except AttributeError:
                self.stderr.write(f"❌ Model {model_name} not found.")
                continue

            articles = model.objects.all()
            self.stdout.write(f"📚 Importing from {model_name} ({articles.count()} articles)...")

            for article in articles:
                try:
                    UnifiedArticles.objects.create(
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
                        journal_name=str(article.journal.name),
                        publication_code=article.publication_code(),
                    )
                    inserted += 1
                except Exception as e:
                    skipped += 1
                    self.stderr.write(f"❌ Failed to insert article {article.title[:50]}... Error: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Rebuilt UnifiedArticles: {inserted} inserted, {skipped} skipped."))
