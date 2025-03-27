from django.db import models

# Create your models here.

class DocumentType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"

    def __str__(self):
        return self.name

    def code(self):
        """Returns the ID padded to 2 digits, for use in filenames."""
        return f"{self.id:02}"

class JournalPublication(models.Model):
    name = models.CharField(max_length=255, unique=True)
    doc_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Journal Publication"
        verbose_name_plural = "Journal Publications"

    def __str__(self):
        return self.name

    def code(self):
        """Returns a padded code based on ID for filenames."""
        return f"{self.id:03}"

class BaseJournalArticle(models.Model):
    journal = models.ForeignKey("JournalPublication", on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=255, unique=True, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    volume = models.IntegerField()
    issue = models.IntegerField(default=0)  # Optional for journals without issues
    article_index = models.IntegerField()

    file_exists = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}.pdf"

class ASCEJournalStructuralEngineering(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Structural Engineering Article"
        verbose_name_plural = "ASCE Journal of Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"