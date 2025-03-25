# publications/management/commands/export_asce_doi_filenames.py

import csv

from django.core.management.base import BaseCommand

from publications.models import ASCEJournalStructuralEngineering


class Command(BaseCommand):
    help = 'Export DOI and filename for ASCE Journal articles'

    def handle(self, *args, **kwargs):
        output_path = 'data/asce_doi_filenames.csv'

        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['doi', 'filename'])

            for article in ASCEJournalStructuralEngineering.objects.all().order_by('year', 'volume', 'issue', 'article_index'):
                doi = article.doi or ''
                filename = f"STDB-{article.publication_code()}-{article.year}.pdf"
                writer.writerow([doi, filename])

        self.stdout.write(self.style.SUCCESS(f"Exported {article.__class__.__name__} to {output_path}"))
