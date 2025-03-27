# publications/management/commands/export_asce_doi_filenames.py

import csv

from django.core.management.base import BaseCommand

from publications.models import ASCEJournalStructuralEngineering


class Command(BaseCommand):
    help = 'Export DOI and filename for ASCE Journal articles where PDF is missing'

    def handle(self, *args, **kwargs):
        output_path = 'data/asce_missing_doi_filenames.csv'

        queryset = ASCEJournalStructuralEngineering.objects.filter(file_exists=False).order_by(
            'year', 'volume', 'issue', 'article_index'
        )

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
