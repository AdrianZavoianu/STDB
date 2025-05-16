import csv

from django.core.management.base import BaseCommand

from publications.models import PCEEProceedings


class Command(BaseCommand):
    help = "Export filenames for WCEE articles in a hardcoded ID range"

    # Set ID range here ⬇️
    START_ID = 1
    END_ID = 167

    def handle(self, *args, **options):
        output_file = f"wcee_filenames_{self.START_ID}_{self.END_ID}.csv"

        queryset = (
            PCEEProceedings.objects
            .filter(id__gte=self.START_ID, id__lte=self.END_ID)
            .order_by("id")
        )
        count = queryset.count()

        if count == 0:
            self.stdout.write("⚠️ No articles found in the specified range.")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Filename"])

            for article in queryset:
                writer.writerow([article.id, article.filename()])

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {count} filenames to {output_file}"))
