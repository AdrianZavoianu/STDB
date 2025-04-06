import csv

from django.core.management.base import BaseCommand

from publications.models import UnifiedArticles


class Command(BaseCommand):
    help = "Export UnifiedArticles to CSV, excluding specific journals and filtering missing files"

    # 🔴 Modify this list to exclude specific journal names
    EXCLUDED_JOURNALS = [
        "JSEE Journal of Seismology and Earthquake Engineering",
        "ACI Structural Journal",
        "AISC Journal of Structural Engineering"
    ]

    def handle(self, *args, **options):
        output_file = "data/unified_articles_export.csv"

        queryset = UnifiedArticles.objects.filter(file_exists=False).exclude(journal_name__in=self.EXCLUDED_JOURNALS)
        queryset = queryset.order_by("journal_name", "volume", "issue", "article_index")
        count = queryset.count()

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["doi", "title", "filename"])

            for article in queryset:
                writer.writerow([article.doi or "", article.title, article.filename()])

        self.stdout.write(self.style.SUCCESS(f"Exported {count} missing-file articles to {output_file}"))
