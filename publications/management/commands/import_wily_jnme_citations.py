import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Max

from publications.journal_map import journals
from publications.models import JournalPublication

volumes_years = {
    126:2025,125:2024,124:2023,123:2022,122:2021,121:2020,120:2019,119:2019,118:2019,117:2019,
    116:2018,115:2018,114:2018,113:2018,112:2017,111:2017,110:2017,109:2017,108:2016,
    107:2016,106:2016,105:2016,104:2015,103:2015,102:2015,101:2015,100:2014,99:2014,
    98:2014,97:2014,96:2013,95:2013,94:2013,93:2013,92:2012,91:2012,90:2012,89:2012,
    88:2011,87:2011,86:2011,85:2011,84:2010,83:2010,82:2010,81:2010,80:2009,79:2009,
    78:2009,77:2009,76:2008,75:2008,74:2008,73:2008,72:2007,71:2007,70:2007,69:2007,
    68:2006,67:2006,66:2006,65:2006,64:2005,63:2005,62:2005,61:2004,60:2004,59:2004,
    58:2003,57:2003,56:2003,55:2002,54:2002,53:2002,52:2001,51:2001,50:2000,49:2000,
    48:2000,47:2000,46:1999,45:1999,44:1999,43:1998,42:1998,41:1998,40:1997,39:1996,
    38:1995,37:1994,36:1993,35:1992,34:1992,33:1992,32:1991,31:1991,30:1990,29:1990,
    28:1989,27:1989,26:1988,25:1988,24:1987,23:1986,22:1986,21:1985,20:1984,19:1983,
    18:1982,17:1981,16:1980,15:1980,14:1979,13:1978,12:1978,11:1977,10:1976,9:1975,8:1974,
    7:1973,6:1973,5:1973,4:1972,3:1971,2:1970,1:1969
}

class Command(BaseCommand):
    help = "Import Wiley citations from structured .txt files with per-issue indexing"

    def add_arguments(self, parser):
        parser.add_argument("--journal", required=True, help="Journal code (e.g., WILEY_EQE)")
        parser.add_argument("--path", required=True, help="Path to folder with .txt files")

    def handle(self, *args, **options):
        journal_code = options["journal"]
        folder_path = options["path"]

        if journal_code not in journals:
            self.stderr.write(f"❌ Journal not found: {journal_code}")
            return

        model_name = journals[journal_code]
        try:
            model = apps.get_model("publications", model_name)
        except LookupError:
            self.stderr.write(f"❌ Model not found for: {model_name}")
            return

        try:
            journal_instance = JournalPublication.objects.get(name=model._meta.verbose_name)
        except JournalPublication.DoesNotExist:
            self.stderr.write(f"❌ JournalPublication instance not found for: {model._meta.verbose_name}")
            return

        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        for txt_file in txt_files:
            full_path = os.path.join(folder_path, txt_file)
            self.stdout.write(f"📄 Processing: {full_path}")

            # Extract volume and issue
            vol_issue_match = re.match(r"Wiley_Vol(\d+)_Issue(\d+)\.txt", txt_file)
            if not vol_issue_match:
                self.stderr.write(f"❌ Could not extract volume/issue from filename: {txt_file}")
                continue

            vol = int(vol_issue_match.group(1))
            issue = int(vol_issue_match.group(2))
            year = volumes_years.get(vol, 1900)

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            entries = [e.strip() for e in content.split("="*80) if e.strip()]
            article_counter = 0

            for entry in entries:
                try:
                    fields = dict(re.findall(r"^(Title|DOI|Authors|Article URL|PDF Link|Abstract):\s*(.*)", entry, re.MULTILINE))

                    doi = fields.get("DOI", "").replace("%2F", "/").strip()
                    if not doi or model.objects.filter(doi=doi).exists():
                        continue

                    authors = fields.get("Authors", "NA").strip() or "NA"
                    title = fields.get("Title", "NA").strip() or "NA"
                    abstract = fields.get("Abstract", "").strip()
                    url = f"https://doi.org/{doi}"

                    article_counter += 1
                    article_index = article_counter

                    if model.objects.filter(journal=journal_instance, volume=vol, issue=issue, article_index=article_index).exists():
                        self.stderr.write(f"⚠️ Duplicate index: Vol {vol} Issue {issue} Index {article_index} — skipping {doi}")
                        continue

                    article = model(
                        journal=journal_instance,
                        authors=authors,
                        title=title,
                        abstract=abstract,
                        doi=doi,
                        url=url,
                        volume=vol,
                        issue=issue,
                        year=year,
                        article_index=article_index,
                    )
                    article.save()
                    self.stdout.write(f"✅ Imported: {title[:60]}...")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to process entry in {txt_file}:\n{entry[:100]}...\nError: {e}")
