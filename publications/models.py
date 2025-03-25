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