import os

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.conference_map import conferences
from publications.models import UnifiedConferenceArticles


class Command(BaseCommand):
    help = "Rebuild the unified table of all conference articles"

    def handle(self, *args, **kwargs):
        UnifiedConferenceArticles.objects.all().delete()
        self.stdout.write("🧹 Cleared UnifiedConferenceArticles table")

        total = 0

        for short_code, model_name in conferences.items():
            model = apps.get_model("publications", model_name)
            for obj in model.objects.all():
                UnifiedConferenceArticles.objects.create(
                    title=obj.title,
                    authors=obj.authors,
                    abstract=obj.abstract,
                    year=obj.year,
                    edition=obj.edition,
                    url=obj.url,
                    country=obj.country,
                    article_index=obj.article_index,
                    file_exists=obj.file_exists,
                    file_source=obj.file_source,
                    filename=obj.filename(),
                    conference_name=obj.conference.name,
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Rebuilt unified table with {total} entries."))
