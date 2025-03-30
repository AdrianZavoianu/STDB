import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand

from publications.journal_map import journals


class Command(BaseCommand):
    help = "Export DOI and filename for ASCE Journal articles where PDF is missing"

    def add_arguments(self, parser):
        parser.add_argument("--journal", type=str, required=True, help="Journal short code (e.g. ASCE_JCC)")

    def handle(self, *args, **options):
        journal_key = options["journal"]
        if journal_key not in journals:
            self.stderr.write(self.style.ERROR(f"Invalid journal key: {journal_key}"))
            return

        model_name = journals[journal_key]
        model = apps.get_model("publications", model_name)

        output_path = f'data/{journal_key}_missing_doi_filenames.csv'

        queryset = model.objects.filter(file_exists=False).order_by(
            'year', 'volume', 'issue', 'article_index'
        )

        os.makedirs("data", exist_ok=True)
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['doi', 'filename'])

            for article in queryset:
                doi = article.doi or ''
                filename = article.filename()
                writer.writerow([doi, filename])

        self.stdout.write(self.style.SUCCESS(
            f"Exported {queryset.count()} missing entries to {output_path}"
        ))
