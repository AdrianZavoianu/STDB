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

class ASCEJournalStructuralDesignConstructionPractice(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Structural Design and Construction Practice"
        verbose_name_plural = "ASCE Journal of Structural Design and Construction Practice Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ASCEJournalPerformanceConstructedFacilities(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Performance of Constructed Facilities"
        verbose_name_plural = "ASCE Journal of Performance of Constructed Facilities Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ASCEJournalCompositesConstruction(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Composites for Construction"
        verbose_name_plural = "ASCE Journal of Composites for Construction Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierJournalConstructionalSteelResearch(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Journal of Constructional Steel Research"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierComputersStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Computers and Structures"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierEngineeringStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Engineering Structures"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierFiniteElementsAnalysisDesign(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Finite Elements in Analysis and Design"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierStructuralSafety(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Structural Safety"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerEarthquakeEngineeringEngineeringVibrations(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Earthquake Engineering and Engineering Vibrations"
        verbose_name_plural ="Springer Earthquake Engineering and Engineering Vibrations Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerInternationalJournalSteelStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer International Journal of Steel Structures"
        verbose_name_plural ="Springer International Journal of Steel Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerBulletinEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Bulletin of Earthquake Engineering"
        verbose_name_plural ="Springer Bulletin of Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerStructuralMultidisciplinaryOptimization(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Structural and Multidisciplinary Optimization"
        verbose_name_plural ="Springer Structural and Multidisciplinary Optimization Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerMaterialsStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Materials and Structures"
        verbose_name_plural ="Springer Materials and Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerComputationalMechanics(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Computational Mechanics"
        verbose_name_plural ="Springer Computational Mechanics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TaylorFrancisJournalEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Taylor & Francis Journal of Earthquake Engineering"
        verbose_name_plural ="Taylor & Francis Journal of Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TaylorFrancisMechanicsStructuresMaterials(BaseJournalArticle):
    class Meta:
        verbose_name = "Taylor & Francis Mechanics of Structures and Materials"
        verbose_name_plural ="Taylor & Francis Mechanics of Structures and Materials Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class IABSEJournalSeismologyEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "IABSE Journal of Seismology and Earthquake Engineering"
        verbose_name_plural ="IABSE Journal of Seismology and Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyStructuralDesignTallSpecialBuildings(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley The Structural Design of Tall and Special Buildings"
        verbose_name_plural ="Wiley The Structural Design of Tall and Special Buildings Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyEarthquakeEngineeringStructuralDynamics(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley Earthquake Engineering & Structural Dynamics"
        verbose_name_plural ="Wiley Earthquake Engineering & Structural Dynamics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyStructuralControlHealthMonitoring(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley Structural Control and Health Monitoring"
        verbose_name_plural ="Wiley Structural Control and Health Monitoring Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyInternationalJournalNumericalMethodsEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley International Journal for Numerical Methods in Engineering"
        verbose_name_plural ="Wiley International Journal for Numerical Methods in Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WSCInternationalJournalStructuralStabilityDynamics(BaseJournalArticle):
    class Meta:
        verbose_name = "WSC International Journal of Structural Stability and Dynamics"
        verbose_name_plural ="WSC International Journal of Structural Stability and Dynamics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SageEarthquakeSpectra(BaseJournalArticle):
    class Meta:
        verbose_name = "Sage Earthquake Spectra"
        verbose_name_plural ="Sage Earthquake Spectra Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SageAdvancesStructuralEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Sage Advances in Structural Engineering"
        verbose_name_plural ="Sage Advances in Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class JSEEJournalSeismologyEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "JSEE Journal of Seismology and Earthquake Engineering"
        verbose_name_plural ="JSEE Journal of Seismology and Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class AISCJournalStructuralEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "AISC Journal of Structural Engineering"
        verbose_name_plural ="AISC Journal of Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ACIStructuralJournal(BaseJournalArticle):

    class Meta:
        verbose_name = "ACI Structural Journal"
        verbose_name_plural ="ACI Structural Journal Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"